# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/7 18:42
import os
from collections import Mapping
from concurrent.futures import ThreadPoolExecutor

import redis
from pymongo import MongoClient

from utils.converters import ReConverters


class BaseSetting(object):

    @classmethod
    def init_app(cls,app):
        try:
            from c_chat_server import local_setting
            for setting in dir(local_setting):
                if setting.isupper():
                    sett = getattr(local_setting, setting)
                    if isinstance(sett,Mapping):
                        cls.__dict__[setting].update(sett)
                    elif isinstance(sett,(list,tuple,set)):
                        cls.__dict__[setting]+=sett
                    else:
                        setattr(cls, setting, sett)
        except ImportError:
            pass

        app.config.from_object(cls)
        app.redis=app.config.get('COMMON_REDIS',None)
        app.mongo=app.config.get('COMMON_MONGO',None)

        if hasattr(cls,'CONVERTERS'):
            app.url_map.converters.update(cls.CONVERTERS)


class Setting(BaseSetting):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    #sqlalchemy连接数据库
    SQLALCHEMY_DATABASE_URI= 'mysql://root:oracle@127.0.0.1:3306/c_chat?charset=utf8'
    #sqlalchemy测试数据库
    TEST_SQLALCHEMY_DATABASE_URI= 'mysql://root:oracle@127.0.0.1:3306/flask_test?charset=utf8'
    # 动态追踪修改设置，如未设置只会提示警告
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    #查询时会显示原始SQL语句
    SQLALCHEMY_ECHO = False
    #数据库连接池的大小。默认是数据库引擎的默认值 （通常是 5）。
    SQLALCHEMY_POOL_SIZE = 10
    #超过连接池大小后最多还可以增加几个链接
    SQLALCHEMY_MAX_OVERFLOW = 5
    #可以省去db.session.commit()的操作
    #SQLALCHEMY_COMMIT_ON_TEARDOWN=True
    CONVERTERS={
        're':ReConverters
    }


    #cookies是否签名
    SESSION_USE_SIGNER=True
    SESSION_KEY_PREFIX='c_chat_server'
    #session过期时间
    PERMANENT_SESSION_LIFETIME=7*24*60*60


    REDIS_HOST='127.0.0.1'
    REDIS_PORT=6379
    REDIS_POOL = redis.ConnectionPool(host='127.0.0.1', port=6379,db=7, max_connections=10,
                                      decode_responses=True)
    COMMON_REDIS = redis.StrictRedis(connection_pool=REDIS_POOL)
    COMMON_MONGO=MongoClient(host='127.0.0.1',port=27017,connect=True)


    """token配置"""
    TOKEN_REDIS_POOL = redis.ConnectionPool(host='127.0.0.1', port=6379, db=6, max_connections=10,
                                            decode_responses=True)
    TOKEN_REDIS = redis.StrictRedis(connection_pool=TOKEN_REDIS_POOL)
    TOKEN_SECURITY_KEY=b'pBy0j5_m6qqTOXElHSs0OlfV5qiYhqHkEvwLtdrXZ5o='

    """邮件设置"""
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_USE_SSL = True
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_DEFAULT_SENDER= '907031027@qq.com'
    MAIL_VERIFY_EXPIRE = 5 * 60


    CELERY = {'CELERY_INCLUDE':
                  ('apps.user.task',),
              'CELERY_BROKER_URL': 'redis://127.0.0.1:6379/12',
              'CELERY_RESULT_BACKEND': 'redis://127.0.0.1:6379/13',
              }


    #解决flask_restful返回时中文字符变成unicode编码问题
    RESTFUL_JSON = dict(ensure_ascii=False)
    #解决jsonify返回中文字符变成unicode编码问题
    JSON_AS_ASCII = True



    # 登录失败锁定时常
    LOGIN_ERROR_TIME = 600
    # 登录失败次数
    LOGIN_ACCESS_NUM = 10

    #serializer线程池对象
    SERIALIZER_THREAD_POLL=ThreadPoolExecutor(10)



class DevSetting(Setting):
    DEBUG=True
    REDIS_HOST = '127.0.0.1'
    REDIS_PORT = 6379



class ProductionSetting(Setting):
    REDIS_HOST = None
    REDIS_PORT = None
    DEBUG=False



SETTING_MAPPING={
    'development':DevSetting,
    'production':ProductionSetting
}
