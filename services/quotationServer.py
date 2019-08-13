# -*- coding: utf-8 -*-
# usr/bin/env python3

import pprint
import time

import json

import yaml
from websocket import create_connection
from fake_useragent import UserAgent
from logs.log_config import logger

f = open('../config/server.yaml', 'r')
server_conf = yaml.load(f)
f.close()


class Quotation(object):
    """ 行情分发服务器 """
    def __new__(cls, *args, **kwargs):
        logger.info('建立Socket连接'.center(30, '*'))
        cls.ws = create_connection(server_conf['dev_server']['qtt'])
        return super().__new__(cls)

    def __init__(self):
        self.server = server_conf['dev_server']['qtt']

    def quotation(self, type_: int = 3, coin_id: str = 'BTC', ) -> dict:
        """ 获取一次行情数据 """
        data = {'Type': type_, 'Action': 1, 'PriceCoin': 'USDT', 'TradeCoin': coin_id, 'Source': 2}

        logger.info(str(data))
        self.ws.send(json.dumps(data))
        info = self.ws.recv()
        logger.info(info)

        # 以字典形式返回
        return json.loads(info)


if __name__ == '__main__':
    x = Quotation()
    i = x.quotation(type_=3)
    pprint.pprint(i)
