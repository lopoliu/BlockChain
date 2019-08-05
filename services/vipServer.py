# -*- coding:utf-8 -*-
# usr/bin/env python3

import sys
import copy
import json
import yaml
import random
import requests
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent
from logs.log_config import logger
import time

f = open('../config/server.yaml', 'r')
server_conf = yaml.load(f)
f.close()


class UserPlatform(object):
    ua = UserAgent()
    """用户平台"""
    def __init__(self):

        self.host = server_conf['server']
        self.header = {'Version': '0.0', 'Token': '', 'Connection': 'close', 'User-Agent': self.ua.random}

    def get_sms(self, phone_number=None, types=1):
        """
        获取一条验证码信息
        :param phone_number: 手机号
        :param types: 1	//注册 3 //设置资金密码 4	//修改资金密码 5	//登陆身份验证 6	//修改登陆密码
                      7 //提币验证码 8	//商家验证码登陆
        """
        logger.info('获取短信验证码'.center(30, '*'))
        time.sleep(0.2)
        api = self.host['vip'] + '/api/user/phone/veri'
        data = {"PhoneNumber": phone_number, "Type": types}
        logger.info(str(data))
        time.sleep(0.2)
        response = requests.post(url=api, headers=self.header, json=data)
        time.sleep(0.2)
        if response.status_code != 200:
            logger.error('服务器未启动'.center(30, "="))
            raise ConnectionError
        logger.info(str(response.json()))
        return response.json()

    def register(self, phone_number=None, code: str = "123456", password: str = 'zxc123..',
                       invite_code: str = '2FcNby', register_source=1, ip: str = "", machin_id="",
                       only_phone=False):
        """
        注册账户api
        :param phone_number: 账号（手机号）
        :param code: 注册账号验证码
        :param password: 设置密码
        :param invite_code: 邀请码
        :param register_source: 注册源
        :param ip: IP地址
        :param machin_id: 设备id
        :param only_phone: 返回手机号
        """
        # 如没有传入手机号参，则随机选取一个未注册的手机号
        if phone_number is None:
            middle = random.randint(1000, 9999)
            last = random.randint(1000, 9999)
            phone_number = '131' + str(middle) + str(last)
        logger.info('注册账号'.center(30, '*'))
        api = self.host['vip'] + '/api/user/register'  # 构建Api
        data = {'PhoneNumber': phone_number, 'PhoneVerificationCode': code, 'Password': password,
                'InviteCode': invite_code, 'RegisteredSource': register_source, 'IP': ip, 'MachinID': machin_id}
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        if only_phone:
            return phone_number
        else:
            return response.json()

    def login_account(self, phone_number="13100010001", password='zxc123..', login_source=1, verification_code='123456',
                      ip='', machin_id='', need_verification_code=1, only_token=False):
        """
        密码方式进行登录账户
        :param phone_number: 手机号
        :param password:    密码
        :param login_source:  登录源
        :param verification_code:  登录验证码
        :param ip:  ip
        :param machin_id: 设备id
        :param need_verification_code: 是否需要验证码
        :param only_token: 只返回token
        :return: response.json
        """
        api = self.host['vip'] + '/api/user/login'
        logger.info(str('进行登录操作').center(30, "*"))
        data = {'PhoneNumber': phone_number, 'Password': password, 'LoginSource': login_source,
                'PhoneVerificationCode': "", 'IP': ip, 'MachinID': machin_id, 'NeedCode': need_verification_code}
        # 如果为 1 则必须传入验证码
        if need_verification_code == 1:
            data['PhoneVerificationCode'] = verification_code
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        if response.status_code != 200:
            logger.error('服务器未启动'.center(30, '='))
            raise ConnectionError
        logger.info(str(response.json()))
        if only_token:
            # 只返回Token值
            return response.json()['Token']
        else:
            return response.json()

    def login_token(self, u_token, login_source=1, ip: str = '', machin_id: str = ''):
        """
        使用token登陆
        :param login_source:
        :param ip:
        :param u_token:
        :param machin_id:
        """
        print("使用token进行登录".center(30, '*'))
        api = self.host['vip'] + '/api/user/tokenlogin'
        data = {'LoginSource': login_source, 'IP': ip, 'MachinID': machin_id}
        self.header['Token'] = u_token
        logger.info(str(self.header))
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def get_user_info(self, tokens):
        """ 获取当前用户信息 """
        api = self.host['vip'] + '/api/user/info'
        logger.info('获取当前用户信息'.center(30, '*'))
        self.header['Token'] = tokens
        logger.info(str(self.header))
        response = requests.post(url=api, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def modify_head_img(self, img_address, token):
        """
        修改头像
        :param token
        :param img_address:  文件名称
        """
        logger.info('修改头像'.center(30, '*'))
        api = self.host['vip'] + '/api/user/headimage/modify'
        # 需要传入一个文件地址
        self.header['Token'] = token
        data = {'Image': img_address}
        logger.info(str(self.header))
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def reset_password(self, phone_number='13100010001', new_password='zxc123..', phone_veri_code='123456', token=None):
        """
        重置账户密码
        :param token
        :param phone_number: 需要重置的账户（手机号）
        :param phone_veri_code: 重置验证码
        :param new_password: 新密码
        """
        logger.info('重置密码'.center(30, '*'))
        api = self.host['vip'] + '/api/user/pw/reset'
        data = {'PhoneNumber': phone_number, 'PhoneVeriCode': phone_veri_code, 'NewPassword': new_password}
        logger.info(str(data))
        self.header['Token'] = token
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def modify_password(self, token='zxc123..', new_password='zxc123..', phone_veri_code='123456'):
        """
        修改账户密码
        :param token:  token
        :param new_password:   新密码
        :param phone_veri_code:  验证码
        """
        logger.info('修改密码'.center(30, '*'))
        api = self.host['vip'] + '/api/user/pw/modify'
        self.header['Token'] = token
        data = {'NewPassword': new_password, 'PhoneVeriCode': phone_veri_code}
        logger.info(str(data))
        response = requests.post(url=api, data=data, headers=self.header)
        logger.info(str(response.json()))
        return response

    def check_veri(self, phone_number: str, verification_code: str, types: str):
        """
        校验手机验证码
        :param phone_number:
        :param verification_code:
        :param types:
        """
        logger.info('验证手机验证码'.center(30, '*'))
        api = self.host + '/api/user/phone/vericheck'
        data = {'PhoneNumber': phone_number, 'VerificationCode': verification_code, 'Type': types}
        logger.info(str(data))
        response = requests.post(url=api, data=data, headers=self.header)
        logger.info(str(response.json()))
        return response

    def bind_bank_card(self, bank_id: int, card_number: str, card_owner: str, bank_addr: str, password: str, token):
        """
        绑定银行卡
        :param token: 账户token
        :param bank_id:  银行id
        :param card_number:  卡号
        :param card_owner:  持有人
        :param bank_addr:  开户行地址
        :param password:  资金密码
        """
        logger.info('绑定银行卡'.center(30, '*'))
        api = self.host['vip'] + '/api/user/bank/bind'
        data = {'BankID': bank_id, 'CardNumber': card_number, 'CardOwner': card_owner,
                'BankAddr': bank_addr, 'Password': password}
        self.header['Token'] = token
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def relieve_bank(self, u_id: int, password: str, token):
        """
        解绑银行卡
        :param token
        :param u_id:  绑定银行卡ID
        :param password:
        """
        logger.info('解除银行卡绑定'.center(30, '*'))
        api = self.host['vip'] + '/api/user/bank/delete'
        data = {'ID': u_id, 'Password': password}
        self.header['Token'] = token
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        self.header.pop('Token')
        return response.json()

    def bind_bank_info(self, user_id: int, token):
        """ 获取绑定银行信息 """
        api = self.host + '/api/user/bank/search'
        data = {'UserID': user_id}
        self.header['Token'] = token
        logger.info(str(self.header))
        response = requests.post(url=api, data=data, headers=self.header)
        logger.info(str(response.json()))
        return response

    def set_price_password(self, phone_vericode='123456', password='a12345678', token=None):
        """
        设定资金密码
        :param phone_vericode: 手机验证码
        :param password:  资金密码
        :param token: token
        """
        logger.info('设定资金密码'.center(30, '*'))
        api = self.host['vip'] + '/api/user/fundpw/set'
        self.header['Token'] = token
        data = {'PhoneVeriCode': phone_vericode, 'Password': password}
        logger.info(str(self.header))
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def modify_price_password(self, new_password, old_password='a12345678', phone_veri_code='123456', tokens=None):
        """
        修改资金密码
        :param tokens
        :param phone_veri_code:
        :param new_password:
        :param old_password:
        :return: response
        """
        logger.info('修改资金密码'.center(30, '*'))
        api = self.host['vip'] + '/api/user/fundpw/modify'
        data = {'PhoneVeriCode': phone_veri_code, 'NewPassword': new_password, 'OldPassword': old_password}
        self.header['Token'] = tokens
        logger.info(str(self.header))
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def check_price_password(self, token):
        """ 检验资金密码 """
        logger.info('校验资金密码'.center(30, '*'))
        api = self.host + '/api/user/fundpw/check'
        self.header['Token'] = token
        logger.info(str(self.header))
        response = requests.post(url=api, headers=self.header)
        logger.info(str(response.json()))
        return response

    def real_name_auth(self, name='lopo', country='中国', complexs="", address='深圳',
                       card_type=1, card_code=None, id_card_front="", id_card_back="", token=None):
        """
        实名认证
        :param name: 真实姓名
        :param country: 国家
        :param complexs: 手持证件照片地址（暂不使用）
        :param address: 户籍地址
        :param card_type: 证件类型
        :param card_code: 证件编号
        :param id_card_front: 证件正面照片地址
        :param id_card_back: 证件反面照片地址
        :param token
        """
        if card_code is None:
            before = random.randint(1000000, 9999999)
            last = random.randint(1000000, 9999999)
            card_code = str(before) + str(last)
        logger.info('实名认证操作'.center(30, '*'))
        api = self.host['vip'] + '/api/user/real/check'
        data = {'Name': name, 'Country': country, 'Complex': complexs, 'Address': address, 'CardType': card_type,
                'CardCode': card_code, 'IDCardFront': id_card_front, 'IDCardBack': id_card_back}
        self.header['Token'] = token
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def real_name_info(self, token):
        """ 查找自己的实名认证信息 """
        logger.info('实名认证信息'.center(30, '*'))
        api = self.host + '/api/user/real/search'
        self.header['Token'] = token
        logger.info(str(self.header))
        response = requests.post(url=api, headers=self.header)
        logger.info(str(response.json()))
        return response

    def real_name_cancel(self, token):
        """ 取消实名 """
        logger.info('取消实名'.center(30, "*"))
        api = self.host['vip'] + '/api/user/real/cancel'
        self.header['Token'] = token
        logger.info(str(self.header))
        response = requests.post(url=api, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def upload_img(self, file_path, account, types, token, expired_time=None):
        """
        上传图片文件到服务器
        :param file_path: 文件路径
        :param expired_time: ？？？ 可选参数
        :param account: 账户id
        :param types:  头像：user 认证：identity_authentication 二维码：QR_code
        :param token:
        """
        logger.info('上传图片到服务器'.center(30, '*'))
        files = {'file': ('pay.jpg', open(file_path, 'rb'), 'image/png', {})}
        api = self.host['img'] + '/upload/' + types
        data = {'account': account, 'type': 'user', 'token': token}
        if expired_time is not None:
            data['expiredTime'] = expired_time
        logger.info(str(data))
        response = requests.post(url=api, data=data, files=files, headers=self.header)
        logger.info(str(response.json()))
        img_url = json.loads(response.text)['Msg']
        return img_url

    def bind_qr_img(self, img_address, pay_type: int, account, password, token, mark="asd",):
        """
        绑定收款二维码
        :param pay_type:
        :param account:
        :param password:
        :param mark:
        :param img_address:
        :param token:
        """
        logger.info('绑定收款二维码'.center(30, '*'))
        api = self.host['vip'] + '/api/user/payqr/bind'
        data = {'Account': account, 'Mark': mark, 'Password': password, 'PayQRImage': img_address, 'PayType': pay_type}
        self.header['Token'] = token
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def relieve_qr_img(self, u_id, password, token):
        """
         解绑收款二维码
        :param u_id:
        :param password:
        :param token:
        """
        logger.info('取消绑定收款二维码'.center(30, '*'))
        api = self.host['vip'] + '/api/user/payqr/delete'
        data = {'ID': u_id, 'Password': password}
        self.header['Token'] = token
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def get_qr_code(self, user_id, token, only_id=False):
        """
        获取用户收款二维码
        :param user_id:
        :param token:
        :param only_id:
        """
        logger.info('获取绑定收款信息'.center(30, '*'))
        api = self.host['vip'] + '/api/user/payqr/search'
        data = {'UserID': user_id}
        self.header['Token'] = token
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        if only_id:
            try:
                id_list = []
                # 只返回收款码ID
                response_data = response.json()['Data']
                for i in response_data:
                    id_list.append(i['ID'])
                return id_list
            except TypeError:
                return response.json()
        return response.json()

    def get_all_info(self, user_id, token):
        """
        获取银行卡及收款二维码信息
        :param token
        :param user_id:
        """
        logger.info('获取银行卡及收款二维码信息'.center(30, '*'))
        api = self.host['vip'] + '/api/user/bankpayqr/search'
        self.header['Token'] = token
        data = {'UserID': user_id}
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def create_wallet(self, coin_id, token):
        """
        创建钱包
        :param token
        :param coin_id:
        """
        logger.info('创建钱包'.center(30, '*'))
        api = self.host["vip"] + '/api/user/wallet/create'
        data = {'CoinID': coin_id}
        self.header['Token'] = token
        logger.info(str(self.header))
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def get_coin_wallet(self, coin_id, token):
        """
        获取指定币种钱包
        :param coin_id:
        :param token:
        """
        logger.info('获取指定钱包'.center(30, '*'))
        api = self.host['vip'] + '/api/user/wallet/search'
        data = {'CoinID': str(coin_id)}
        logger.info(str(data))
        self.header['Token'] = token
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def get_all_wallet(self, token):
        """ 获取用户所有钱包 """
        logger.info('获取用户所有钱包'.center(30, '*'))
        api = self.host['vip'] + '/api/user/wallet/searchall'
        self.header['Token'] = token
        logger.info(str(self.header))
        response = requests.post(url=api, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def detailed_commission(self, coin_id, start_time, page_index, page_count, end_time, token):
        """
        获取返佣明细
        :param token:
        :param coin_id:
        :param start_time:
        :param page_index:
        :param page_count:
        :param end_time:
        """
        logger.info('获取币种信息'.center(30, '*'))
        api = self.host['vip'] + '/api/user/wallet/rebate/search'
        data = {'CoinID': coin_id, 'StartTime': start_time, 'PageIndex': page_index,
                'PageCount': page_count, 'EndTime': end_time}
        self.header['Token'] = token
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def recharge_coin_record(self, record_type, page_index, page_count, token):
        """
        获取充币提币记录
        :param token:
        :param record_type:
        :param page_index:
        :param page_count:
        """
        logger.info('获取充提币记录'.center(30, '*'))
        api = self.host["vip"] + '/api/user/wallet/iorecord/search'
        data = {'RecordType': record_type, 'PageIndex': page_index, 'PageCount': page_count}
        self.header['Token'] = token
        logger.info(str(data))
        response = requests.post(url=api, json=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()

    def extract_coin(self, coin_id, amount, decimal, password, address, phone_veri_code):
        """
        提币
        :param coin_id:
        :param amount:
        :param decimal:
        :param password:
        :param address:
        :param phone_veri_code:
        """
        logger.info('提币操作'.center(30, '*'))
        api = self.host + '/api/user/wallet/withdraw'
        data = {'CoinID': coin_id, 'Amount': amount, 'Decimal': decimal, 'Password': password,
                'Address': address, 'PhoneVeriCode': phone_veri_code}
        logger.info(str(data))
        response = requests.post(url=api, data=data, headers=self.header)
        logger.info(str(response.json()))
        return response.json()
