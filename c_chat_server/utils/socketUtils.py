# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/8/4 17:00
from flask import current_app,request

from collections import Mapping
from functools import wraps
import six


def get_room_name(self:int,friend:int)->str:
    """获取房间名称"""
    if not isinstance(self,int) or not isinstance(friend,int):
        try:
            self=int(self)
            friend=int(friend)
        except:
            raise Exception(f'{self}&{friend}必须是一个数字!')
    return f'{self if self>friend else friend}_{self if self<friend else friend}'


class SocketViewMeta(type):
    """scoketio视图"""

    @classmethod
    def options(cls,bases,attrs):
        deco=attrs.get('method_decorators')
        for key, value in attrs.items():
            if key.startswith('SOCKET_'):
                if isinstance(deco, Mapping):
                    decorators = deco.get(key, [])
                else:
                    decorators = deco
                for decorator in decorators:
                    value = decorator(value)
                attrs[key] = value
        return attrs

    def __new__(cls, name, bases, attrs):
        new_attrs = cls.options(bases, attrs)
        return super().__new__(cls, name, bases, new_attrs)


@six.add_metaclass(SocketViewMeta)
class SocketView(object):
    ...


# 保存socketio的sid,user_id映射
class SocketRedis(object):
    key='socketMap'

    @classmethod
    def set(cls,user:dict):
        """存储socket的映射"""
        current_app.redis.hset(cls.key,request.sid,user)

    @classmethod
    def get(cls):
        return current_app.redis.hget(cls.key,request.sid)

class FriendRoomUtil(object):

    @staticmethod
    def get_room(id):
        return f'c_{id}'
