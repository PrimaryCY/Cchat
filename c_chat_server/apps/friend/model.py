# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/30 12:44
import enum

from sqlalchemy import or_

from c_chat_server.extensions import db
from utils.baseModel import BaseModel
from globals.before_request import token


class FriendsStrategy(BaseModel,db.Model):
    """添加好友策略"""
    __tablename__='friends_strategy'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(126),comment='添加好友策略')
    user=db.relationship('User',backref='friends_strategy',lazy='dynamic')


class chatFriendGroup(BaseModel,db.Model):
    """好友分组表"""
    __tablename__='chat_friend_group'
    id=db.Column(db.Integer,primary_key=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),comment='用户')
    name=db.Column(db.String(126),comment='好友分组组名')
    group_users=db.relationship('ChatFriend',backref='group',lazy='dynamic')
    

class ChatFriend(BaseModel,db.Model):
    """好友审核表"""
    __tablename__='chat_friend'

    class ChatFriendStatus(enum.Enum):
        """审核状态"""
        NOT_PASS=0
        PASS=1
        WAIT=2
        LOSE=3

    id=db.Column(db.Integer,primary_key=True)
    self_id=db.Column(db.Integer,index=True,comment='自己')
    friend_id=db.Column(db.Integer,index=True,comment='好友')
    status=db.Column(db.SmallInteger,default=2,comment='审核状态')
    remark=db.Column(db.String(126),comment='名称备注')
    top=db.Column(db.Boolean,default=False,comment='置顶')
    become_friends_time=db.Column(db.DATETIME,comment='成为好友的时间')
    group_id=db.Column(db.Integer,db.ForeignKey('chat_friend_group.id'),comment='分组')
    room=db.Column(db.String(126),comment='房间名称')
    initiator_id=db.Column(db.Integer,comment='发起人')

    @staticmethod
    def get_friends_id():
        """获取好友字典"""
        friends=db.session.query(ChatFriend.friend_id,ChatFriend).filter(
            ChatFriend.self_id == token.id,
            ChatFriend.is_active==True,
            ChatFriend.status==1).all()
        return {str(i[0]):i[1].to_dict() for i in friends}

    @staticmethod
    def check_is_friend(friend_id):
        if db.session.query(ChatFriend).filter(ChatFriend.self_id==token.id,
                                            ChatFriend.friend_id==friend_id,
                                            ChatFriend.is_active==True,
                                            ChatFriend.status==1).first():
            return True
        return False



class FriendsMessage(BaseModel,db.Model):
    """消息表"""
    __tablename__='friends_message'

    class FriendMsgStatus:
        """阅读状态"""
        markRead=0
        unRead=1

    id=db.Column(db.Integer,primary_key=True)
    msg=db.Column(db.String(126),comment='聊天记录')
    type=db.Column(db.SmallInteger,default=1,comment='类型')
    from_user_id=db.Column(db.Integer,index=True,comment='发送者')
    to_user_id=db.Column(db.Integer,index=True,comment='接收者')
    status=db.Column(db.SmallInteger,default=1,comment='接收状态')
    room=db.Column(db.String(126),comment='房间名称')

    @staticmethod
    def get_history_message(room):
        """获取单个好友的历史消息"""
        return db.session.query(FriendsMessage).filter(FriendsMessage.room == room,
                                                or_(FriendsMessage.from_user_id == token.id,
                                                    FriendsMessage.to_user_id == token.id),
                                                       FriendsMessage.is_active==True) \
            .order_by(FriendsMessage.create_time.desc())
