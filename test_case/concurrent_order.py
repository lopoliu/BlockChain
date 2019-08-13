from multiprocessing import Process
import time
from services.vipServer import UserPlatform
from services.c2cServer import C2CServer
from services.counterServer import CounterServer

c2c = C2CServer()
user = UserPlatform()
user_info = user.login_account('13100010001')

# 进行下单操作必须需要资金专用token
price_token = user.check_price_token(token=user_info['Token'], price_password='a12345678')
counter = CounterServer(token=price_token, user_id=user_info['Data']['ID'])

# 多线程实施多任务同时并发，测试资金解冻在极限情况下是否正确处理 （暂未完成）

while True:
    counter.order(trade_coin_id='ETH', direction=83)
    time.sleep(5)
    counter.order(trade_coin_id='ETH', direction=66)
    time.sleep(5)
