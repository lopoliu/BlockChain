from services.vipServer import UserPlatform
from services.miscellaneousServer import ApiData


sever = UserPlatform()
api_data = ApiData()
#
# x = sever.register(invite_code='2FcMFg', only_phone=True)     # 进行流程测试时使用
#
user_info = sever.login_account(phone_number='13165188582')       # 13165188582
sever.get_sms(phone_number='17322311020')       # 向该号码发送一条短信
sever.real_name_auth(token=user_info['Token'])      # 实名认证
sever.set_price_password(token=user_info['Token'])  # 设置资金密码
sever.create_wallet(coin_id='BTC', token=user_info['Token'])       # 创建钱包
bank_dict = api_data.get_bank_dict(token=user_info['Token'], only_id=True)       # 获取银行字典
sever.bind_bank_card(bank_id=bank_dict[0], card_number='98278173800', bank_addr='中国深圳', price_password='a12345678',
                     card_owner='lopo', token=user_info['Token'])   # 绑定银行卡


