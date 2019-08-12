# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/26 22:34
import datetime
from random import choice

from sqlalchemy.sql import and_
from flask_wtf.file import FileRequired, FileAllowed
from wtforms.fields import simple
from wtforms import IntegerField,FieldList
from wtforms.form import Form
from wtforms import validators
from werkzeug.security import generate_password_hash
from wtforms.compat import iteritems
from flask import current_app

from .model import User
from globals.before_request import token
from utils.optional import Optional


class UserForm(Form):
    userName = simple.StringField(
        label="用户名",
        validators=[
            validators.DataRequired(message="用户名必须填写!"),
            validators.length(min=6,max=20,message="用户名应在6-20位之间!")
        ],
    )
    pwd = simple.PasswordField(
        label="密码",
        validators=[
            validators.DataRequired(message="密码不能为空"),
            validators.Regexp('^(?:(?=.*[A-Za-z])(?=.*[0-9])).{5,}$',message='密码应最少6位,由字母和数字的组成!')
        ]
    )
    nickName=simple.StringField(
        label='昵称',
        validators=[
            validators.DataRequired(message="昵称必须填写!"),
            validators.length(max=20, message="用户名不得大于20位!")
        ]
    )

    def validate_userName(self,userName):
        if  User.query.filter(User.userName==userName.data).first():
            raise validators.StopValidation("用户已被注册!")




class LoginPwdForm(Form):
    userName = simple.StringField(
        label="用户名",
        validators=[ validators.length(min=6, max=20, message="用户名应在6-20位之间!"),
                     validators.DataRequired(message="用户名必须填写!"),
                     ],)
    pwd = simple.PasswordField(
        label="密码",
        validators=[ validators.Regexp('^(?:(?=.*[A-Za-z])(?=.*[0-9])).{5,}$', message='密码应最少6位,由字母和数字的组成!'), validators.DataRequired(message="密码不能为空"),
        ]
    )

class LoginEmailForm(Form):
    email = simple.StringField(
        label='邮箱',
        validators=[validators.Length(8, 64, message='邮箱格式不正确'),
                    validators.DataRequired(message="邮箱必须填写!"),
                    validators.Email(message='这不是一个正确的邮箱格式'),])
    code = simple.StringField(
        label='验证码',
        validators=[validators.Length(6, 6, message='验证码不正确'),
                    validators.DataRequired(message="验证码未填写!"),
                    ])


class EmailForm(Form):
    """发送邮箱验证码form"""
    user = simple.StringField(
        label='用户')
    email = simple.StringField(
        label='邮箱',
        validators=[validators.Length(8, 64, message='邮箱格式不正确'),
                    validators.DataRequired(message="邮箱必须填写!"),
                    validators.Email(message='这不是一个正确的邮箱格式'),])


    def validate_email(self,email):
        self.user.data=User.query.filter(and_(User.email==email.data,User.is_email)).first()
        if not self.user.data:
            raise validators.StopValidation("邮箱用户不存在!")


class PwdForm(Form):


    """修改密码form"""
    pwd = simple.PasswordField(
        label="密码",
        validators=[validators.Regexp('^(?:(?=.*[A-Za-z])(?=.*[0-9])).{5,}$', message='密码应最少6位,由字母和数字的组成!'),
                    validators.DataRequired(message="原始密码不能为空!"),
                    ]
    )
    newPwd = simple.PasswordField(
        label="密码",
        validators=[validators.Regexp('^(?:(?=.*[A-Za-z])(?=.*[0-9])).{5,}$', message='新密码应最少6位,由字母和数字的组成!'),
                    validators.DataRequired(message="新密码不能为空!"),
                    ]
    )
    repeatPwd = simple.PasswordField(
        label="密码",
        validators=[validators.Regexp('^(?:(?=.*[A-Za-z])(?=.*[0-9])).{5,}$', message='密码应最少6位,由字母和数字的组成!'),
                    validators.DataRequired(message="请重复输入新密码!"),
                    ]
    )

    def validate_pwd(self,pwd):
        if  not token.user.check_password(pwd.data):
            raise validators.StopValidation('原始密码输入错误!')



    def validate_newPwd(self,newPwd):
        if newPwd.data!=self.repeatPwd.data:
            raise validators.StopValidation('新密码两次输入不一致!')
        elif newPwd.data==self.pwd.data:
            raise validators.StopValidation('新密码与原始密码相同!')
        self.newPwd.data = generate_password_hash(newPwd.data)


class UserInfoForm(Form):
    """修改个人资料form"""
    birth=simple.StringField(
        label='生日',
        validators=[Optional(),]
    )
    email = simple.StringField(
        label='邮箱',
        validators=[Optional(),
                    validators.Length(8, 64, message='邮箱格式不正确'),
                    validators.Email(message='这不是一个正确的邮箱格式'), ])
    sex=simple.StringField(
        label='性别',
        validators=[
            Optional()
                    ]
    )
    area=FieldList(simple.StringField('code'),
                   validators=[Optional()])
    nickName = simple.StringField(
        label='昵称',
        validators=[
            validators.length(max=20, message="用户名不得大于20位!")
        ]
    )
    portrait=simple.FileField(
        label='头像',
        validators=[
            Optional(),
            validators.URL(message='请传入一个有效的图片地址!')
        ]
    )
    province=simple.StringField()
    city=simple.StringField()
    home=simple.StringField()

    def validate_email(self,email):
        if email.data:
            user=User.query.filter(User.email==email.data).first()
            if user:
                raise validators.StopValidation('邮箱已被注册!')

    def validate_sex(self,sex):
        if sex.data is not None:
            if sex.data=='男':
                self.sex.data=1
            elif sex.data=='女':
                self.sex.data=0
            else:
                raise validators.StopValidation("性别输入不正确!")

    def validate_birth(self,birth):
        if birth.data:
            try:
                datetime.datetime.strptime(birth.data,'%Y-%m-%d')
            except:
                raise validators.StopValidation('生日输入错误!')

    def validate_area(self,area):
        if area.data:
            lis=['province','city','home']
            for h,i in zip(lis,area.data):
                if not isinstance(i,dict):
                    raise validators.StopValidation('地区输入不正确!')
                try:
                    self[h].data=i['code']
                except:
                    raise validators.StopValidation('地区输入不正确')
    @property
    def data(self):
        return dict((name, f.data) for name, f in iteritems(self._fields) if f.data is not None)



class UploadForm(Form):
    """上传接口form"""
    file = simple.FileField('file', validators=[FileRequired(),
                                    FileAllowed(['jpg','jpeg','png','gif'])])
