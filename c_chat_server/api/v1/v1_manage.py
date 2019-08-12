# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/18 13:56
from flask_restful import Api

from c_chat_server.extensions import socketIo
from c_chat_server.app_manage import BluePrintManage

v1=BluePrintManage('api',__name__)

from .user import UserView,LoginView,EmailView,PwdView,UploadView
from .feedback import FeedbackTypeView,FeedbackView
from .chat import chat,socketTest,ChatRoomView,chatRoom,ChatRoomUserView
from .friend import friendSocketView,FriendView,FriendCheckView,FriendMsgView
from .test import Test


api=Api(v1,prefix='/api/v1')
# 获取邮箱验证码
api.add_resource(EmailView,'/email')
# 用户crud接口
api.add_resource(UserView,'/user')
api.add_resource(LoginView,'/login')
api.add_resource(PwdView,'/pwd')
# 反馈信息
api.add_resource(FeedbackTypeView,'/feedbackTypes')
api.add_resource(FeedbackView,'/feedback')

# 聊天室crud
api.add_resource(ChatRoomView,'/chatRooms','/chatRooms/<int:id>')
# 获取聊天室好友
api.add_resource(ChatRoomUserView,'/chatRoomUsers')

#好友增删改查
api.add_resource(FriendView,'/friends','/friends/<int:id>')
#好友状态审核
api.add_resource(FriendCheckView,'/friendCheck')
#好友消息列表
api.add_resource(FriendMsgView,'/friendMsgs','/friendMsgs/<string:id>')

# socket用户连接
socketIo.on_event('connect',chat.CONNECT)
socketIo.on_event('disconnect',chat.SOCKET_DISCONNECT)
socketIo.on_event('AUTHORIZATION',chat.AUTHORIZATION)
socketIo.on_event('STAT_ONLINE_NUMS',chat.SOCKET_STAT_ONLINE_NUMS)
socketIo.on_event('HISTORY_MESSAGE',chat.SOCKET_HISTORY_MESSAGE)

socketIo.on_event('JOINROOM',chatRoom.SOCKET_JOINROOM)
socketIo.on_event('LEAVEROOM',chatRoom.SOCKET_LEAVEROOM)
socketIo.on_event('NEWMESSAGE',chatRoom.SOCKET_NEWMESSAGE)


# 测试使用
socketIo.on_event('test',socketTest.test)
# 上传接口
api.add_resource(UploadView,'/upload')

# 测试接口
api.add_resource(Test,'/test')

