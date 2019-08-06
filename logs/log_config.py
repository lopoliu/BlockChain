import logging
import os
import time


logger = logging.getLogger()
logger.setLevel(logging.INFO)

now_data = time.strftime("%Y-%m-%d", time.localtime())

file_path = str(now_data) + '.log'

pwd = os.getcwd()
log_dir_path = pwd + "\\" + file_path

if not os.path.exists(log_dir_path):
    with open(log_dir_path, 'w') as f:
        pass


console = logging.StreamHandler()
console.setLevel(logging.INFO)  # 输出到控制台

output = logging.FileHandler(log_dir_path, mode='a')    # 输出到log文件
output.setLevel(logging.INFO)

# 配置日志格式
formatter = logging.Formatter("%(asctime)s-%(funcName)s-%(levelname)s-||%(message)s")
console.setFormatter(formatter)
output.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(output)


logger.info(str(time.strftime('%Y-%m-%d %H:%M:%S')).center(30, "+"))


