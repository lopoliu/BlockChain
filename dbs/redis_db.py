from rediscluster import StrictRedisCluster
from redis.exceptions import ResponseError
import yaml

config = open(r'../config/server.yaml', 'rb')
conf = yaml.load(config)
config.close()


class SmsRedis(object):

    def __init__(self):
        self.host = conf['server']['redis_sms']['host']
        self.port = conf['server']['redis_sms']['port']
        nodes = [{"host": self.host, "port": self.port}]

        self.r = StrictRedisCluster(startup_nodes=nodes, decode_responses=True)
        # x = self.r.get("user:sms:13116285391_5")
        # print(x)

    def get_value(self, phone, types=None, only_value=True):
        kv = {}
        if types is not None:
            key = 'user:sms:' + phone + '_' + str(types)
            # print(key)
            try:
                kv[str(phone) + '_' + str(types)] = self.r.get(key)
                # print(kv)
            except ResponseError:
                pass
        else:
            for i in [1, 3, 4, 5, 6, 7, 8]:
                key = 'user:sms:' + phone + '_' + str(i)
                try:
                    if self.r.get(key) is not None:
                        kv[key] = self.r.get(key)
                except ResponseError:
                    pass
        if only_value:
            return kv[str(phone) + '_' + str(types)]
        else:
            return kv


if __name__ == '__main__':
    x = SmsRedis()
    v = str(x.get_value("13116285391", types=5))
    print(v)