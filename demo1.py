import requests

header = {
    'Version': '0.0',
    'Token': "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJhdWQiOiJHcmVlbiIsImF1dGgiOiIiLCJleHAiOjE1NjY1MzIyMDgsImlhdCI6MTU2Mzk0MDE0OCwiaXNzIjoiR3JlZW4iLCJzdWIiOjEwMDAwMTcwMH0.z_V0F5KIJ3xeVe9S2SVsoWA-AB1g795VCzR-dAut2dM",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/75.0.3770.142 Safari/537.36'
}


def bind_qr_img(image_addr, pay_type, account, password, mark="我是备注"):
    api = 'http://192.168.28.66:8600/api/user/payqr/bind'
    parameter = {
        'PayQRImage': image_addr,
        'PayType': pay_type,
        'Account': account,
        'Password': password,
        'Mark': mark
    }
    response = requests.post(url=api, json=parameter, headers=header)
    print(response.json())
    return response

# img_url = 'http://192.168.28.76:8605/static/user/100001700/identity_authentication_100001700_1564105747000.jpg'
# bind_qr_img(img_url, 3, "testasdz", "a12345678")

import yaml
import copy

c = open('./config/parameter.yaml')
y = yaml.load(c)
c.close()

m = open('modify_heade.png', 'rb')
print(m)


data = {
    'account': y['user_id'],
    'type': 'user',
    'token': y['token'],
}


files = {'file': ('modify_heade.png', open('modify_heade.png', 'rb'), 'image/png', {})}
url = 'http://192.168.28.76:8605/upload/user'
x = requests.post(url=url, data=data, files=files)

print(x.json())
print(x.status_code)

# , {"username": "test1",
#                                              "password": "zxc123..",
#                                              "act": "act_login",
#                                              "back_act": "user.php",
#                                              "submit": ""}
# from selenium import webdriver
#
#
# def create_account(start, number):
#     for i in range(start, start + number):
#         phantomjs.get('http://127.0.0.1/ecshop/upload/user.php?act=register')
#         phantomjs.find_element_by_id('username').send_keys(f"test{i}")                  # 用户名
#         phantomjs.find_element_by_id('email').send_keys(f'test{i}@qq.com')              # email
#         phantomjs.find_element_by_id('password1').send_keys('zxc123..')             # 密码
#         phantomjs.find_element_by_id('conform_password').send_keys('zxc123..')      # 确认密码
#         phantomjs.find_element_by_name('extend_field1').send_keys(f"test{i}@msn.com")   # MSN
#         phantomjs.find_element_by_name('extend_field2').send_keys(f"12345678{i}")       # QQ
#         phantomjs.find_element_by_name('extend_field3').send_keys(f"12345678{i}")       # 办公电话
#         phantomjs.find_element_by_name('extend_field4').send_keys(f"12345678{i}")       # 家庭电话
#         phantomjs.find_element_by_name('extend_field5').send_keys(f"13112341234{i}")    # 手机
#         phantomjs.find_element_by_name('sel_question').find_element_by_xpath("//option[@value='old_address']").click()
#         phantomjs.find_element_by_name('passwd_answer').send_keys("test")
#         phantomjs.find_element_by_name('Submit').click()
#         print('创建成功')
#     phantomjs.close()
#
#
# if __name__ == '__main__':
#     phantomjs = webdriver.PhantomJS("D:\\phantomjs\\bin\\phantomjs.exe")
#     create_account(0, 1)




