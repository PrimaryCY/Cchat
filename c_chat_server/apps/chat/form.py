# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/8/2 23:15
import re
import string

from wtforms.fields import simple
from wtforms import validators

from apps.chat.model import ChatRoom
from c_chat_server.extensions import db
from utils.serializer import BaseForm
from utils.optional import Optional


class CreateChatRoomForm(BaseForm):
    """创建聊天室form"""
    name=simple.StringField(
        label='聊天室名称',
        validators=[
            validators.DataRequired(message='聊天室名称必须填写!'),
            validators.length(max=10,message='聊天室名称应小于10字')
        ]
    )

    desc=simple.StringField(
        label='聊天室简介',
        validators=[
            validators.DataRequired(message='聊天室简介必须填写!'),
            validators.Length(max=512,message='聊天室简介应小于512字')
        ]
    )

    img=simple.StringField(
        label='聊天室封面图片',
        validators=[
            Optional(),
        ]
    )

    def validate_name(self,name):
        word_list = string.punctuation
        for i in word_list:
            if i in name.data:
                raise validators.StopValidation('聊天室名称不能带有特殊字符!')
        queryset=db.session.query(ChatRoom.id).filter(ChatRoom.name==name.data).first()
        if queryset:
            raise validators.StopValidation('聊天室名称已经被抢先注册了!')


    def validate_img(self,images):
        if images.data:
            if not re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',images.data):
                raise validators.StopValidation('图片不符合规则!')