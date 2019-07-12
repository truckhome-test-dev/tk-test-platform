from test_code import *
from base_server import *
import hashlib


class Login():
    def __init__(self,username,password):
        self.username=username
        self.password=self.encryption_MD5(password)
        conf = configparser.ConfigParser()
        conf.read("conf/config.ini")
        self.db_qa = pymysql.connect(conf.get('qa', 'host'), conf.get('qa', 'user'), conf.get('qa', 'passwd'),
                                     conf.get('qa', 'database'), charset='utf8')
        self.db_mantis = pymysql.connect(conf.get('mantis_bug_db', 'host'), conf.get('mantis_bug_db', 'user'),
                                         conf.get('mantis_bug_db', 'passwd'),
                                         conf.get('mantis_bug_db', 'database'), charset='utf8')

    #MD5加密
    def encryption_MD5(self,data):
        hash_data=hashlib.md5()
        hash_data.update(data.encode(encoding='utf-8'))
        ret=hash_data.hexdigest()
        return ret

    #验证登录
    def valid_login(self):
        cur=self.db_mantis.cursor()
        sql="select * from mantis_user_table where username='%s'"%self.username
        cur.execute(sql)
        self.db_mantis.commit()
        self.db_mantis.close()
        data=cur.fetchone()
        if data:
            if self.password==data[4]:
                return data[1],data[7]
            else:
                return False
        else:
            return False

# login=Login("cuijinyue","360che")
# print(login.valid_login())