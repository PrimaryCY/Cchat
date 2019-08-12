# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/31 9:42
import datetime
import json

from flask import current_app,request,url_for
from flask.globals import _request_ctx_stack
from sqlalchemy import func, and_,distinct
from flask_socketio import emit, join_room, disconnect, leave_room,send

from utils.tools import get_day_zero_time, getFlatten
from globals.before_request import token,SocketAuth
from c_chat_server.constant import RET,error_map
from c_chat_server.extensions import db
from utils.socketUtils import SocketView,SocketRedis,FriendRoomUtil
from utils.resource import ApiView, View
from apps.friend.model import ChatFriend
from apps.user.token import Token
from apps.user.model import User,AnonyMous
from apps.chat.model import ChatRoom,ChatMessage,ChatUserRoom
from apps.chat.form import CreateChatRoomForm
from apps.friend.model import ChatFriend


# 实时聊天准备工作
class Chat(SocketView):
    method_decorators =[SocketAuth]

    def CONNECT(self,*args):
        """
        用户进入网站
        :param args:
        :return:
        """
        #历史总访问量
        current_app.redis.incr('all_user_count')

        #当日访问量
        now,expire_time=get_day_zero_time()
        current_app.redis.incr(f'{now}_users_count')
        print('expire_time:',expire_time)
        current_app.redis.expire(f'{now}_users_count',expire_time)
        emit('CONNECT',True)


    @property               # 获取当前用户所在平台
    def platform(self):
        ua = request.user_agent.platform or ''
        if 'android' in ua or 'Linux' in ua:
            return 0
        elif 'iphone' in ua:
            return 1
        else:
            return 2

                            #保存用户退出登录时间

    def saveUserLogOutInfo(self):
        current_app.redis.hmset(self.onlineUserInfoRedisKey,
                                {'logout_time':
                                     datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

    def AUTHORIZATION(self,token,*args):
        """
        用户身份验证
        :param token:token
        :return: {}
        """
        print('authorization')
        if not token:
            t = AnonyMous().to_dict()
        else:
            userInfo = Token.unpackTk(current_app.config, token)
            if not userInfo:
                return {'code': RET.TOKENERR, 'msg': error_map[RET.TOKENERR], 'data': '1'}
            else:
                user = User.query.filter(User.userName == userInfo['userName']).first()
                t=user.to_dict()
        t['platform']=self.platform

        SocketRedis.set(json.dumps(t))
        # ctx = _request_ctx_stack()
        # ctx.token = t
        # self.saveUserLoginInfo()
        return True


    @property  # 当前登录用户信息的rediskey
    def onlineUserInfoRedisKey(self):
        return f'user_{token["id"]}'


    # 保存用户登录时间
    def saveUserLoginInfo(self):
        current_app.redis.hmset(self.onlineUserInfoRedisKey,
                                {'login_time':
                                     datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')})

    @property  # 当前各个平台在线的redis-Key名称
    def onlineRedisKey(self):
        map = {
            0: 'online_android_users',
            1: 'online_ios_users',
            2: 'online_pc_users'
        }

        return map[token.get('platform')]


    def SOCKET_STAT_ONLINE_NUMS(self,*args,**kwargs):
        """记录统计数据"""
        # 当前在线用户
        current_app.redis.sadd(self.onlineRedisKey,token['id'])
        #保存用户最近一次登录时间
        self.saveUserLoginInfo()


    def SOCKET_HISTORY_MESSAGE(self,*args,**kwargs):
        """获取用户历史消息记录"""

        #加入私人房间
        self._SOCKET_SELF_HISTORY_MESSAGE()
        self._SOCKET_ROOM_HISTORY_MESSAGE()

    def _SOCKET_SELF_HISTORY_MESSAGE(self):
        """加入私人房间"""
        join_room(room=FriendRoomUtil.get_room(token['id']))


    def _SOCKET_ROOM_HISTORY_MESSAGE(self):
        #获取用户群聊房间列表和用户群聊聊天记录
        room_list=db.session.query(ChatUserRoom.chat_room_id).filter(ChatUserRoom.user_id==token['id'],ChatUserRoom.is_active==True).all()
        room_list=[i[0] for i in room_list]
        emit('ROOMLIST', room_list)

        #用户登录之后循环加入之前的房间
        for i in room_list:

            # emit('USER_JOIN', f"{token['userName']}登录了!", room=i)
            join_room(i)
            history_msg=db.session.query(ChatMessage,User).outerjoin(User,User.id==ChatMessage.user_id).filter(ChatMessage.room_id==i).order_by(ChatMessage.create_time.desc()).limit(10).all()
            data=[]
            for u in history_msg:
                history_data=u[0].to_dict()
                if '.' in u[0].user_id:
                    #信息是匿名用户发过来的
                    an=AnonyMous().to_dict()
                    an.pop('id')
                    history_data['user']=an
                else:
                    #信息是实名用户发过来的
                    history_data['user']=u[1].to_dict()
                data.append(history_data)

            history_msg={
                'room_id':i,
                'data':data[::-1]
            }
            #发送历史消息
            emit('RECEIVE_HISTORY_MESSAGE', history_msg,room=i,broadcast=True)


    def SOCKET_DISCONNECT(self):
        """
        用户离开网站时
        """
        current_app.redis.srem(self.onlineRedisKey,token['id'])
        current_app.redis.srem(self.onlineRedisKey,request.remote_addr)
        self.saveUserLogOutInfo()


# 群聊实现
class ChatRoomSocket(SocketView):
    method_decorators = [SocketAuth]

    def SOCKET_JOINROOM(self,data):
        """
        用户加入聊天室
        :param data: 聊天室完整数据
        """
        sql=ChatUserRoom.query.filter(ChatUserRoom.user_id==token['id'],
                                      ChatUserRoom.chat_room_id==data['id'],
                                      ChatUserRoom.is_active==False).first()
        if sql:
            sql.is_active=True
        else:
            sql=ChatUserRoom(
            user_id=token['id'],
            chat_room_id=data['id']
                     )
        db.session.add(sql)
        db.session.commit()
        join_room(data['id'])
        emit('RECEIVE_MESSAGE','你已经进入这个房间了',room=data['id'])
        return True

    def SOCKET_NEWMESSAGE(self,data):
        """
        新消息来临时
        :param data:
        :return:
        """
        msg=ChatMessage(
            user_id=token['id'],
            room_id=data['room_id'],
            msg=data['msg']
        )
        db.session.add(msg)
        db.session.commit()
        msg=msg.to_dict()
        user=User.query.filter(User.id==token['id']).first()
        an=AnonyMous().to_dict()
        an.pop('id')
        msg['user']=user.to_dict() if token['pre']=='user' else an
        emit('NEW_MESSAGE',msg,room=data['room_id'],broadcast=True)
        return True


    def SOCKET_LEAVEROOM(self,data):
        """
        用户离开聊天室
        :param data: 聊天室完整数据
        """
        ChatUserRoom.query.filter(and_(ChatUserRoom.user_id==token['id'],
                                       ChatUserRoom.chat_room_id==data['id'],
                                       ChatUserRoom.is_active==True)).update({"is_active":False})
        db.session.commit()
        leave_room(data['id'])
        emit('RECEIVE_MESSAGE','你已经离开这个房间了',room=data['id'])
        return True


# 获取所有聊天室信息
class ChatRoomView(ApiView):


    def list(self):
        """
        获取所有聊天室信息(只包含聊天室人数,没有聊天室创建人信息)
        """
        order_by = request.args.get('order_by', 'create_time')
        page = request.args.get('p')

        try:
            page=int(page)
        except:
            page=1

        """
                使用了外连子查询
                SELECT * from chat_room as c LEFT JOIN (SELECT chat_room_id,COUNT(*) as nums from ChatUserRoom GROUP BY chat_room_id) as m on c.id=m.chat_room_id ORDER BY m.nums
        """
        sql = db.session.query(ChatUserRoom.chat_room_id,
                               func.count(ChatUserRoom.user_id).label('nums')).\
            filter(ChatUserRoom.is_active==True).group_by(
            ChatUserRoom.chat_room_id).subquery()
        queryset = db.session.query(ChatRoom,sql.c.nums).outerjoin(sql, ChatRoom.id == sql.c.chat_room_id) #.outerjoin(User,User.id==ChatRoom.create_user)

        order_by_mapping={
            'nums':sql.c.nums,
            '-nums':sql.c.nums.desc(),
            'create_time':ChatRoom.create_time,
            '-create_time':ChatRoom.create_time.desc()
        }

        queryset=queryset.order_by(order_by_mapping.get(order_by,'create_time'))

        paginate = queryset.paginate(page=page, per_page=6, error_out=False)

        data=[]
        for i in paginate.items:
            dict=i[0].to_dict()
            # dict['create_user']=i[2]
            dict['nums']=i[1] if i[1] else 0
            data.append(dict)

        return {'code':RET.OK,'msg':error_map[RET.OK],'data':data}



    def retrieve(self,id):
        """
        获取单个聊天室详细信息
        响应:{完整聊天室信息}
        """
        room=db.session.query(ChatRoom,User.userName).outerjoin(User,User.id==ChatRoom.create_user).filter(ChatRoom.id==id).first()

        data={}
        if room:
            data=room[0].to_dict()
            data['founder']=room[1]
        return {'code':RET.OK,'msg':error_map[RET.OK],'data':data}



    def create(self):
        """
        创建聊天室
        请求:{'name':'xxx'}
        响应:{聊天室完整信息}
        """

        if token.pre!='user':
            return {'code':RET.ROLEERR,'msg':'匿名用户不可以创建聊天室!'}

        form=CreateChatRoomForm(data=request.json)
        if form.validate():
            mid_room=ChatUserRoom(
                chat_room=ChatRoom(name=form.name.data,
                          create_user=token.id,
                          img=form.img.data,
                          desc=form.desc.data,
                        ),
                user_id=token.id,
                is_create_user=True
            )
            try:
                db.session.add(mid_room)
                db.session.commit()
                room = mid_room.chat_room
            except:
                db.session.rollback()
                return {'code':RET.SERVERERR,'msg':error_map[RET.SERVERERR]}
            return {'code':RET.OK,'msg':error_map[RET.OK],'data':room.to_dict()}
        return {'code': RET.PARAMERR, 'msg': getFlatten(form.errors.values())}


# 获取聊天室好友列表
class ChatRoomUserView(View):


    def get(self):
        """
        获取聊天室好友列表
        """
        room_id=request.args.get('id',None,int)
        if not room_id:
            return {'code':RET.PARAMERR,'msg':error_map[RET.PARAMERR]}
        sql=db.session.query(
            ChatUserRoom.user_id.label('cuser'),
            ChatUserRoom.is_create_user.label('ccreate_user')
        ).filter(
            and_(
                ChatUserRoom.chat_room_id==room_id,
                ChatUserRoom.is_active==True
            )
        ).subquery()
        data=db.session.query(sql,User).outerjoin(User,User.id==sql.c.cuser).all()

        #获取当前自己的所有好友
        friends=ChatFriend.get_friends_id()

        fina_data=[]
        #判断是否匿名用户,然后添加进去
        for i in data:
            if not i[2]:
                temp=AnonyMous().to_dict()
                temp['id']=i[0]
            else:
                temp=i[2].to_dict()
                #判断两人是否为好友
                if i[0] in friends:
                    temp['is_friend']=True
                    temp['user']=friends[i[0]]
                #判断是否为创建人,是则添加至第一位
                if i[1]:
                    fina_data.insert(0,temp)
                    continue
            fina_data.append(temp)
        #对数据进行分组,5个为一组
        fina_data=[fina_data[i:i+4] for i in range(0,len(fina_data),4)]
        return {'code':RET.OK,'msg':error_map[RET.OK],'data':fina_data}




class ScoketTest(object):

    def test(self,*args):
        print('test:',args)
        emit('test','flask-socketio')


chat = Chat()
chatRoom=ChatRoomSocket()
socketTest=ScoketTest()
