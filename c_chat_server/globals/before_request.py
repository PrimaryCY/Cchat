# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/18 10:47
import uuid
from functools import wraps
import json

from flask.globals import LocalProxy,partial,_request_ctx_stack,_lookup_req_object
from flask import session,request,current_app,make_response

from globals.globals_manage import gb
from apps.user.token import Token
from apps.user.model import User,AnonyMous
from c_chat_server.constant import RET,error_map
from utils.socketUtils import SocketRedis

class O:
    ...


@gb.before_app_request
def authorization():
    user_token=request.headers.get('tk')
    if not user_token:
        t=AnonyMous()
    else:
        userInfo=Token.unpackTk(current_app.config,user_token)
        if not userInfo:
            print('userinfo,',userInfo)
            response=make_response(json.dumps({'code':RET.TOKENERR,'msg':error_map[RET.TOKENERR],'data':'1'},ensure_ascii=False))
            response.delete_cookie('tk')
            return response
        t=User.query.filter(User.userName==userInfo['userName']).first()
        t.user=t
        t.pre='user'
    ctx = _request_ctx_stack()
    ctx.token = t



#socket权限验证
def SocketAuth(func):
    @wraps(func)
    def wrap(self,*args,**kwargs):
        t=SocketRedis.get()
        if not t:
            return {'code': RET.TOKENERR, 'msg': error_map[RET.TOKENERR], 'data': '1'}
        ctx = _request_ctx_stack()
        ctx.token = json.loads(t)
        return func(self,*args,**kwargs)
    return wrap


token = LocalProxy(partial(_lookup_req_object,'token'))
