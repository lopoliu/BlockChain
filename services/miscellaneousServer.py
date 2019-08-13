import requests
import yaml
from logs.log_config import logger

f = open('../config/server.yaml', 'r')
server_conf = yaml.load(f)
f.close()


class ApiData(object):
    # 杂项服务器
    def __init__(self):
        self.host = server_conf['dev_server']
        # self.host = server_conf['test_server']
        self.header = {'Version': '0.0', 'Token': ''}

    def get_bank_dict(self, token, only_id=True) -> list or dict:
        # only_id为true时，返回已个包含银行ID的列表
        logger.info('获取银行字典'.center(30, '*'))
        api = self.host['mis'] + '/dictionary/bank'
        self.header['Token'] = token
        logger.info(str(self.header))
        response = requests.post(url=api, headers=self.header, verify=False)
        logger.info(str(response.json()))
        if only_id:
            bank_id = []
            bank_list = response.json()['Data']
            for i in bank_list:
                bank_id.append(i['ID'])
            return bank_id
        return response.json()['Data']

    def get_coin_info(self, token) -> list:
        # 返回一个列表，包含所有币种名称
        coin_list = []
        api = self.host['mis'] + '/messy/dictionary/coin'
        self.header['Token'] = token
        logger.info(str(self.header))
        response = requests.post(url=api, headers=self.header, verify=False)
        logger.info(str(response.json()))
        data = response.json()['Data']
        for i in data:
            coin_list.append(i['ID'])
        return coin_list


if __name__ == '__main__':
    x = ApiData()
