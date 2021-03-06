# -*- coding: utf-8 -*-
# usr/bin/env python3


from fake_useragent import UserAgent
import requests
import yaml

from logs.log_config import logger
from services.vipServer import UserPlatform


f = open('../config/server.yaml', 'r')
server_conf = yaml.load(f)
f.close()


class C2CServer(object):
    ua = UserAgent()
    """ C2C服务器 """
    def __init__(self):
        self.api_coinrise_vip = r'G:\BlockChain\services\ssl\api_coinrise_vip'
        self.coinrise_vip = r'G:\BlockChain\services\ssl\coinrise_vip'
        # self.host = server_conf['server']     # 测试环境
        self.host = server_conf['dev_server']['C2C']   # 正式环境   https://api.coinrise.vip/c2c
        self.header = {'Version': '0.0', 'Token': '', 'Connection': 'close', 'User-Agent': self.ua.random}

    def add_buy(self, u_id, biz_id=0, buy_type=1, decimal=2, amount=100,
                price=22200, payment_method=2, token=None, price_token=None):
        """ 买用户新增买单 """
        logger.info('用户新增买单'.center(30, '*'))
        api = self.host + '/v1/user/order/addbuy'
        self.header['Token'] = token
        data = {"UserId": u_id, "BizId": biz_id, "Amount": amount, "Decimal": decimal, "Price": price,
                "PaymentMethod": payment_method, "BuyType": buy_type, "CoinID": "USDT", "WalletToken": price_token}
        logger.info(data)
        response = requests.post(url=api, json=data, headers=self.header, verify=False)
        logger.info(response.json())
        return response.json()

    def add_sell(self, u_id, biz_id=0, buy_type=1, decimal=2, amount=100,
                 price=22200, payment_method=2, token=None, price_token=None):
        """ 用户新增卖单 """
        # 除了接口地址外，其他参数完全与买单易之
        logger.info('用户新增卖单'.center(30, '*'))
        api = self.host + '/v1/user/order/addsell'
        self.header['Token'] = token
        data = {"UserId": u_id, "BizId": biz_id, "Amount": amount, "Decimal": decimal, "Price": price,
                "PaymentMethod": payment_method, "BuyType": buy_type, "CoinID": "USDT", "WalletToken": price_token}
        logger.info(data)
        response = requests.post(url=api, json=data, headers=self.header, verify=False)
        logger.info(response.json())
        return response.json()


if __name__ == '__main__':
    u = UserPlatform()
    x = C2CServer()
    user_info = u.login_account('13100010002')
    p = u.check_price_token(user_info['Token'], 'a12345678')
    # price_token = u.wallet_token(user_info['Token'], p['Token'])
    x.add_sell(u_id=user_info['Data']['ID'], token=user_info['Token'], price_token=p)
    x.add_buy(u_id=user_info['Data']['ID'], token=user_info['Token'], price_token=p)
