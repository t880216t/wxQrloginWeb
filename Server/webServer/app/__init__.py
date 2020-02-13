#-*-coding:utf-8-*-
from flask import Flask
from datetime import timedelta

app = Flask(__name__,static_url_path='/c2hApi/static')
app.config['UPLOAD_FOLDER'] = '/static/uploads/'
app.config['DOMAIN'] = ''
app.config['AppID'] = ''
app.config['AppSecret'] = ''
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif','HTML','html','xlsx'])
app.config['SECRET_KEY']= "thisisaverycoolttttpalt" #设置为24位的字符,每次运行服务器都是不同的，所以服务器启动一次上次的session就清除。
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(days=1) #设置session的保存时间。
app.config['KEY'] = 'bHBxsLYz' # id加密秘钥

'''
数据库对象创建
'''
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1:3306/c2h?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_POOL_TIMEOUT"] = 15
app.config["SQLALCHEMY_POOL_RECYCLE"] = 3000
db = SQLAlchemy(app)

'''
Redis配置
'''
app.config['REDIS_HOST'] = "127.0.0.1" # redis数据库地址
app.config['REDIS_PORT'] = 6379 # redis 端口号
app.config['REDIS_DB'] = 0 # 数据库名
app.config['REDIS_EXPIRE'] = 60 # redis 过期时间60秒

'''
注册蓝图
'''

from .auth.login import login
app.register_blueprint(login, url_prefix='/webApi/login')

from .auth.user import user
app.register_blueprint(user, url_prefix='/webApi/user')