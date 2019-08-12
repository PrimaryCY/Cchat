# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/30 12:44
from urllib.parse import urljoin

from flask import url_for

from c_chat_server.extensions import db
from utils.baseModel import BaseModel

"""
聊天信息表(存mysql):{
room:聊天室名称,msg:聊天信息,id:用户id,time:发表时间
}

聊天室信息表(存mysql):{
room:聊天室名称,room_id:聊天室id
}

聊天室用户中间表(存mysql):{
room:聊天室名称,id:用户id
}

聊天室好友私聊表
a_id,b_id,is_active,room_name
"""


class ChatUserRoom(BaseModel,db.Model):
    """聊天室用户中间表"""
    __tablename__='user_chat_room'
    id=db.Column(db.Integer,primary_key=True)
    #user_id=db.Column(db.Integer, db.ForeignKey('user.id'),primary_key=True)
    user_id = db.Column(db.String(256), index=True)
    chat_room_id=db.Column(db.Integer, db.ForeignKey('chat_room.id'),index=True)
    is_create_user= db.Column(db.Boolean,default=False,comment='角色')


class ChatRoom(BaseModel,db.Model):
    """聊天室表"""
    __tablename__='chat_room'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),comment='聊天室名称',unique=True)
    create_user=db.Column(db.Integer,db.ForeignKey('user.id'),comment='创建人')
    img=db.Column(db.String(256),comment='聊天室封面图')
    desc=db.Column(db.String(512),comment='聊天室简介')
    #中间表中用户
    mid_users=db.relationship('ChatUserRoom',backref='chat_room',lazy='dynamic')
    #跨越中间表的用户
    # users=db.relationship('User',secondary='user_chat_room',
    #                          backref=db.backref('chat_rooms',lazy='dynamic'),lazy='dynamic',cascade='all')
    messages=db.relationship('ChatMessage',backref='room',lazy='dynamic')


    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.set_img()

    def set_img(self):
        """设置默认封面图"""
        if not self.img:
            urlFilePath=urljoin('static','default/roomDefault.jpg')
            self.img=url_for('static', _external=True, filename=urlFilePath)


class ChatMessage(BaseModel,db.Model):
    """聊天消息表"""
    __tablename__="chat_message"
    id=db.Column(db.Integer,primary_key=True)
    room_id=db.Column(db.Integer,db.ForeignKey('chat_room.id'),comment='信息发表房间')
    #user_id=db.Column(db.Integer,db.ForeignKey('user.id'),comment='信息发表人')
    user_id = db.Column(db.String(256), comment='信息发表人')
    msg=db.Column(db.String(256),comment='聊天信息')


