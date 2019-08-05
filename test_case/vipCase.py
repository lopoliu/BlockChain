# -*- coding:utf-8 -*-
# /use/bin/env python3

import unittest
import yaml
import time
import random
from services.vipServer import UserPlatform
from services.miscellaneousServer import ApiData
from dbs.redis_db import SmsRedis
from dbs.sql_data import MySql

__Author__ = 'Lopo'

# 读取配置文件
file = open('../config/parameter.yaml', 'r')
config = yaml.load(file)
file.close()

user_platform = UserPlatform()      # 实例一个vip Api服务器
api_data = ApiData()
redis_server = SmsRedis()           # 连接到redis 短信服务器
mysql_server = MySql()

public_phone = mysql_server.my_phone()
_info = user_platform.login_account(public_phone)
public_token = _info['Token']
public_user_id = _info['Data']['ID']
public_price_password = 'a1234567'


class Test01GetSms(unittest.TestCase):

    def test_01(self):
        """ 正常输入 输入PhoneNumber参数值为1开头的11位数字，如 """

        # 获取已个可以接受短信的手机号
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone, types=5)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """ 输入PhoneNumber参数值不为1开头的11位数字，如05212341234 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone)
        self.assertEqual(eq['Result']['Msg'], '手机号格式错误')

    def test_03(self):
        """ 输入PhoneNumber参数值为12位数字，如188444455556 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone)
        self.assertEqual(eq['Result']['Msg'], '手机号格式错误')

    def test_04(self):
        """ 输入PhoneNumber参数值为10位数字，如1884444555 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone)
        self.assertEqual(eq['Result']['Msg'], '手机号格式错误')

    def test_05(self):
        """ 输入PhoneNumber参数值开头\中间\结尾包含中文\英文 """
        phone_n = ['a18844445555', '18844445555a', '188444a45555']
        for i in phone_n:
            eq = user_platform.get_sms(i)
            self.assertEqual(eq['Result']['Msg'], '[1002] 手机验证码错误')
            time.sleep(0.5)

    def test_06(self):
        """ 输入PhoneNumber参数为空 """
        eq = user_platform.get_sms(phone_number='')
        self.assertEqual(eq['Result']['Msg'], '[1002] 手机验证码错误')

    def test_07(self):
        """ 获取到注册验证码 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone, types=1)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_08(self):
        """ 获取到设置资金密码验证码 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone, types=3)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_09(self):
        """ 获取到修改资金密码验证码 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone, types=4)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_10(self):
        """ 获取到登陆身份验证验证码 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone, types=5)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_11(self):
        """ 获取到修改登陆密码验证码 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone, types=6)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_12(self):
        """ 获取到提币验证码 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone, types=7)
        self.assertEqual(eq['Result']['Msg'], "成功")

    def test_13(self):
        """ 获取到商家登陆验证码 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone, types=8)
        self.assertEqual(eq['Result']['Msg'], "成功")

    def test_14(self):
        """ 输入Type参数值为空 """
        phone = mysql_server.send_number()
        eq = user_platform.get_sms(phone, types='')
        self.assertEqual(eq['Result']['Msg'], '[21] 参数错误')

    def test_15(self):
        """ 输入Type参数值为其他数字 如 8/123/-1 """
        type_list = [000000, 123, -1]
        phone = mysql_server.send_number()
        for i in type_list:
            eq = user_platform.get_sms(phone, types=i)
            # 断言发送短信不为成功状态
            self.assertNotEqual(eq['Result']['Msg'], '成功')

    def test_16(self):
        """ 输入Type参数值为其他数字 如 8/123/-1 """
        phone = mysql_server.send_number()
        type_list = ['a', '@']
        for i in type_list:
            eq = user_platform.get_sms(phone, types=i)
            self.assertEqual(eq['Result']['Msg'], '[21] 参数错误')

    def test_17(self):
        """单日短信超10次"""
        phone = mysql_server.send_count_is_10()
        for i in range(10):
            user_platform.get_sms(phone)
            time.sleep(0.5)
        eq = user_platform.get_sms(phone)
        self.assertNotEqual(eq['Result']['State'], '[1064] 每账号每日只能使用10次短信')

    def test_18(self):
        """ 短信验证码错误3次 第四次正确输入"""
        user_num = mysql_server.send_number()
        # 发送一条登陆验证短信
        user_platform.get_sms(user_num, types=5)
        correct = redis_server.get_value(user_num, types=5)
        # 连续三次输入错误的验证
        code = ['000000', '111111', '222222']
        for i in code:
            user_platform.login_account(phone_number=user_num, verification_code=i)
        # 第四次输入正确
        eq = user_platform.login_account(phone_number=user_num, verification_code=correct)
        time.sleep(0.5)
        self.assertEqual(eq['Result']['State'], '验证码错误')



class Test02RegisterUser(unittest.TestCase):

    def test_01(self):
        """ 正常注册 """
        eq = user_platform.register()
        # 默认获取到一个随机手机号并进行注册
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """ 输入PhoneNumber参数值不为1开头的十一位数字 """
        before = random.randint(1000, 9999)
        last = random.randint(1000, 9999)
        error_phone = '032'+str(before) + str(last)
        eq = user_platform.register(error_phone)
        self.assertEqual(eq['Result']['Msg'], "手机号错误")

    def test_03(self):
        """ 输入PhoneNumber参数值为12/10位数字(长度错误)"""
        before = random.randint(1000, 9999)
        last = random.randint(1000, 9999)
        error_phone1 = '1321'+str(before) + str(last)
        error_phone2 = '13'+str(before) + str(last)
        phone_list = [error_phone1, error_phone2]
        for i in phone_list:
            eq = user_platform.register(i)
            self.assertEqual(eq['Result']['Msg'], "手机号错误")

    def test_04(self):
        """ 输入PhoneNumber参数包含字母 """
        last = random.randint(1000000, 9999999)
        for i in range(3):
            phone = str(last) + "12a"
            eq = user_platform.register(phone)
            self.assertEqual(eq['Result']['Msg'], "手机号错误")

    def test_05(self):
        """ 输入PhoneNumber参数值为空 """
        eq = user_platform.register(phone_number='')
        self.assertEqual(eq['Result']['Msg'], "[21] 参数错误")

    def test_07(self):
        """ 输入的PhoneNumber参数为已注册手机号 """
        eq = user_platform.register(phone_number='13100010001')
        self.assertEqual(eq['Result']['Msg'], '[1000] 手机号已被使用')

    def test_08(self):
        """ 输入PhoneVerificationCode参数值长度错误 """
        verification_code = random.randint(0, 99999)
        eq = user_platform.register(phone_number="17788887777", code=verification_code)
        self.assertEqual(eq['Result']['Msg'], '[21] 参数错误')
        time.sleep(0.5)

    def test_09(self):
        """ 输入PhoneVerificationCode参数值包含字母 """
        ramd_num = str(random.randint(100000, 9999999))
        verification_code = ['a' + ramd_num,
                             ramd_num + 'a',
                             '123' + ramd_num + '456',
                             '']
        for i in verification_code:
            eq = user_platform.register(phone_number=str(i))
            time.sleep(0.5)
            self.assertNotEqual(eq['Result']['Msg'], '[21] 参数错误')

    def test_10(self):
        """ 输入Password参数值为8-16位英文加数字 """
        eq = user_platform.register(password='aaa123456')
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_11(self):
        """ 输入Password参数值为8-16位纯英文/数字/符号 """
        password_list = ['123456789', 'password', '@@@@@@@@']
        for i in password_list:
            eq = user_platform.register(password=i)
            self.assertNotEqual(eq['Result']['Msg'], '成功')

    def test_12(self):
        """ 密码长度设置为8、16位 """
        password_list = ['a1234567', 'abcdabcd12345678']
        for i in password_list:
            eq = user_platform.register(password=i)
            self.assertNotEqual(eq['Result']['Msg'], '成功')

    def test_13(self):
        """ password长度错误 """
        # Todo: 此功能未实现
        password_list = ["a123456", "abcdefghi1234567890"]
        for i in password_list:
            eq = user_platform.register(password=i)
            self.assertNotEqual(eq['Result']['Msg'], '成功')

    def test_14(self):
        """ 设置password为空 """
        eq = user_platform.register(phone_number='13136174003', password='')
        # 断言结果不能为成功
        self.assertNotEqual(eq['Result']['Msg'], '成功')

    def test_15(self):
        """ 邀请码长度错误 """
        num1 = str(random.randint(100, 999))
        num2 = str(random.randint(10000, 99999))
        invite_code_list = ['aa'+num1, 'aa'+num2]
        for i in invite_code_list:
            eq = user_platform.register(i)
            # 断言结果不能为成功
            self.assertNotEqual(eq['Result']['Msg'], '成功')

    def test_16(self):
        """ 邀请码为空 """
        # 邀请码默参数可以为空
        eq = user_platform.register(invite_code="")
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_17(self):
        """ 输入InviteCode参数值为不存在的邀请码 """
        eq = user_platform.register(invite_code="Ab1234")
        self.assertNotEqual(eq['Result']['Msg'], '邀请码不存在')

    def test_18(self):
        """ 输入RegisteredSource参数值为1, 2, 3, 4 """
        registered_source = [1, 2, 3, 4]
        for i in registered_source:
            eq = user_platform.register(register_source=i)
            self.assertEqual(eq['Result']['Msg'], '成功')

    def test_19(self):
        """ 输入RegisteredSource参数值为中文/英文/符号 如：中/a/@ """
        registered_source = ['a', '123', "", '@']
        for i in registered_source:
            eq = user_platform.register(register_source=i)
            # 断言结果不能为成功
            self.assertNotEqual(eq['Result']['Msg'], '成功')

    def test_20(self):
        """ 输入RegisteredSource参数值为空 """
        eq = user_platform.register(register_source='')
        self.assertEqual(eq['Result']['Msg'], '[21] 参数错误')

    def test_21(self):
        """ 输入IP参数值为ip，如：0.0.0.0 """
        eq = user_platform.register(ip='191.255.255.abc')
        self.assertNotEqual(eq['Result']['Msg'], '成功')

    def test_22(self):
        """ 输入PhoneVerificationCode参数值为 可用的设置资金密码验证码 """
        code = [3, 4, 5, 6, 7, 8]
        # 获取一条其他功能的短信验证码
        _phone = '13116285392'
        for i in code:
            key = _phone + '_' + str(i)
            user_platform.get_sms(phone_number=_phone, types=i)
            time.sleep(0.5)
            # 获取到这条验证码
            code_dict = redis_server.get_value(_phone, types=i)
            # 调用注册账号接口
            eq = user_platform.register(code=code_dict[key])
            self.assertEqual(eq['Result']['Msg'], '[1002] 手机验证码错误')

    def test_23(self):
        """ MachinID """
        pass


class Test03Login(unittest.TestCase):
    def test_01(self):
        """ 正常登陆  """
        eq = user_platform.login_account(public_phone)
        # 验证Token不为空则是登陆成功
        self.assertNotEqual(eq['Token'], "")

    def test_02(self):
        """ 输入一个错误的手机号 开头错误，长度错误, 未注册 """
        phone_list = ['1310001000', '131000100010']
        for i in phone_list:
            eq = user_platform.login_account(i)
            self.assertEqual(eq['Result']['Msg'], '[1006] 用户不存在')
            time.sleep(0.5)

    def test_03(self):
        """ 手机号为空, 密码为空 """
        eq1 = user_platform.login_account(phone_number='')
        self.assertEqual(eq1['Result']['Msg'], '[21] 参数错误')
        eq2 = user_platform.login_account(phone_number='13100010001', password='')
        self.assertEqual(eq2['Result']['Msg'], '[21] 参数错误')
        time.sleep(0.5)

    def test_04(self):
        """ 登陆密码是否区分大小写 正确密码为：zxc123.. """
        _phone = mysql_server.my_phone()
        error_pwd = "zxc123..".upper()
        eq = user_platform.login_account(phone_number=_phone, password=error_pwd)
        self.assertEqual(eq['Result']['Msg'], '[1007] 密码错误')

    def test_05(self):
        """登陆密码错误上限账户被锁定"""
        # Todo: 暂未实现
        _phone = "13100030001"      # 请勿修改这个变量值
        _error = "zxc123"
        for i in range(5):
            user_platform.login_account(_phone, _error)
        eq = user_platform.login_account()
        self.assertEqual(eq['Result']['Msg'], "账户已被锁定")

    def test_06(self):
        """ 密码错误 """
        error = ['zxc123.', 'zxc123...', 'Zxc123..']
        for i in error:
            eq = user_platform.login_account(phone_number='13100010001', password=i)
            self.assertEqual(eq['Result']['Msg'], '[1007] 密码错误')
            time.sleep(0.5)

    def test_07(self):
        """ 登陆源不同   正常登陆 """
        login_source = [1, 2, 3, 4]
        for i in login_source:
            eq = user_platform.login_account(phone_number='13100010001', login_source=i)
            self.assertEqual(eq['Result']['Msg'], '成功')

    def test_08(self):
        """登陆源为负数/0, 英文， 中文"""
        error_source = [0, -1, "a", "源"]
        for i in error_source:
            eq = user_platform.login_account(phone_number='13100010001', login_source=i)
            self.assertEqual(eq['Result']['Msg'], '[21] 参数错误')

    def test_09(self):
        """ 登陆时验证码少一位/多一位 """
        error_code = ['12345', '1234567']
        for i in error_code:
            eq = user_platform.login_account(verification_code=i)
            self.assertEqual(eq['Result']['Msg'], '[1002] 手机验证码错误')

    def test_10(self):
        """ 不需要验证码 """
        eq = user_platform.login_account(need_verification_code=None)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_11(self):
        """ 开头\中间\结尾包含中文\字母，如：a123456\123a456\123456a """
        error_code = ['a123456', '123a456', '123456a']
        for i in error_code:
            eq = user_platform.login_account(verification_code=i)
            self.assertEqual(eq['Result']['Msg'], '[1002] 手机验证码错误')

    def test_12(self):
        """ 输入PhoneVerificationCode参数值为其他可用验证码 """
        code = [3, 4, 1, 6, 7, 8]
        _phone = '132111951890'
        # 获取一条错误的验证码
        for i in code:
            time.sleep(0.5)
            # 获取到这条验证码
            code_dict = redis_server.get_value(_phone, types=i)
            print(code_dict)
            # 调用登陆账号接口
            eq = user_platform.login_account(verification_code=code_dict)
            self.assertEqual(eq['Result']['Msg'], '[1002] 手机验证码错误')

    def test_13(self):
        """ ip """
        ip_list = ['0.0.0.0', '255.255.255.255', '255.255.255.256', '256.255.255.255', '']
        for i in ip_list:
            eq = user_platform.login_account(ip=i)
            time.sleep(0.5)
            self.assertEqual(eq['Result']['Msg'], '成功')

    def test_14(self):
        """ MachinID 设备id """
        pass

    def test_15(self):
        pass


class Test04TokenLogin(unittest.TestCase):

    def test_01(self):
        """ 使用正确的Token登陆 """
        # 使用全局token
        eq = user_platform.login_token(u_token=public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """ Token值错误 """
        error_srt = ['1', '@', 'a']
        for i in error_srt:
            tokens = public_token + i
            eq = user_platform.login_token(u_token=tokens)
            self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')
            time.sleep(0.5)
        for x in error_srt:
            tokens = x + public_token
            eq = user_platform.login_token(tokens)
            self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')
            time.sleep(0.5)

    def test_03(self):
        """ token 为空 """
        eq = user_platform.login_token(u_token='')
        self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')

    def test_04(self):
        """ token已过有效期 """
        pass

    def test_05(self):
        """登陆源参数 """
        source = [1, 2, 3]
        for i in source:
            eq = user_platform.login_token(public_token, login_source=i)
            time.sleep(0.5)
            self.assertEqual(eq['Result']['Msg'], '成功')

    def test_06(self):
        """ 登陆源错误 """
        source = [14, "@", 'a', '']
        for i in source:
            eq = user_platform.login_token(public_token, login_source=i)
            self.assertEqual(eq['Result']['Msg'], '[21] 参数错误')
            time.sleep(0.5)

    def test_07(self):
        """ ip错误 """
        ip_list = ['0.0.0.0', '255.255.255.255', '255.255.255.256', "256.255.255.255"]
        for i in ip_list:
            eq = user_platform.login_token(public_token, ip=i)
            self.assertEqual(eq['Result']['Msg'], '成功')

    def test_08(self):
        pass


class Test05GetUserInfo(unittest.TestCase):
    def test_01(self):
        """ 正常获取用户信息 """
        eq = user_platform.get_user_info(public_token)
        time.sleep(0.5)
        self.assertEqual(eq['Result']['Msg'], '成功')
        self.assertEqual(eq['Data']['ID'], public_user_id)
        self.assertEqual(eq['Data']['PhoneNumber'], public_phone)
        time.sleep(0.5)

    def test_02(self):
        """ 获取用户信息，token错误 """
        eq = user_platform.get_user_info(tokens="errorToken")
        self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')


class Test06ModifyHead(unittest.TestCase):

    def test_01(self):
        """ 正常修改，修改头像 """
        # 上传图片服务器
        img_url = user_platform.upload_img('../img/pay.jpg', public_user_id, 'user', token=public_token)
        time.sleep(1)
        eq = user_platform.modify_head_img(img_address=img_url, token=public_token)
        time.sleep(0.5)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """ 修改头像，图片大于2m"""
        # 上传图片服务器
        img_url = user_platform.upload_img('../img/2M.jpg', public_user_id, 'user', token=public_token)
        time.sleep(1)
        eq = user_platform.modify_head_img(img_address=img_url, token=public_token)
        time.sleep(0.5)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_03(self):
        """ 修改头像，图片地址错误 """
        img_url = "htt://test.png"
        eq = user_platform.modify_head_img(img_address=img_url, token=public_token)
        time.sleep(0.5)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_04(self):
        """ 修改头像，token错误"""
        """ 修改头像，图片大于2m"""
        # 上传图片服务器
        img_url = user_platform.upload_img('../img/2M.jpg', public_user_id, 'user', token=public_token)
        time.sleep(1)
        eq = user_platform.modify_head_img(img_address=img_url, token="errorToken")
        time.sleep(0.5)
        self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')


class Test07ResetPassword(unittest.TestCase):
    """ 重置密码 """
    @classmethod
    def tearDownClass(cls) -> None:
        """测试完成后重置密码为默认密码"""
        user_platform.reset_password(token=public_token)

    def test_01(self):
        """ 错误的手机号码 """
        phone_nub = ['18844445545', '03212341234', '118444455556', '14844445555a']
        for i in phone_nub:
            eq = user_platform.reset_password(i, token=public_token)
            self.assertEqual(eq['Result']['Msg'], '[152] 数据未找到')

    def test_02(self):
        """正常重置密码"""
        eq = user_platform.reset_password(public_phone, token=public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_03(self):
        """ 重置密码，手机号参数为空"""
        eq = user_platform.reset_password(phone_number='', token=public_token)
        self.assertEqual(eq['Result']['Msg'], '[152] 数据未找到')
        time.sleep(0.5)

    def test_04(self):
        """ 使用其他类型的短信验证码进行充值密码 """
        unregistered = '14455556666'
        registered = '13100010001'
        test_user = '17777777777'
        code_type = [1, 3, 4, 5, 7]
        for i in code_type:
            if i == 1:
                user_platform.get_sms(unregistered, types=i)
                code_dict = redis_server.get_value(unregistered, types=i)
                code = code_dict[unregistered + '_' + str(i)]
                print(code)
            else:
                user_platform.get_sms(registered, types=i)
                code_dict = redis_server.get_value(registered, types=i)
                code = code_dict[registered + '_' + str(i)]
                print(code)
            eq = user_platform.reset_password(phone_number=test_user, phone_veri_code=code, token=public_token)
            self.assertEqual(eq['Result']['Msg'], '[1002] 手机验证码错误')
            time.sleep(0.5)

    def test_05(self):
        """ 充值密码 短信验证码错误 """
        error_code = ['', '12345', '1234567', 'a123456', '123a456', '123456a']
        for i in error_code:
            eq = user_platform.reset_password(phone_veri_code=i, token=public_token)
            self.assertEqual(eq['Result']['Msg'], "[1002] 手机验证码错误")

    def test_06(self):
        """正常修改"""
        ok_password = ['a1234567', 'abcdabcd12345678', 'zxc123..']
        for i in ok_password:
            eq = user_platform.reset_password(phone_number=public_phone, new_password=i, token=public_token)
            self.assertEqual(eq['Result']['Msg'], '成功')
            time.sleep(0.5)

    def test_07(self):
        """密码中包含特殊字符"""
        password = ['aaaa@！@#￥%', '123456@！@#￥%']
        for i in password:
            eq = user_platform.reset_password(new_password=i, token=public_token)
            self.assertEqual(eq['Result']['Msg'], '成功')

    def test_08(self):
        """密码只包含一种字符"""
        # Todo: 预期与实际不符
        error_password = ['aaaaabbbbb', '123456789', '@@@@@@@@@']
        for i in error_password:
            eq = user_platform.reset_password(new_password=i, token=public_token)
            self.assertNotEqual(eq['Result']['Msg'], '成功')
            time.sleep(0.5)

    def test_09(self):
        """密码长度错误"""
        # Todo: 预期与实际不符, 预期8-16位字符
        error_password = ['123456a', '12345a6sd4a6sd123']
        for i in error_password:
            eq = user_platform.reset_password(new_password=i, token=public_token)
            time.sleep(0.5)
            self.assertNotEqual(eq['Result']['Msg'], '成功')

    def test_10(self):
        """新密码为空"""
        # Todo: 实际与预期不符
        eq = user_platform.reset_password(new_password='', token=public_token)
        self.assertNotEqual(eq['Result']['Msg'], '成功')
        time.sleep(0.5)


class Test08BindBank(unittest.TestCase):

    def test_01(self):
        """正常绑定，获取绑定信息，解除绑定银行卡"""
        # 获取所有银行信息
        print("asd", public_token)
        bank_info = api_data.get_bank_dict(token=public_token)
        time.sleep(2)
        for i in bank_info:
            bank_id = i['ID']
            print(f"+++开始测试绑定{i['Name']}+++")
            # 进行绑定操作
            eq = user_platform.bind_bank_card(int(bank_id), '64000123456782', 'lopo', '深圳福田车公庙支行', 'a12345678',
                                              public_token)
            time.sleep(0.5)
            # 获取所有绑定信息
            bank_info = user_platform.get_all_info(_info['Data']['ID'], public_token)
            time.sleep(0.5)
            # 完成绑定并验证后解除绑定
            user_platform.relieve_bank(bank_info['Bank']['ID'], 'a12345678', token=public_token)
            time.sleep(0.5)
            self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """ bank_id长度错误 """
        error_bank_id = ['764482494467201', '7644824944672']
        for i in error_bank_id:
            print(f"+++账号为{i}+++")
            # 进行绑定操作
            eq = user_platform.bind_bank_card(int(i), '64000123456782', 'lopo',
                                              '深圳福田车公庙支行', 'a12345678', public_token)
            time.sleep(0.5)
            # 获取所有绑定信息
            bank_info = user_platform.get_all_info(_info['Data']['ID'], public_token)
            # 完成绑定并验证后解除绑定
            time.sleep(0.5)
            user_platform.relieve_bank(bank_info['Bank']['ID'], 'a12345678', public_token)
            time.sleep(0.3)
            self.assertNotEqual(eq['Result']['Msg'], '成功')

    def test_03(self):
        """ 卡号包含非数字 """
        # Todo: 此功能没有实现，预期卡号不能包含非数字
        error_card = ['123123123123aq', 'as123123123123', '23123as12312']
        for i in error_card:
            eq = user_platform.bind_bank_card(76448249446400, i, 'lopo', '深圳福田车公庙支行', 'a12345678', public_token)
            time.sleep(0.5)
            # 获取所有绑定信息
            bank_info = user_platform.get_all_info(_info['Data']['ID'], public_token)
            time.sleep(0.5)
            # 完成绑定并验证后解除绑定
            user_platform.relieve_bank(bank_info['Bank']['ID'], 'a12345678', public_token)
            self.assertNotEqual(eq['Result']['Msg'], '成功')
            time.sleep(0.5)

    def test_04(self):
        """解绑银行卡，资金密码错误"""
        error_price_password = ["a1234567", '1234567', "123a4564"]
        user_platform.bind_bank_card(76448249446400, '64000123456781', 'lopo', '深圳福田车公庙支行', 'a12345678', public_token)
        time.sleep(0.4)
        # 获取所有绑定信息
        bank_info = user_platform.get_all_info(_info['Data']['ID'], public_token)
        for i in error_price_password:
            time.sleep(0.5)
            # 完成绑定并验证后解除绑定
            user_platform.relieve_bank(bank_info['Bank']['ID'], i, public_token)
            time.sleep(0.5)

    def test_05(self):
        """解绑未绑定的账户"""
        user = user_platform.login_account("13171362796")
        bank_info = user_platform.get_all_info(user['Data']['ID'], token=user['Token'])
        ids = bank_info['Bank']['ID']
        user_platform.relieve_bank(u_id=ids, password="a12345678", token=public_token)
        eq = user_platform.relieve_bank(u_id=ids, password="a12345678", token=public_token)
        self.assertEqual(eq['Result']['Msg'], '[21] 参数错误')


class Test09SetPricePassword(unittest.TestCase):
    """只有新注册的账号才能设定资金密码"""

    def test_01(self):
        """正常设定"""
        # 新注册一个账号，并登陆获得该账户的Token
        new_user = user_platform.register(only_phone=True)
        user_info = user_platform.login_account(new_user)
        token = user_info['Token']
        eq = user_platform.set_price_password('123456', 'a12345678', token=token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """使用已设定过资金密码的账户进行操作"""
        eq = user_platform.set_price_password('123456', password='a12345678', token=public_token)
        self.assertEqual(eq['Result']['Msg'], '[1015] 已设置资金密码')

    def test_03(self):
        """ 资金密码不符合要求 """
        price_password = ['', "1", '@']
        new_user = user_platform.register(only_phone=True)
        user_info = user_platform.login_account(new_user)
        token = user_info['Token']
        for i in price_password:
            eq = user_platform.set_price_password('123456', i, token)
            self.assertNotEqual(eq['Result']['Msg'], '成功')
            time.sleep(0.5)

    def test_04(self):
        """token错误/token为空"""
        token_list = ['error', '']
        for i in token_list:
            eq = user_platform.set_price_password('123456', 'a12345678', token=i)
            self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')

    def test_05(self):
        """手机验证码错误/手机验证码为空"""
        code_list = ['12345', '1234567', '']
        new_user = user_platform.register(only_phone=True)
        user_info = user_platform.login_account(new_user)
        for i in code_list:
            eq = user_platform.set_price_password(i, 'a12345678', user_info['Token'])
            self.assertEqual(eq['Result']['Msg'], '[1002] 手机验证码错误')

    def test_06(self):
        """设定资金密码与登录密码一致"""
        # Todo: 此功能未实现，预期登录密码与实际密码不能一致
        # 登录密码为zxc123..
        login_password = 'zxc123..'
        new_user = user_platform.register(only_phone=True)
        user_info = user_platform.login_account(new_user)
        eq = user_platform.set_price_password('123456', login_password, token=user_info['Token'])
        self.assertNotEqual(eq['Result']['Msg'], '成功')


class Test10ModifyPricePassword(unittest.TestCase):
    price = 'a12345678'

    def test_01(self):
        """正常修改资金密码"""
        eq = user_platform.modify_price_password(new_password='a123456789', old_password=self.price,
                                                 tokens=public_token)
        time.sleep(0.5)
        user_platform.modify_price_password(new_password=self.price, old_password='a123456789',
                                            tokens=public_token)
        time.sleep(0.5)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """ 重置资金密码 token错误"""
        eq = user_platform.modify_price_password(self.price, 'a12345678', tokens="qweqwe")
        self.assertEqual(eq['Result']['Msg'], "[20] 身份验证失败")

    def test_03(self):
        """ 重置资金密码 新密码与旧密码相同 """
        eq = user_platform.modify_price_password(self.price, self.price, tokens=public_token)
        self.assertEqual(eq['Result']['Msg'], "成功")

    def test_04(self):
        """ 重置资金密码 资金密码与登录密码一致 """
        eq = user_platform.modify_price_password(new_password='zxc123..', old_password=self.price, tokens=public_token)
        time.sleep(0.5)
        user_platform.modify_price_password(new_password=self.price, old_password='zxc123..', tokens=public_token)
        time.sleep(0.5)
        self.assertNotEqual(eq['Result']['Msg'], "成功")

    def test_05(self):
        """ 资金密码设置为空 """
        eq = user_platform.modify_price_password(new_password='', old_password=self.price, tokens=public_token)
        user_platform.modify_price_password(new_password=self.price, old_password='', tokens=public_token)
        self.assertNotEqual(eq['Result']['Msg'], '成功')


class Test11RealNameAuth(unittest.TestCase):
    """实名认证"""
    # 一个身份证只能绑定一个账号，暂未实现
    @classmethod
    def get_data(cls):
        # 从数据库获得手机号
        not_real_name_user = mysql_server.not_real_name_user()
        token = user_platform.login_account(phone_number=not_real_name_user, only_token=True)
        time.sleep(0.5)
        # 将身份证正反面图片上传单图片服务器
        front = user_platform.upload_img('../img/id_card_1.png', public_user_id,
                                         'identity_authentication', public_token)
        time.sleep(0.5)
        back = user_platform.upload_img('../img/id_card_2.png', public_user_id,
                                        'identity_authentication', public_token)
        return token, front, back

    def test_01(self):
        """正常实名认证， 证件类型为身份证"""
        # 开始绑定身份证
        token, front, back = self.get_data()
        eq = user_platform.real_name_auth(card_type=1, id_card_front=front, id_card_back=back, token=token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_01_1(self):
        """ 证件类型为护照 """
        token, front, back = self.get_data()
        eq = user_platform.real_name_auth(card_type=2, id_card_front=front, id_card_back=back, token=token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_01_2(self):
        """ 证件类型为港澳回乡证 """
        token, front, back = self.get_data()
        eq = user_platform.real_name_auth(card_type=3, id_card_front=front, id_card_back=back, token=token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_01_3(self):
        """ 证件类型为台胞证 """
        token, front, back = self.get_data()
        eq = user_platform.real_name_auth(card_type=4, id_card_front=front, id_card_back=back, token=token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """ 姓名为空 """
        _user_num = "17323131131"
        _token = user_platform.login_account(_user_num, only_token=True)
        _front = 'http://192.168.28.76:8605/static/identity_authentication/100001700/user_100001700_1564564585000.png'
        _back = 'http://192.168.28.76:8605/static/identity_authentication/100001700/user_100001700_1564564586000.png'
        eq = user_platform.real_name_auth(id_card_front=_front, id_card_back=_back, token=_token, name='')
        self.assertEqual(eq['Result']['Msg'], '[1058] 名称长度不合法')

    def test_03(self):
        """卡号为空"""
        token, front, back = self.get_data()
        eq = user_platform.real_name_auth(id_card_front=front, id_card_back=back, token=token, card_code="")
        self.assertNotEqual(eq['Result']['Msg'], "成功")

    def test_04(self):
        """ 重复提交 """
        _user_num = "17323131132"
        _token = user_platform.login_account(_user_num, only_token=True)
        _front = 'http://192.168.28.76:8605/static/identity_authentication/100001700/user_100001700_1564564585000.png'
        _back = 'http://192.168.28.76:8605/static/identity_authentication/100001700/user_100001700_1564564586000.png'
        user_platform.real_name_auth(id_card_front=_front, id_card_back=_back, token=_token, card_code="")
        time.sleep(0.5)
        eq = user_platform.real_name_auth(id_card_front=_front, id_card_back=_back, token=_token, card_code="")
        self.assertEqual(eq['Result']['Msg'], '[1016] 已提交过实名认证，正在审核中')

    def test_05(self):
        """取消实名认证"""
        # 实名认证后，无法取消实名认证
        eq = user_platform.real_name_cancel(token=public_token)
        self.assertEqual(eq['Result']['Msg'], '[1054] 实名认证成功不可取消')


class Test12BindQrCode(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        qr_id = user_platform.get_qr_code(public_user_id, public_token, only_id=True)
        for i in qr_id:
            time.sleep(0.5)
            user_platform.relieve_qr_img(i, 'a12345678', token=public_token)

    def test_01(self):
        """ 绑定收款二维码 支付宝"""
        img_url = user_platform.upload_img(file_path='../img/pay.jpg', account=public_user_id,
                                           types='user', token=public_token)
        time.sleep(0.5)
        eq = user_platform.bind_qr_img(img_address=img_url, pay_type=2, account="支付宝",
                                       password="a12345678", token=public_token)
        time.sleep(0.5)
        # 测试完成后立即取消绑定
        qr_id = user_platform.get_qr_code(public_user_id, public_token, only_id=True)
        time.sleep(0.5)
        user_platform.relieve_qr_img(qr_id, 'a12345678', token=public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_01_01(self):
        """ 绑定收款二维码 微信"""
        img_url = user_platform.upload_img(file_path='../img/pay.jpg', account=public_user_id,
                                           types='user', token=public_token)
        time.sleep(0.5)
        eq = user_platform.bind_qr_img(img_address=img_url, pay_type=3, account="微信",
                                       password="a12345678", token=public_token)
        time.sleep(0.5)
        # 测试完成后立即取消绑定
        qr_id = user_platform.get_qr_code(public_user_id, public_token, only_id=True)
        time.sleep(0.5)
        user_platform.relieve_qr_img(qr_id, 'a12345678', token=public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_01_03(self):
        """ 绑定收款二维码 所有"""
        img_url = user_platform.upload_img(file_path='../img/pay.jpg', account=public_user_id,
                                           types='user', token=public_token)
        time.sleep(0.5)
        eq = user_platform.bind_qr_img(img_address=img_url, pay_type=1, account="银行卡",
                                       password="a12345678", token=public_token)
        time.sleep(0.5)
        # 测试完成后立即取消绑定
        qr_id = user_platform.get_qr_code(public_user_id, public_token, only_id=True)
        time.sleep(0.5)
        user_platform.relieve_qr_img(qr_id, 'a12345678', token=public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """多次绑定"""
        img_url = user_platform.upload_img(file_path='../img/pay.jpg', account=public_user_id,
                                           types='user', token=public_token)
        user_platform.bind_qr_img(img_address=img_url, pay_type=2, account="支付宝",
                                  password="a12345678", token=public_token)
        eq = user_platform.bind_qr_img(img_address=img_url, pay_type=2, account="支付宝",
                                       password="a12345678", token=public_token)
        self.assertEqual(eq['Result']['Msg'], "[3] 数据已存在")


class Test14QrCodeClear(unittest.TestCase):
    def test_01(self):
        """取消绑定收款码"""
        qr_id = user_platform.get_qr_code(public_user_id, public_token, only_id=True)
        for i in qr_id:
            eq = user_platform.relieve_qr_img(i, 'a12345678', token=public_token)
            self.assertEqual(eq['Result']['Msg'], '成功')
            time.sleep(0.4)

    def test_02(self):
        """没有绑定信息时取消绑定（qr_id错误）"""
        eq = user_platform.relieve_qr_img(u_id=120014, password='a12345678', token=public_token)
        self.assertEqual(eq['Result']['Msg'], '[4] 数据不存在')
        time.sleep(0.5)


class Test15GetQrInfo(unittest.TestCase):
    def test_01(self):
        """获取账户绑定收款信息"""
        eq = user_platform.get_qr_code(public_user_id, public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """获取用户绑定收款信息 token为空"""
        eq = user_platform.get_qr_code(public_user_id, token='')
        self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')

    def test_03(self):
        """获取用户绑定收款信息 id错误"""
        eq = user_platform.get_qr_code(user_id=123, token=public_token)
        self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')


class Test14CreateWallet(unittest.TestCase):

    def test_01(self):
        """正常创建钱包"""
        # 注册一个新用户
        new_user = user_platform.register(only_phone=True)
        # 登陆新用户并获取到token
        tokens = user_platform.login_account(new_user, only_token=True)
        # 获取到所有币种
        coin_list = api_data.get_coin_info(tokens)
        for i in coin_list:
            eq = user_platform.create_wallet(coin_id=i, token=tokens)
            self.assertEqual(eq['Result']['Msg'], '成功')
            time.sleep(1)

    def test_02(self):
        """重复创建同一个币种"""
        new_user = user_platform.register(only_phone=True)
        # 登陆新用户并获取到token
        tokens = user_platform.login_account(new_user, only_token=True)
        user_platform.create_wallet(coin_id='BTC', token=tokens)
        eq = user_platform.create_wallet(coin_id='BTC', token=tokens)
        self.assertEqual(eq['Result']['Msg'], '[1102] 该币种钱包已存在')
        time.sleep(0.5)

    def test_03(self):
        """ 创建不存在的币种 """
        # ICT为不存在的币种
        eq = user_platform.create_wallet(coin_id='ICT', token=public_token)
        self.assertEqual(eq['Result']['Msg'], '[30] 币种信息不存在')

    def test_04(self):
        """ token错误 """
        error_token = ['', "i'm is tokens"]
        for i in error_token:
            eq = user_platform.create_wallet(coin_id="BTC", token=i)
            self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')

    def test_05(self):
        """ 币种为小写 """
        # 注册一个新用户
        new_user = user_platform.register(only_phone=True)
        # 登陆新用户并获取到token
        tokens = user_platform.login_account(new_user, only_token=True)
        # 获取到所有币种
        coin_list = api_data.get_coin_info(tokens)
        for i in coin_list:
            eq = user_platform.create_wallet(coin_id=str(i).lower(), token=tokens)
            self.assertEqual(eq['Result']['Msg'], '[30] 币种信息不存在')
            time.sleep(1)

    def test_06(self):
        """ 币种为空 """
        eq = user_platform.create_wallet(coin_id='', token=public_token)
        self.assertEqual(eq['Result']['Msg'], '[21] 参数错误')


class Test15GetAllWallet(unittest.TestCase):
    def test_01(self):
        """获取一个用户的所有钱包"""
        eq = user_platform.get_all_wallet(token=public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """ 获取一个用户的所有钱包token错误 """
        eq = user_platform.get_all_wallet(token=public_token+'iAs')
        self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')
        time.sleep(0.5)


class Test16GetCoinWallet(unittest.TestCase):
    def test_01(self):
        """ 正常获取BTC币种钱包 """
        coin_info = api_data.get_coin_info(token=public_token)
        for i in coin_info:
            eq = user_platform.get_coin_wallet(i, token=public_token)
            self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """ 获取BTC币种钱包 币种参数错误 """
        eq = user_platform.get_coin_wallet(coin_id='ICT', token=public_token)
        self.assertEqual(eq['Result']['Msg'], '[30] 币种信息不存在')

    def test_03(self):
        """ 获取BTC币种钱包 token错误"""
        eq = user_platform.get_coin_wallet(coin_id='BTC', token=public_token+"acA")
        self.assertEqual(eq['Result']['Msg'], '[20] 身份验证失败')


class Test17DetailedCommission(unittest.TestCase):
    def test_01(self):
        """获取到佣金明细"""
        eq = user_platform.detailed_commission('BTC', 20190601000000, 1, 50, 20190801000000, public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """获取佣金明细 开始时间大于借宿时间"""
        eq = user_platform.detailed_commission('BTC', 20190801000000, 1, 50, 20190501000000, public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_03(self):
        """ 获取佣金明细 币种信息为空"""
        eq = user_platform.detailed_commission('', 20190601000000, 1, 50, 20190801000000, public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_04(self):
        """ 获取佣金明细 页码为0"""
        eq = user_platform.detailed_commission('BTC', 20190601000000, 0, 50, 20190801000000, public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')


class Test18RechargeCoinRecord(unittest.TestCase):
    def test_01(self):
        """获取所有记录"""
        eq = user_platform.recharge_coin_record(record_type=1, page_index=10, page_count=10, token=public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_02(self):
        """获取冲币记录"""
        eq = user_platform.recharge_coin_record(record_type=2, page_index=10, page_count=10, token=public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')

    def test_03(self):
        """获取提币记录"""
        eq = user_platform.recharge_coin_record(record_type=3, page_index=10, page_count=10, token=public_token)
        self.assertEqual(eq['Result']['Msg'], '成功')


class Test19ExtractCoin(unittest.TestCase):
    def test_01(self):
        """提币"""
        pass


if __name__ == '__main__':
    unittest.main(verbosity=2)
