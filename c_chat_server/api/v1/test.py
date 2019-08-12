# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/19 10:59
from flask_restful import Resource
from apps.test.serializer import PostUser


class Test(Resource):

    def get(self):
        ...

    def post(self):
        serializer=PostUser()
        return serializer.data


        # from apps.user.task import send_mail
        # send_mail.delay('Cchat','907031027@qq.com')
        # return {'data':'发送成功'}

