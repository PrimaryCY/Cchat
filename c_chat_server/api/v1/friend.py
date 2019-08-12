# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/8/8 16:37
import datetime
import json

from flask import current_app,request,url_for
from sqlalchemy import func, and_, distinct, or_
from sqlalchemy.sql import func
from flask_socketio import emit, join_room, disconnect, leave_room,send,rooms

from utils.authentication import afterLogin
from utils.tools import  getFlatten,sort_pinyin
from utils.socketUtils import get_room_name
from globals.before_request import token,SocketAuth
from c_chat_server.constant import RET,error_map
from utils.socketUtils import SocketView,FriendRoomUtil
from utils.resource import ApiView, View
from apps.friend.model import *
from apps.friend.form import CreateFriendForm,CheckFriendForm
from apps.user.model import User
from apps.friend.model import FriendsMessage,ChatFriend
from apps.friend.form import FriendMsgForm


class FriendSocketView(SocketView):
    method_decorators = [SocketAuth]

    def SOCKET_SEND_MSG(self,data):
        """发送消息"""
        msg=FriendsMessage(msg=data['msg'],#消息
                           from_user_id=token['id'],#发送方
                           to_user_id=data['to_user_id'],#接收方
                           type=data['type'],#消息类型
                           status=0)#消息状态
        db.session.add(msg)
        db.session.commit()

        #从redis中查询该用户登录之后所有加入过的房间
        #?这样做对方每次发送过来消息我都需要去redis中查询一次当前用户加入过这个房间么,是否可行
        if f'{data["to_user_id"]}_{token["id"]}' not in rooms(sid='对方的id'):
            join_room(sid='对方的id',room=f'{data["to_user_id"]}_{token["id"]}')
            emit('REVEIVE_MSG',msg.to_dict(),room=data['to_user_id'])
            
        emit('REVEIVE_MSG',msg.to_dict(),room=f'{data["to_user_id"]}_{token["id"]}')


friendSocketView=FriendSocketView()


# 好友的增删改查
class FriendView(ApiView):
    method_decorators = [afterLogin]

    def list(self):
        """展示所有好友"""
        friends=db.session.query(User,ChatFriend).outerjoin(ChatFriend,ChatFriend.friend_id==User.id).filter(ChatFriend.is_active==True,
                                    ChatFriend.status==1,
                                    ChatFriend.self_id==token.id).all()
        friends=sort_pinyin(friends)
        return {'code':RET.OK,'msg':error_map[RET.OK],'data':friends}

    def retrieve(self,id):
        """获取单个好友详细信息"""
        friend=db.session.query(ChatFriend,User).outerjoin(User,User.id==id).\
            filter(ChatFriend.self_id==token.id,
                    ChatFriend.status==1,
                   ChatFriend.friend_id==id,
                    ChatFriend.is_active==True).first()
        if friend:
            data=friend[1].to_dict()
            data['user']=friend[0].to_dict()
            data['is_friend']=True
            return {'code':RET.OK,'msg':error_map[RET.OK],'data':data}
        return {'code':RET.PARAMERR,'msg':error_map[RET.PARAMERR]}

    def create(self):
        """添加好友"""
        form=CreateFriendForm(data=request.json)
        if not form.validate():
            return {'code':RET.SERVERERR,'msg':getFlatten(form.errors.values())}
        #判断用户是否在重复添加好友
        res=db.session.query(ChatFriend.id).filter(ChatFriend.self_id==token.id,
                         ChatFriend.friend_id==form.data['friend_id'],
                         ChatFriend.is_active==True).first()
        if res:
            return {'code':RET.USERERR,'msg':'您已经发出过申请了,请去我的申请中查看!'}

        try:
            friend=ChatFriend(self_id=token.id,
                          friend_id=form.data['friend_id'],
                          room=get_room_name(token.id,form.data['friend_id']),
                          remark=form.friend_name,       #在form中动态添加的好友名称
                          initiator_id=token.id
                          )
            db.session.add(friend)
            db.session.commit()
        except Exception as e:
            return {'code':RET.SERVERERR,'msg':error_map[RET.SERVERERR]}
        return {'code':RET.OK,'msg':error_map[RET.OK],'data':friend.to_dict()}

    def delete(self,id):
        """删除好友"""
        ChatFriend.query.filter(or_(and_(ChatFriend.self_id==token.id,ChatFriend.friend_id==id),
                                    and_(ChatFriend.friend_id==id,ChatFriend.self_id==token.id)),
                                ChatFriend.is_active==True,
                                ChatFriend.status==1).update({'is_active':False})
        return {'code':RET.OK,'msg':error_map[RET.OK]}


# 好友审核视图
class FriendCheckView(View):
    method_decorators = [afterLogin]

    def get(self):
        """获取好友审核列表"""
        try:
            type=request.args.get('type',type=int)
            page=request.args.get('page',1,type=int)
            page_num=request.args.get('page_num',6,type=int)
        except:
            return {'code':RET.PARAMERR,'msg':error_map[RET.PARAMERR]}
        if type==1:
            #我发起的审核记录
            history=db.session.query(ChatFriend,User).\
                outerjoin(User,User.id==ChatFriend.friend_id).\
                filter(ChatFriend.initiator_id==token.id,
                    ChatFriend.is_active==True,
                    ).order_by(ChatFriend.create_time.desc())
        else:
            #别人发给我的审核记录
            history = db.session.query(ChatFriend,User).\
                outerjoin(User,User.id==ChatFriend.self_id).\
                filter(ChatFriend.friend_id == token.id,
                        ChatFriend.is_active == True,
                       ChatFriend.initiator_id!=token.id
                        ).order_by(ChatFriend.create_time.desc())
        history=history.paginate(page=page, per_page=page_num, error_out=False)
        data=[]
        for i in history.items:
            temp=i[0].to_dict()
            temp['user']=i[1].to_dict()
            data.append(temp)
        return {'code':RET.OK,'msg':error_map[RET.OK],'data':data}


    def post(self):
        """好友审核"""
        form=CheckFriendForm(data=request.json)
        if not form.validate():
            return {'code':RET.PARAMERR,'msg':getFlatten(form.errors.values())}
        friendCheck=db.session.query(ChatFriend).filter(ChatFriend.friend_id==token.id,
                                            ChatFriend.is_active==True,
                                            ChatFriend.status==2,
                                            ChatFriend.id==form.data['id']).first()
        if not friendCheck:
            return {'code':RET.PARAMERR,'msg':'不存在该好友审核'}
        selfFriend=ChatFriend(self_id=token.id,
                          friend_id=friendCheck.self_id,
                          room=friendCheck.room,
                          )
        selfFriend.status=friendCheck.status = form.data['status']
        if friendCheck.status == 1:
            #用户同意好友请求
            friendCheck.become_friends_time = selfFriend.become_friends_time = datetime.datetime.now()
            selfFriend.room=friendCheck.room
            userName=db.session.query(User.userName).filter(User.id==friendCheck.self_id).scalar()
            selfFriend.remark=userName
        try:
            db.session.add(selfFriend)
            db.session.commit()
        except:
            return {'code':RET.SERVERERR,'msg':error_map[RET.SERVERERR]}
        data=selfFriend.to_dict()
        user=db.session.query(User).filter(data['self_id']==User.id).first()
        data['user']=user.to_dict()
        return {'code':RET.OK,'msg':error_map[RET.OK],'data':selfFriend.to_dict()}


# 好友消息视图
class FriendMsgView(ApiView):
    method_decorators = [afterLogin]

    def list(self):
        """获取好友消息列表的所有消息(消息列表的数据结构要和单条发送消息的结构保持一致)"""
        subquery=db.session.query(FriendsMessage.room,func.max(FriendsMessage.create_time).label(
            's_ctime')).filter(or_(FriendsMessage.to_user_id==token.id,
                                   FriendsMessage.from_user_id==token.id),
                               FriendsMessage.is_active==True).group_by(
            FriendsMessage.room).subquery()

        res=db.session.query(subquery,FriendsMessage).outerjoin(FriendsMessage,
                                                 and_(subquery.c.room==FriendsMessage.room,
                                            subquery.c.s_ctime==FriendsMessage.create_time)).all()
        friends_id=set()
        fina_data=[]
        for room,create_time,msg in res:
            msg=msg.to_dict()
            if msg['to_user_id']==token.id:
                friends_id.add(msg['from_user_id'])
            else:
                friends_id.add(msg['to_user_id'])
            fina_data.append(msg)
        #拿到好友详细信息
        friends_id=db.session.query(ChatFriend,User).outerjoin(User,User.id==ChatFriend.friend_id).\
            filter(ChatFriend.friend_id.in_(friends_id),
                    ChatFriend.self_id==token.id).all()
        friends={}
        for chat,user in friends_id:
            chat=chat.to_dict()
            chat['user']=user.to_dict()
            friends[chat['friend_id']]=chat

        for msg in fina_data:
            if msg['to_user_id'] == token.id:
                msg['user']=friends.pop(msg['from_user_id'])
            else:
                msg['user']=friends.pop(msg['to_user_id'])

        return {'code':RET.OK,'msg':error_map[RET.OK],'data':fina_data}


    def retrieve(self,id):
        """获取单个好友详细聊天历史记录"""
        page=request.args.get('page',1,int)
        queryset=FriendsMessage.get_history_message(room=id)
        queryset= queryset.paginate(page=page, per_page=10, error_out=False)
        data=[i.to_dict() for i in queryset.items][::-1]
        return {'code':RET.OK,'msg':error_map[RET.OK],'data':data}


    def create(self):
        """用户发送消息"""
        form=FriendMsgForm(data=request.json)
        if not form.validate():
            return {'code':RET.PARAMERR,'msg':getFlatten(form.errors.values())}
        msg=FriendsMessage(
            msg=form.msg.data,
            type=form.type.data,
            from_user_id=token.id,
            to_user_id=form.to_user_id.data,
            status=form.status.data,
            room=form.room.data
        )
        db.session.add(msg)
        db.session.commit()
        msg = msg.to_dict()
        msg['user'] = token.user.to_dict()
        emit('FRIEND_NEW_MSG',msg,
             room=FriendRoomUtil.get_room(form.to_user_id.data),
             namespace='/',
             broadcast=True)
        return {'code':RET.OK,'msg':error_map[RET.OK],'data':msg}