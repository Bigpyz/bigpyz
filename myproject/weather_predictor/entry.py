from datetime import datetime
import os
import time
import webbrowser

from myproject.weather_predictor.csv_file_processor import processor
from myproject.weather_predictor.predictor_impl import predictor_impl


def get_user_input(prompt, valid_responses=None):
    """
    获取用户输入并验证

    Args:
        prompt (str): 提示用户输入的消息
        valid_responses (list, optional): 有效的响应列表. Defaults to None.

    Returns:
        str: 用户输入的响应

    Raises:
        None

    """
    while True:
        response = input(prompt).strip().lower()
        if valid_responses is None or response in valid_responses:
            return response
        print(f"无效输入，请输入: {'/'.join(valid_responses)}")


def get_root_path():
    """自动获取项目根目录"""
    current_file = os.path.abspath(__file__)
    path_parts = current_file.split(os.sep)
   
    try:
        bigpyz_index = path_parts.index('myproject')
        root_dir = os.sep.join(path_parts[:bigpyz_index + 1])
        # return root_dir  # 使用dirname获取上一级目录 刘建伟测试放开
        return os.path.dirname(root_dir) # 罗根湖测试放开
    except ValueError:
        return os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_file))))

def run_prediction(file_path):
    """运行预测流程"""
    try:
        # 获取预测起始日期
        while True:
            date_str = input("请输入预测起始日期 (格式: YYYY-MM-DD): ").strip()
            period = input("请输入预测天数 (默认10): ").strip()
            try:
                period = int(period)
                datetime.strptime(date_str, "%Y-%m-%d")                
                break
            except ValueError:
                print("日期格式错误，请使用 YYYY-MM-DD 格式")
                
         # 初始化处理器
        # proc = processor(file_path)
        
        # 创建预测器并运行预测
        predictor = predictor_impl(os.path.join(file_path, "result\\all_in_one_processed.csv"), period)
        predictor.set_base_date(date_str)
        predictor.create_predictor_from_csv()
        predictor.predict()
        predictor.predicton_data_saver()
        
        # 处理预测数据
        # proc.predicted_csv()
        
    except Exception as e:
        print(f"预测过程出错: {str(e)}")
        return False
    return True

def run_webservice(url_):
    # 初始化返回url
    url_r = url_
    
    # 检查URL是否以'http'开头，如果不是则添加'http:'
    if not url_[0:4] == 'http':
        url_r = 'http://' + url_
   
    try:
        # 等待1秒确保服务已启动
        time.sleep(1)
       
        # 使用默认浏览器打开URL
        webbrowser.open(url_r)
        print(f"已在浏览器中打开可视化页面 {url_r}")
       
    except Exception as e:
        print(f"打开浏览器页面出错: {str(e)}")
        return False
   
    return True

def start_all(start_scrapy,url_):    # 终极方法, 一切的开始
    
    open_webserver = False
    
    try:
        # 获取项目根路径
        root_path = get_root_path()
        if not os.path.exists(root_path):
            print(f"错误：路径 {root_path} 不存在")
            return
        
        # print(file_path)

        temperature_file = os.path.join(root_path, "result\\temperature.csv")
        # print(temperature_file)
        data_exists = os.path.exists(temperature_file)

        # 确定是否需要爬取数据
        need_crawl = False
        if not data_exists:
            print("原始爬虫数据不存在")
            need_crawl = get_user_input("是否启动爬虫? (y/n): ", ['y', 'n']) == 'y'
            if not need_crawl:
                print("请先启动爬虫")
                return
        else:
            print("原始爬虫数据已存在")
            need_crawl = get_user_input("是否重新爬取数据? (y/n): ", ['y', 'n']) == 'y'

        # 爬虫流程
        if need_crawl:
            try:
                # 在这里添加爬虫代码
                start_scrapy()
                print("爬虫执行完成")
            except Exception as e:
                print(f"爬虫过程出错: {str(e)}")
                return

        # 数据处理流程
        if get_user_input("是否启动数据处理? (y/n): ", ['y', 'n']) == 'y':
            try:
                proc = processor(root_path)
                proc.processed_csv()
                print("数据处理完成")
            except Exception as e:
                print(f"数据处理出错: {str(e)}")
                return

            # 预测流程
            if get_user_input("是否启动天气预测? (y/n): ", ['y', 'n']) == 'y':
                if run_prediction(root_path):
                    print("全部流程执行完成")
                else:
                    print("预测流程执行失败")
            else:
                print("天气数据已保存到all_in_one_processed.csv, 但未进行预测")
        else:
            if os.path.join(root_path, "all_in_one_processed.csv"):
                if get_user_input("处理后的数据已存在, 是否进行预测? (y/n): ", ['y', 'n']) == 'y':
                    if run_prediction(root_path):
                        print("全部流程执行完成")
                    else:
                        print("预测流程执行失败")
                else:
                    print("天气数据已保存到all_in_one_processed.csv, 但未进行预测")
            else:
                print("处理后的数据不存在, 结束")
                
        # 可视化启动流程
        open_webserver = get_user_input("是否启动可视化展示? (y/n): ", ['y', 'n']) == 'y' 
        if open_webserver:
            run_webservice(url_)
                            
    except Exception as e:
        print(f"程序执行出错: {str(e)}")

# if __name__ == "__main__":
#     start_all()
    
# 调用顺序：
# 1.爬虫
# 2.csv_file_processor.py->processed_csv()
# 3.predicoctor_impl.py
# 4.csv_file_processor.py->predicted_csv()
