# 调试模式是否开启
DEBUG = True
# session 必须要设置key
SECRET_KEY = 'data_science'
# mysql
SQLALCHEMY_TRACK_MODIFICATIONS = False
DIALECT = 'mysql'
DRIVER = 'pymysql'  # 连接数据库驱动
USERNAME = 'root'  # 用户名
PASSWORD = '123456'  # 密码
HOST = 'localhost'  # 服务器
PORT = '3306'  # 端口
DATABASE = 'data_sci'  # 数据库名
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT,
                                                                       DRIVER,
                                                                       USERNAME,
                                                                       PASSWORD,
                                                                       HOST,
                                                                       PORT,
                                                                       DATABASE)
