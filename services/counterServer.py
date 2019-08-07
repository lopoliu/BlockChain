from websocket import create_connection
import websocket
from logs.log_config import logger
import time
import json


class CounterServer(object):
    def __init__(self, user_id, token, types=0):
        logger.info('建立Socket连接'.center(30, '*'))
        self.ws = create_connection('wss://coinrise.vip/front/')
        self.types = types
        self.user_id = user_id
        self.token = token
        data = {'Type': self.types, 'UserId': self.user_id, 'Token': self.token, 'Data': {"Source": 1, "Action": 1}}
        logger.info('进行登记用户'.center(30, '*'))
        logger.info(str(data))
        self.ws.send(json.dumps(data))
        logger.info(self.ws.recv())

    def order(self, types: int, user_id: int, token: str, trade_coin_id: str, direction: int):
        """委托下单"""
        # Direction： 66 为买单，83 为卖单
        coin_data = None
        if trade_coin_id == 'ETH':
            coin_data = {'BrokerID': 10, 'PriceCoinID': 'USDT', 'TradeCoinID': trade_coin_id, 'Direction': direction,
                         'Price': 215400, 'PriceDecimal': 4, 'Volume': 10000000, 'VolumeDecimal': 6, 'OrderSouce': 85,
                         'OrderType': 1, 'CustomInfo': "test"}
        send = {"Type": types, "UserID": user_id, "Token": token, "Data": coin_data}
        logger.info('进行下单操作'.center(30, '*'))
        logger.info(str(send))
        self.ws.send(json.dumps(send))
        ws_info = self.ws.recv()
        logger.info(ws_info)
