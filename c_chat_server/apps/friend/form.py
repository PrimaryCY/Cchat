# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/8/9 17:17
import re

from wtforms.fields import simple,IntegerField,FieldList,SelectField,StringField
from wtforms import validators

from apps.user.model import User
from apps.friend.model import ChatFriend
from c_chat_server.extensions import db
from utils.serializer import BaseForm
from globals.before_request import token
from utils.optional import Optional


class CreateFriendForm(BaseForm):
    """添加好友form"""
    friend_id=IntegerField(
        label='好友id',
        validators=[
            validators.DataRequired(message='必须选择好友!')
        ]
    )

    def validate_friend_id(self,friend):
        if friend.data==token.id:
            raise validators.StopValidation('参数传递错误!')
        friend_name = db.session.query(User.userName).filter(User.id == friend.data).scalar()
        if not friend_name:
            raise validators.StopValidation('不存在此用户')
        self.friend_name=friend_name


class CheckFriendForm(BaseForm):
    """审核好友form"""
    id=IntegerField(
        label='好友审核表id',
        validators=[
            validators.DataRequired(message='参数错误!')
        ]
    )
    status=IntegerField(
        label='审核结果',
        validators=[
            validators.DataRequired(message='参数错误'),
            validators.AnyOf([1,3],message='参数传递错误!')
        ]
    )

class FriendMsgForm(BaseForm):
    msg = simple.StringField(
        label="消息",
        validators=[
            validators.DataRequired(message="消息必须填写!"),
        ],
    )
    type = IntegerField(
        label='消息类型',
        validators=[
            validators.DataRequired(message='参数错误!')
        ]
    )

    to_user_id = IntegerField(
        label='接收方',
        validators=[
            validators.DataRequired(message='参数错误!')
        ]
    )
    status = IntegerField(
        label='状态',
        default=1,
        validators=[
           Optional()
        ]
    )
    room = simple.StringField(
        label="房间号",
        validators=[
            validators.DataRequired(message="房间号必须填写!"),
        ],
    )

    def validate_to_user_id(self,to_user_id):
        if not ChatFriend.check_is_friend(to_user_id.data):
            raise validators.StopValidation('不存在的好友!')
