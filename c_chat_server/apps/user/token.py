# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/26 23:50
from collections import Mapping

import msgpack
from cryptography.fernet import Fernet, InvalidToken
from typing import Union
from flask import request


class Token(object):

    #token存入redis中的唯一标识
    key='userName'

    def __init__(self,config:dict):

        assert config.get('TOKEN_SECURITY_KEY'), (
            '未设置TOKEN_SECURITY_KEY!'
        )
        self.security_key = config.get('TOKEN_SECURITY_KEY')

        if config.get('TOKEN_REDIS'):
            #设置token过期时间,默认七天
            self.expires=config.get('TOKEN_EXPIRES',7*24*3600)
            self.redis=config.get('TOKEN_REDIS')

        self.conf=config


    @property
    def redis_key(self):
        """获取redis中存入的key名"""
        if not hasattr(self, '_redis_key'):
            ua=request.user_agent.platform or ''
            if 'android'in ua or 'Linux' in ua:
                self._redis_key=f'tk_android_{self.data.get(self.key)}'
            elif 'iphone' in ua:
                self._redis_key=f'tk_ios_{self.data.get(self.key)}'
            else:
                self._redis_key=f'tk_pc_{self.data.get(self.key)}'
        return self._redis_key

    @property
    def token(self):
        """获得加密实例"""
        if not hasattr(self, '_token'):
            self._token = Fernet(self.security_key)
        return self._token

    def _generate_token(self)->str:
        """生成token"""
        wait_token=msgpack.dumps(self.data)
        return (self.token.encrypt(wait_token)).decode()[::-1]


    def _encryptTk(self,data:Mapping)-> Union[str,bool]:
        """
        加密token
        """
        assert isinstance(data, Mapping), (
            "data必须是一个字典类型|类字典类型的数据"
        )
        self.data = dict(data)
        token=self._generate_token()
        if self.redis:
            assert data.get(self.key, None), (
                '传入的属性必须要有唯一标识属性ID!')
            res=self.redis.setex(self.redis_key,self.expires,token)
            if not res:return False
        return token


    def _deleteTk(self,data:Mapping)->bool:
        """删除token"""
        if self.redis:
            self.data=data
            return self.redis.delete(self.redis_key)

    def _unpackTk(self,token:str)->Union[dict,bool]:
        """
        :return:dict
        """
        try:
            bytes_user_info=self.token.decrypt(token.encode()[::-1])
            user_info=msgpack.loads(bytes_user_info,encoding='utf8')
        except InvalidToken:
            return False
        except Exception as ex:
            raise ex

        if self.redis:
            self.data=user_info
            res=self.redis.get(self.redis_key)
            if not res:
                return False
            elif res!=token.replace(' ',''):
                return False
        return user_info

    @classmethod
    def encryptTk(cls, config: dict, data: Mapping) -> Union[str, bool]:
        """
        加密接口
        :param config:配置文件,dict形式
        :param data: 类字典或者字典形式对象
        :return: 加密成功返回token,
                 加密失败返回false布尔值
        """
        return cls(config)._encryptTk(data)

    @classmethod
    def unpackTk(cls, config: dict, token: str) -> Union[dict, bool]:
        """
        解密接口
        :param config: 配置文件,dict形式
        :param token: token字符串
        :return: 解密成功返回user对象
                 解密失败返回false布尔值
        """
        return cls(config)._unpackTk(token)

    @classmethod
    def deleteTk(cls, config: dict, data: Mapping)->bool:
        """
        删除redis中token
        :param config:配置文件,dict形式
        :param data: 映射对象,主要是寻找redis-key使用
        :return: 布尔值
        """
        return cls(config)._deleteTk(data)
