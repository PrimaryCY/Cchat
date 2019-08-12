# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/18 14:08
from flask import current_app,request
from werkzeug.security import generate_password_hash,check_password_hash
from sqlalchemy import String,Integer,DATE,Boolean,Column,ForeignKey,SmallInteger
from sqlalchemy_utils import ChoiceType

from c_chat_server.extensions import db
from utils.baseModel import BaseModel


class AnonyMous:
    userName='匿名'
    portrait='https://img.yzcdn.cn/vant/cat.jpeg',
    pre = 'anonymous'

    @property
    def id(self):
        return request.remote_addr

    def to_dict(self):
        return {'userName': '匿名',
                'portrait': 'https://img.yzcdn.cn/vant/cat.jpeg',
                'id': self.id,
                'pre':'AnonyMous'
                }

    @property
    def platform(self):
        ua = request.user_agent.platform or ''
        if 'android' in ua or 'Linux' in ua:
            return 0
        elif 'iphone' in ua:
            return 1
        else:
            return 2


#角色权限中间表
roles_permissions = db.Table('roles_permissions',
                             db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
                             )


class User(BaseModel,db.Model):
    """用户表"""
    __tablename__='user'

    USER_SEX = (
        (0, 'women'),
        (1, 'man'),
        (2, 'secrecy')
    )
    id=db.Column(Integer,primary_key=True)
    userName=db.Column(String(64),nullable=False,unique=True,comment='用户名')
    pwd=db.Column(String(256),nullable=False,comment='密码')
    nickName=db.Column(String(64),nullable=False,comment='昵称')
    #需手动修改migrate表文件
    sex = db.Column(ChoiceType(USER_SEX, SmallInteger()), comment='性别',default=2)
    birth=db.Column(DATE,comment='生日')
    portrait=db.Column(String(256), comment='头像',nullable=False)
    email=db.Column(String(128),unique=True,comment='邮箱')
    is_email=db.Column(Boolean,comment='认证邮箱',default=False)
    province=db.Column(String(64),comment='省份')
    city=db.Column(String(64),comment='城市')
    home=db.Column(String(64),comment='地区')
    role_id=db.Column(Integer,db.ForeignKey('role.id'))
    friends_strategy_id=db.Column(db.Integer,db.ForeignKey('friends_strategy.id'),comment='添加好友策略')


    #用了back_populates,另一张表也必须指明!
    role = db.relationship('Role', back_populates='users',lazy='joined')
    # #我的反馈
    feedback=db.relationship('Feedback',lazy='dynamic',backref=db.backref('user',lazy='joined'))
    #我的反馈回复
    feedbackReply=db.relationship('FeedbackReply',lazy='dynamic',backref=db.backref('user',lazy='joined'))
    #我创建的聊天室
    MychatRooms=db.relationship('ChatRoom',lazy='dynamic',backref='founder')

    # from apps.friend.model import ChatFriend
    # # 我的所有好友
    # friends=db.relationship('ChatFriend',lazy='dynamic',backref='user',
    #                         foreign_keys='ChatFriend.self_id')

    #lazy="dynamic",懒加载,用到时才会去查询
    #lazy="select",直接查询
    #lazy="joined",连表查询
    #lazy="subquery": 与joined类似，但使用子子查询
    #db.backref('_class',lazy="dynamic"), lazy="dynamic")
    #areas = db.relationship("Area", backref="users", secondary=user_area,lazy='dynamic')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.set_role()
        self.set_portrait()
        self.password_hash=self.pwd

    def __repr__(self):
        return self.userName

    @property
    def platform(self):
        ua = request.user_agent.platform or ''
        if 'android' in ua or 'Linux' in ua:
            return 0
        elif 'iphone' in ua:
            return 1
        else:
            return 2


    @property
    def is_admin(self):
        return self.role.name == 'Administrator'

    @property
    def password_hash(self):
        raise AttributeError('only setter attribute')

    @password_hash.setter
    def password_hash(self,value):
        self.pwd=generate_password_hash(value)

    def check_password(self,pwd):
        return check_password_hash(self.pwd,pwd)

    def to_dict(self,values=None):
        data=super().to_dict(values)
        data.pop('pwd')
        data['pre']='user'
        return data

    def set_role(self):
        """设置默认角色"""
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()

    def set_portrait(self):
        """设置默认头像"""
        if not self.portrait:
            self.portrait = 'https://img.yzcdn.cn/vant/cat.jpeg'

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and permission in self.role.permissions



class Permission(BaseModel,db.Model):
    """权限"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True,comment='权限名称')
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions',lazy='joined')



class Role(BaseModel,db.Model):
    """角色"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True,comment='角色名称')
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=roles_permissions,back_populates='roles')

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'Locked': ['FOLLOW'],                       #被封禁用户只可以登录
            'User': ['FOLLOW', 'COLLECT',],             #普通用户可以登录,添加好友
            'Moderator': ['FOLLOW', 'COLLECT',  'MODERATE'],
            'Administrator': ['FOLLOW', 'COLLECT', 'COMMENT',  'MODERATE', 'ADMINISTER']
        }

        for role_name in roles_permissions_map:
            role = Role.query.filter(Role.name==role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()
