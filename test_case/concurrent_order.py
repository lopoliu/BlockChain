from multiprocessing import Process
from services.vipServer import UserPlatform
from services.c2cServer import C2CServer
from services.counterServer import CounterServer

c2c = C2CServer()
user = UserPlatform()
user_info = user.login_account('13100010002')
counter = CounterServer(token=user_info['Token'], user_id=user_info['Data']['ID'])

while True:
    counter.order(types=1, user_id=user_info['Data']['ID'], token=user_info['Token'], trade_coin_id='ETH', direction=66)
    # counter.order(types=1, user_id=user_info['Data']['ID'], token=user_info['Token'], trade_coin_id='ETH', direction=66)