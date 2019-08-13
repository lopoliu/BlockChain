# -*- coding:utf-8 -*-
# use/bin/evn python3


from websocket import create_connection
from logs.log_config import logger
import json

__author__ = 'Lopo'


class CounterServer(object):
    # 柜台服务器
    def __new__(cls, *args, **kwargs):
        logger.info('建立Socket连接'.center(30, '*'))
        cls.ws = create_connection('wss://coinrise.vip/front/')
        return super().__new__(cls)

    def __init__(self, user_id, token):
        self.user_id = user_id
        self.token = token

        data = {'Type': 0, 'UserId': self.user_id, 'Token': self.token, 'Data': {"Source": 1, "Action": 1}}
        logger.info('进行登记用户'.center(30, '*'))
        logger.info(str(data))
        self.ws.send(json.dumps(data))
        logger.info(self.ws.recv())

    def order(self, trade_coin_id: str, direction: int = 66):
        """ 委托下单 """
        coin_data = None
        # 价格与价格小数位
        price, price_decimal = 123400, 4
        # 数量与数量小数位
        volume, volume_decimal = 10000000, 6

        if direction == 66:     # 66 为买单
            logger.info('进行买单操作'.center(30, '*'))
        elif direction == 83:   # 83 为卖单
            logger.info('进行卖单操作'.center(30, '*'))

        if trade_coin_id == 'ETH':
            coin_data = {'BrokerID': 10, 'PriceCoinID': 'USDT', 'TradeCoinID': trade_coin_id, 'Direction': direction,
                         'Price': price, 'PriceDecimal': price_decimal, 'Volume': volume,
                         'VolumeDecimal': volume_decimal, 'OrderSouce': 85, 'OrderType': 1, 'CustomInfo': 'test'}

        elif trade_coin_id == 'BTC':
            pass

        elif trade_coin_id == 'LTC':
            pass

        send = {'Type': 1, 'UserID': self.user_id, 'Token': self.token, 'Data': coin_data}

        logger.info(str(send))
        # 以json格式发送数据
        self.ws.send(json.dumps(send))
        ws_info = self.ws.recv()
        logger.info(ws_info)

        try:
            # 如果出现交易失败 停止交易
            assert json.loads(ws_info)['Result']['Msg'] == '成功', '下单失败, 交易停止'
            logger.info('有内鬼，终止交易...')
        except AssertionError:
            self.__del__()
        return json.loads(ws_info)

    def __del__(self):
        self.ws.close()
        logger.info('服务关闭')