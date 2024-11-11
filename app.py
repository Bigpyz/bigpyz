import os
import subprocess
import time
import webbrowser
from datetime import datetime
import redis
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import pandas as pd
from openai import OpenAI
import config
from myproject.weather_predictor.csv_file_processor import processor
from myproject.weather_predictor.entry import get_root_path
from myproject.weather_predictor.predictor_impl import predictor_impl

app = Flask(__name__)

#跨域启用
CORS(app)

# 连接到 Redis
r = redis.Redis(
    host='113.45.148.34',
    port=6379,
    password='mingri1234',
    db=3
)

# 初始化openai配置
client = OpenAI(
    base_url = 'https://xiaoai.plus/v1',
    # sk-xxx替换为自己的key
    api_key = config.api_key
)


# 启动Scrapy爬虫
@app.route('/scrapy', methods=['POST'])
def start_scrapy():
    try:
        # 执行Redis命令
        print("执行Redis命令...")
        # 检查键是否存在并获取当前值
        length = r.llen('weather_spider:start_url')
        # 如果键不存在或当前值为空，则执行 lpush
        if length == 0:
            r.lpush('weather_spider:start_url', config.first_url)
            print("已添加新的 URL 到 Redis")
        else:
            print("URL 已存在，跳过添加操作")

        # 启动 Scrapy 爬虫
        launch_scrapy_cmd = 'scrapy crawl weather_spider'
        process = subprocess.Popen(launch_scrapy_cmd, shell=True)
        process.wait()
        # 调用数据处理
        process_data()
        response = {
            "code": 200,
            "message": "Scrapy爬虫启动成功",
            "data": None
        }
        return jsonify(response)

    except Exception as e:
        print(f"发生意外错误: {e}")
        response = {
            "code": 400,
            "message": str(e),
            "data": None
        }
        return jsonify(response)


# 数据处理
@app.route('/process', methods=['POST'])
def process_data():
    root_path = get_root_path()
    try:
        proc = processor(root_path)
        proc.processed_csv()
        response = {
            "code": 200,
            "message": "数据处理完成",
            "data": None
        }
        return jsonify(response)
    except Exception as e:
        response = {
            "code": 400,
            "message": str(e),
        }
        return jsonify(response)


# 启动预测流程
@app.route('/predict', methods=['POST'])
def start_prediction():
    file_path = get_root_path()
    start_date = datetime.now().strftime("%Y-%m-%d")
    predict_period = 30
    try:
        predictor = predictor_impl(os.path.join(file_path, "result/all_in_one_processed.csv"), predict_period)
        predictor.set_base_date(start_date)
        predictor.create_predictor_from_csv()
        predictor.predict()
        predictor.predicton_data_saver()

        # 读取文件数据
        df = pd.read_csv(config.predict_path)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        dates = df['date'].dt.strftime('%Y年%m月%d日').tolist()

        hum = list(map(str, df['humidity_predicted'].tolist()))
        hei_tem = list(map(str, df['height_temperature_predicted'].tolist()))
        low_tem = list(map(str, df['low_temperature_predicted'].tolist()))
        preci = list(map(str, df['precipitation_predicted'].tolist()))

        data = {
            'dates': dates,
            'hum': hum,
            'hei_tem': hei_tem,
            'low_tem': low_tem,
            'preci': preci
        }

        response = {
            "code": 200,
            "message": "数据预测成功",
            "data": data
        }
        return jsonify(response)
    except Exception as e:
        response = {
            "code": 400,
            "message": str(e),
        }
        return jsonify(response)




# 统一请求拦截
@app.before_request
def before_request():
    return None


# 首页
@app.route("/")
def index():
    return render_template("index.html")



# chatGPT
@app.route("/chat", methods=["POST"])
def chat():
    try:
        text = request.args.get('text')
        if not text:
            return jsonify({"error": "请求参数 'text' 不能为空"}), 400
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": text}
            ]
        )
        msg = completion.choices[0].message.content

        response = {
            "code": 200,
            "message": "请求成功",
            "data": msg
        }
        return jsonify(response)

    except Exception as e:
        response = {
            "code": 400,
            "message": str(e),
        }
        return jsonify(response)


# 查询温度数据
@app.route("/tem/<int:year>", methods=["GET"])
def get_temperature(year):
    # 读取文件
    # 读取文件数据
    df = pd.read_csv(config.csv_path)
    df = pd.DataFrame(df)

    if df.empty:
        response = {
            "code": 400,
            "message": "温度数据为空",
        }
        return jsonify(response)

    # 转换为datetime对象
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # 转换为datetime，并处理无效日期
    # 过滤出指定年份的数据
    filtered_df = df[df['date'].dt.year == year]

    # 如果没有找到数据
    if filtered_df.empty:
        response = {
            "code": 400,
            "message": f"{year}年的温度数据为空",
        }
        return jsonify(response)

    # 转换为指定格式并放入列表
    dates = filtered_df['date'].dt.strftime('%Y年%m月%d日').tolist()

    # 将数据转换为字符串形式
    height_temperature = list(map(str, filtered_df['height_temperature'].tolist()))
    height_history_temperature = list(map(str, filtered_df['height_history_temperature'].tolist()))
    low_temperature = list(map(str, filtered_df['low_temperature'].tolist()))
    low_history_temperature = list(map(str, filtered_df['low_history_temperature'].tolist()))

    # 将数据放入一个大集合中
    data = {
        'dates': dates,
        'hei_temps': height_temperature,
        'hei_his_temps': height_history_temperature,
        'low_temps': low_temperature,
        'low_his_temps': low_history_temperature,
    }

    response = {
        "code": 200,
        "message": "温度数据获取成功",
        "data": data
    }

    return jsonify(response)



# 查询湿度数据
@app.route("/hum/<int:year>", methods=["GET"])
def get_humidity(year):
    # 读取文件数据
    df = pd.read_csv(config.csv_path)
    df = pd.DataFrame(df)

    # 读取文件
    if df.empty:
        response = {
            "code": 400,
            "message": "湿度数据为空",
        }
        return jsonify(response)
    # 转换为datetime对象
    df['date'] = pd.to_datetime(df['date'], errors='coerce')  # 转换为datetime，并处理无效日期
    # 过滤出指定年份的数据
    filtered_df = df[df['date'].dt.year == year]

    # 如果没有找到数据
    if filtered_df.empty:
        response = {
            "code": 400,
            "message": f"{year}年的湿度数据为空",
        }
        return jsonify(response)

    dates = filtered_df['date'].dt.strftime('%Y年%m月%d日').tolist()  # 转换为指定格式并放入列表
    humidity = list(map(str, filtered_df['humidity'].tolist()))
    humidity_history = list(map(str, filtered_df['humidity_history'].tolist()))


    data = {
        'dates': dates,
        'hums': humidity,
        'hums_his': humidity_history,
    }
    response = {
        "code": 200,
        "message": "湿度数据获取成功",
        "data": data
    }
    return jsonify(response)




# 查询风速数据
@app.route("/wind/<int:year>", methods=["GET"])
def get_wind(year):
    # 读取文件数据
    df = pd.read_csv(config.csv_path)
    df = pd.DataFrame(df)

    # 读取文件
    if df.empty:
        response = {
            "code": 400,
            "message": "风速数据为空",
        }
        return jsonify(response)

    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # 过滤出指定年份的数据
    filtered_df = df[df['date'].dt.year == year]
    # 如果没有找到数据
    if filtered_df.empty:
        response = {
            "code": 400,
            "message": f"{year}年的风速数据为空",
        }
        return jsonify(response)
    dates = filtered_df['date'].dt.strftime('%Y年%m月%d日').tolist()  # 转换为指定格式并放入列表
    wind_velocity = list(map(str, filtered_df['wind_velocity'].tolist()))
    wind_velocity_history = list(map(str, filtered_df['wind_velocity_history'].tolist()))
    data = {
        'dates': dates,
        'winds': wind_velocity,
        'winds_his': wind_velocity_history,
    }
    response = {
        "code": 200,
        "message": "风速数据获取成功",
        "data": data
    }
    return jsonify(response)


# 查询降水量数据
@app.route("/preci/<int:year>", methods=["GET"])
def get_preci(year):
    # 读取文件数据
    df = pd.read_csv(config.csv_path)
    df = pd.DataFrame(df)

    # 读取文件
    if df.empty:
        response = {
            "code": 400,
            "message": "降水数据为空",
        }
        return jsonify(response)

    # 获取参数
    # 获取日期列并转换格式
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    # 过滤出指定年份的数据
    filtered_df = df[df['date'].dt.year == year]
    # 如果没有找到数据
    if filtered_df.empty:
        response = {
            "message": f"{year}年的降水量数据为空",
            "code": 400,
            "data": None
        }
        return jsonify(response)
    dates = filtered_df['date'].dt.strftime('%Y年%m月%d日').tolist()  # 转换为指定格式并放入列表
    preci = list(map(str, filtered_df['precipitation'].tolist()))
    data = {
        'dates': dates,
        'preci': preci
    }
    response = {
        "code": 200,
        "message": "降水量数据获取成功",
        "data": data
    }
    return jsonify(response)


# 获取每日摘要（过去12个月）
@app.route("/sum", methods=["GET"])
def get_sum():
    year = datetime.now().year
    # 读取文件数据
    df = pd.read_csv(config.csv_path)
    df = pd.DataFrame(df)

    # 检查数据是否为空
    if df.empty:
        response = {
            "code": 400,
            "message": "数据为空",
        }
        return jsonify(response)

    # 处理日期列
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # 过滤出指定年份的数据
    filtered_df = df[df['date'].dt.year == year]

    # 如果没有找到数据
    if filtered_df.empty:
        response = {
            "code": 400,
            "message": f"{year}年的数据为空",
        }
        return jsonify(response)


    # 计算统计信息
    hei_tem = {
        'max': filtered_df['height_temperature'].max(),
        'min': filtered_df['height_temperature'].min(),
        'mean': round(filtered_df['height_temperature'].mean(), 2)
    }

    low_tem = {
        'max': filtered_df['low_temperature'].max(),
        'min': filtered_df['low_temperature'].min(),
        'mean': round(filtered_df['low_temperature'].mean(), 2)
    }

    wind = {
        'max': filtered_df['wind_velocity'].max(),
        'min': filtered_df['wind_velocity'].min(),
        'mean': round(filtered_df['wind_velocity'].mean(), 2)
    }

    preci = {
        'max': filtered_df['precipitation'].max(),
        'min': filtered_df['precipitation'].min(),
        'mean': round(filtered_df['precipitation'].mean(), 2)
    }

    # 将数据放入一个大集合中
    data = {
        'hei_tem': hei_tem,
        'low_tem': low_tem,
        'wind': wind,
        'preci': preci
    }

    response = {
        "code": 200,
        "message": "每日摘要数据获取成功",
        "data": data
    }

    return jsonify(response)



# @app.route("/test", methods=["GET"])
# def test():
#     print("test")
#     return "hello"


# 设置调度器
scheduler = BackgroundScheduler()
scheduler.add_job(start_scrapy, 'cron', hour=0, minute=0)  # 每天0点运行爬虫刷新数据
scheduler.start()


if __name__ == "__main__":
    # 静态文件缓存自动刷新
    app.jinja_env.auto_reload = True
    app.run(host="127.0.0.1", port=8002, debug=True)
