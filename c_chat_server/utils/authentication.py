# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/11 22:08
from functools import wraps

from flask import g

from c_chat_server.constant import RET,error_map
from globals.before_request import token




def afterLogin(view):
    """登陆后才可以访问"""
    @wraps(view)
    def wrap(*args,**kwargs):
        if token.pre == 'anonymous' :
            return {'code':RET.TOKENERR,'msg':error_map[RET.TOKENERR]}
        g.user=token.user
        return view(*args,**kwargs)
    return wrap

