# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/20 10:14
import time

from flask import request
from wtforms.fields import simple,html5,core
from wtforms.form import Form
from wtforms import validators
from wtforms import widgets,SubmitField
from wtforms.csrf.core import CSRF
from flask_restful.reqparse import RequestParser

from utils.serializer import Serializer

class PostUser(object):

    @property
    def serializer(self):
        if not hasattr(self,'_serializer'):
            self._serializer=RequestParser()
        return self._serializer

    @property
    def data(self):
        return self.serializer.parse_args()

    def __init__(self):
        self.serializer.add_argument(
            'username', dest='username',
            type=str, location='json',
            required=True, help='The user\'s username',
        )
        self.serializer.add_argument(
            'password',type=dict,required=True,
        )






class TestSerializer(Serializer):

    def valid_id(self,request:request):
        id=request.args.get('id',None)
        if id:
            #time.sleep(2)#模拟io
            self.validated_data['id']=id*3

    def valid_name(self,request:request):
        name = request.args.get('name', None)
        if name:
            #time.sleep(2)  # 模拟io
            self.validated_data['name'] = request.args

