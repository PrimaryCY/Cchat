# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/18 14:01
import os
import string
import random
from random import choice
from urllib.parse import urljoin

from flask import request,current_app,url_for

from apps.user.model import User,db,AnonyMous
from apps.user.form import UserForm,LoginEmailForm,LoginPwdForm,EmailForm,\
    PwdForm,UserInfoForm,UploadForm
from apps.user.token import Token
from c_chat_server.constant import RET,error_map
from utils.tools import getFlatten,random_filename
from utils.authentication import afterLogin
from utils.resource import View
from globals.before_request import token


# 用户视图
class UserView(View):

    method_decorators = {
        'get': [],
        'put':[afterLogin]
    }

    def get(self):
        """
        *获取用户信息:
        *响应: {userName: '907031027', nickName: 'nick', email: '907031027@qq.com'}
        """
        if token.pre !='anonymous':
            return {'code':RET.OK,'msg':error_map[RET.OK],'data':token.user.to_dict()}
            # 匿名用户资料


        return {'code':RET.OK,'msg':error_map[RET.OK],'data':AnonyMous().to_dict()}


    def post(self):
        """
        * 注册用户:
        * 请求:{userName:'907031027',nickName:'xx',pwd:'1234567',checkPwd:'1234567'}
        * 响应:{token:'12345678'}
        """
        form=UserForm(data=request.json)
        if form.validate():
            user=User(**form.data)
            try:
                db.session.add(user)
                token=Token.encryptTk(current_app.config,user.to_dict())
                db.session.commit()
            except:
                db.session.rollback()
                return {'code': RET.SERVERERR, 'msg': error_map[RET.SERVERERR]}
            if not token:
                return {'code':RET.SERVERERR,'msg':error_map[RET.SERVERERR]}
            return {'code':RET.OK,'msg':'OK','data':{'token':token}}
        return {'code':RET.PARAMERR,'msg':getFlatten(form.errors.values())}

    def put(self):
        """
        * 修改用户个人信息
        * 请求:{area:[{code: "110000",name: "北京市"},{code: "110000",name: "朝阳区"},{code:"110000",name: "望京"}],birth: "1950-01-01",email: "907031027@qq.com",sex: "男"}
        * 响应:{完整用户信息}
        """
        form=UserInfoForm(data=request.json)
        if form.validate():
            try:
                for k,v in form.data.items():
                    setattr(token.user,k,v)
            except:
                db.session.rollback()
                return {'code':RET.SERVERERR,'msg':error_map[RET.SERVERERR]}
            db.session.commit()
            return  {'code':RET.OK,'msg':'OK','data':token.user.to_dict()}
        return  {'code':RET.PARAMERR,'msg':getFlatten(form.errors.values())}


#登录视图
class LoginView(View):
    method_decorators = {
        'delete': [afterLogin]
    }

    def post(self):
        """
        * 登录接口:
        * 请求:{email:'907031027@qq.com',code:'123456',username:'',pwd:'',type:1}
        * 响应:{token:'1234567890123',user:{完整用户信息}}
        """
        res = current_app.redis.get(self.login_error_key)
        if res and int(res) >= current_app.config['LOGIN_ACCESS_NUM']:
            return {'errno': RET.LOGINERR, 'msg': '密码输入次数过多,请十分钟之后重试'}

        js=request.json
        type=js.get('type')
        if type is None:
            return {'code':RET.PARAMERR,'msg':error_map[RET.PARAMERR]}
        #密码认证
        if type==0:
            form=LoginPwdForm(data=js)
            if not form.validate():
                return {'code': RET.PARAMERR, 'msg': getFlatten(form.errors.values())}

            user=User.query.filter(User.userName==form.userName.data).first()
            if not user:
                return {'code':RET.USERERR,'msg':'用户不存在!'}

            flag=user.check_password(form.pwd.data)

            if not flag:
                current_app.redis.incr(self.login_error_key)
                current_app.redis.expire(self.login_error_key, current_app.config['LOGIN_ERROR_TIME'])
                return {'code':RET.PARAMERR,'msg':'用户名或密码错误!'}

        #邮箱验证码验证
        elif type==1:
            form=LoginEmailForm(data=js)
            if not form.validate():
                return {'code': RET.PARAMERR, 'msg': getFlatten(form.errors.values())}
            user=User.query.filter(User.email==form.email.data).first()
            if not user:
                return {'code': RET.PARAMERR, 'msg': '用户名或验证码错误!'}
            code=current_app.redis.get(EmailView.pubilc_email_redis_key(user.userName))
            if not code:
                return {'code': RET.PARAMERR, 'msg': '用户名或验证码错误!'}
            if code!=form.code.data:
                return {'code': RET.PARAMERR, 'msg': '验证码错误!'}
            else:
                current_app.redis.delete(EmailView.pubilc_email_redis_key(user.userName))

        token = Token.encryptTk(current_app.config,user.to_dict())
        return  {'code':RET.OK,'msg':error_map[RET.OK],'data':{
            'token':token,
            'user':user.to_dict()
        }}


    @property
    def login_error_key(self):
        """同一台机器用户名密码输入次数过多,之间锁定该ip"""
        return f'access_{request.remote_addr}'

    def delete(self):
        """
        * 退出登录:
        * 响应:{code:'2000',msg:'ok'}
        """
        res=Token.deleteTk(current_app.config,token.user.to_dict())
        if not res:
            return {'code':RET.SERVERERR,'msg':error_map[RET.SERVERERR]}
        return {'code':RET.OK,'msg':error_map[RET.OK]}

#发送邮箱验证码
class EmailView(View):

    @staticmethod
    def pubilc_email_redis_key(userName):
        """获取邮箱redis的key"""
        return f'email_{userName}'

    @property
    def email_redis_key(self):
        """获取邮箱redis的key"""
        if not hasattr(self, '_redis_code'):
            self._redis_code = f'email_{self.user.userName}'
        return self._redis_code

    @property
    def generate_code(self):
        """生成邮箱验证码"""
        seeds = f"1234567890{''.join([string.ascii_uppercase[random.randrange(0,26)] for i in range(10)])}"
        random_str = []
        for i in range(6):
            random_str.append(choice(seeds))
        return "".join(random_str)


    def post(self):
        """
        * 获取邮箱验证码:
        * 请求:{email:'907031027@qq.com'}
        * 响应:{code:'2000',msg:'ok'}
        """
        from apps.user.task import send_mail
        form=EmailForm(data=request.json)
        if form.validate():
            self.user=form.data['user']
            if current_app.redis.get(self.email_redis_key):
                timeRemaining = current_app.redis.ttl(self.email_redis_key)
                return {'code':RET.PARAMERR,'msg':f'{timeRemaining}秒后才可以重新发送邮箱验证码'}

            code=self.generate_code
            current_app.redis.setex(self.email_redis_key,
                                    current_app.config['MAIL_VERIFY_EXPIRE'],code)
            send_mail.delay(self.user.email, code)
            return {'code':RET.OK,'msg':error_map[RET.OK]}
        return {'code':RET.PARAMERR,'msg':getFlatten(form.errors.values())}

#修改密码
class PwdView(View):
    method_decorators = {
        'put':[afterLogin]
    }

    def put(self):
        """
        *修改密码:
        *请求:{pwd:'12345678',newPwd:'1111111','repeatPwd':'11111111'}
        *响应:{code:'2000',msg:'ok'}
        """
        form=PwdForm(data=request.json)
        if form.validate():
            try:
                token.user.pwd=form.newPwd.data
                db.session.commit()
            except:
                db.session.rollback()
                return {'code':RET.SERVERERR,'msg':error_map[RET.SERVERERR]}
            return {'code':RET.OK,'msg':error_map[RET.OK]}
        return {'code': RET.PARAMERR, 'msg': getFlatten(form.errors.values())}


class UploadView(View):


    def post(self):
        """
        * 上传文件接口
        * 请求:{file:文件对象}
        * 响应:{'code':2000,'msg':'ok',url:文件存储后的url}
        """
        form=UploadForm(request.files)
        if not form.validate():
            return {'code':RET.PARAMERR,'msg':getFlatten(form.errors.values())}
        f = form.file.data
        filename = random_filename(f.filename)

        Path=os.path.join(current_app.static_folder, 'upload')
        if not os.path.isdir(Path):
            os.makedirs(Path)
        filePath=os.path.join(Path,filename)
        f.save(filePath)

        #url中文件的路径
        urlFilePath=urljoin('upload/',filename)
        return {'code':RET.OK,'msg':'ok','url':url_for('static',_external=True,filename=urlFilePath)}
