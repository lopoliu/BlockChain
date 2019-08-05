import requests
import yaml
from logs.log_config import logger

f = open('../config/server.yaml', 'r')
server_conf = yaml.load(f)
f.close()


class ApiData(object):
    def __init__(self):
        self.host = server_conf['server']
        self.header = {'Version': '0.0', 'Token': ''}

    def get_bank_dict(self, token):
        api = self.host['mis'] + '/api/dictionary/bank'
        self.header['Token'] = token
        logger.info(str(self.header))
        response = requests.post(url=api, headers=self.header)
        logger.info(str(response.json()))
        return response.json()['Data']

    def get_coin_info(self, token):
        coin_list = []
        api = self.host['mis'] + '/api/dictionary/coin'
        self.header['Token'] = token
        logger.info(str(self.header))
        response = requests.post(url=api, headers=self.header)
        logger.info(str(response.json()))
        data = response.json()['Data']
        for i in data:
            coin_list.append(i['ID'])
        return coin_list


if __name__ == '__main__':
    x = ApiData()
    w = x.get_bank_dict(token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJHcmVlbiIsImF1dGgiOiIiLCJl'
                              'eHAiOjE1NjcwNzEzNDgsImlhdCI6MTU2NDQ3OTI4OCwiaXNzIjoiR3JlZW4iLCJzdWIiOjEwM'
                              'DAwMTcwMH0.4zUWB2lQ7iSDKboDOMG9KSGBGAAmSAGJ9xGKmJ6U6XI')
    print(w)