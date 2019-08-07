import logging
import os
import time


logger = logging.getLogger()
logger.setLevel(logging.INFO)

now_data = time.strftime("%Y-%m-%d", time.localtime())

file_path = str(now_data) + '.log'

path = r'G:\BlockChain\logs'
# log保存位置
log_dir_path = path + "\\" + file_path

# 如果log文件不存在则创建
if not os.path.exists(log_dir_path):
    with open(log_dir_path, 'w') as f:
        pass


console = logging.StreamHandler()
console.setLevel(logging.INFO)  # 输出到控制台

output = logging.FileHandler(log_dir_path, mode='a', encoding='utf-8')    # 输出到log文件，追加方式
output.setLevel(logging.INFO)

# 配置日志格式
formatter = logging.Formatter("%(asctime)s-<%(funcName)s>-%(levelname)s-||%(message)s")
console.setFormatter(formatter)
output.setFormatter(formatter)

logger.addHandler(console)
logger.addHandler(output)


logger.info(str(time.strftime('%Y-%m-%d %H:%M:%S')).center(30, "+"))


