from services.miscellaneousServer import MiscellaneousServer


def get_dict_all_value(d: dict):
    _key = []
    values = []
    for i in d:
        _key.append(i)

    for i in _key:
        values.append(d[i])

    return values


if __name__ == '__main__':
    m = MiscellaneousServer()
    ds = m.get_bank_dict(token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJHcmVlbiIsImF1dGgiOiIiLCJl'
                                 'eHAiOjE1NjcwNzEzNDgsImlhdCI6MTU2NDQ3OTI4OCwiaXNzIjoiR3JlZW4iLCJzdWIiOjEwM'
                              'DAwMTcwMH0.4zUWB2lQ7iSDKboDOMG9KSGBGAAmSAGJ9xGKmJ6U6XI')
    x = get_dict_all_value(ds)
    print(x)