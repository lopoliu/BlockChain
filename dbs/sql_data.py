import pymysql


class MySql(object):
    def __init__(self):
        conn = pymysql.connect(host='192.168.28.25', user='root', password='tljs@123', database='user_db', port=3306)
        self.cursor = conn.cursor()

    def send_number(self):
        """ 从数据库中获取一个可接收短信的用户 """
        sql: str = "select sms.phone_number from " \
                   "user_db.veri_code_count_infos as sms left join user_db.user_infos as user " \
                   "on sms.phone_number = user.phone_number " \
                   "where user.password='X/QPfQSG0lX3Nq5iUQWTDQ==' and sms.count < 10 and " \
                   "length(sms.phone_number) = 11 order by sms.phone_number desc "

        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        phone_number, *ignore = data
        return phone_number

    def send_count_is_10(self):
        """ 获取一条剩余短信次数为10次的账户 """
        sql: str = "select phone_number from `veri_code_count_infos` where `count`<10"
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        phone_number, *ignore = data
        return phone_number

    def not_real_name_user(self):
        """ 获取一个没有实名的手机号并且要求账户密码未zxc123.."""
        sql: str = "select phone_number " \
                   "from user_db.user_infos " \
                   "where is_real_check = 2 " \
                   "and password='X/QPfQSG0lX3Nq5iUQWTDQ=='"
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        phone_number, *ignore = data
        return phone_number

    def my_phone(self):
        """ 获取一个密码为zxc123..的手机号码 """
        sql: str = "select phone_number from user_db.user_infos where password='X/QPfQSG0lX3Nq5iUQWTDQ=='"
        self.cursor.execute(sql)
        data = self.cursor.fetchone()
        phone_number, *ignore = data
        return phone_number


if __name__ == '__main__':
    x = MySql()
    p = x.my_phone()
    print(p)
