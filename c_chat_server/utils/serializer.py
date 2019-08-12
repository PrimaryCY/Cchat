# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/20 9:47
import time
from collections import OrderedDict
from concurrent.futures import ThreadPoolExecutor

from flask import current_app,request
from wtforms.form import Form
from wtforms.compat import iteritems


class SerializerRequest(object):
    """拷贝request类"""
    copy_method=(
        'args',
        'method',
        'json',
        'form',
        'environ',
        'url',
        'remote_addr'
    )

    def __init__(self,request:request) -> request:
        for i in dir(request):
            if i in self.copy_method:
                setattr(self,i,getattr(request,i))


class Serializer(object):


    def __init__(self,request:request):
        self.request=SerializerRequest(request)
        self.validated_data=OrderedDict()
        if not isinstance(current_app.config.get('SERIALIZER_THREAD_POLL'),ThreadPoolExecutor):
            raise Exception(f'当前传入的:{current_app.config.get("SERIALIZER_THREAD_POLL")},'
                            f'不是一个线程池对象!')
        self.pool=current_app.config['SERIALIZER_THREAD_POLL']


    def is_valid(self)->bool:

        tasks=[self.pool.submit(getattr(self,i),self.request)
               for i in dir(self) if i.startswith('valid_')]

        for task in tasks:
            if task.exception():
                self.validated_data=task.exception().args[0]
                return False
        return True


    @property
    def data(self):
        return self.validated_data


class BaseForm(Form):

    @property
    def data(self):
        return dict((name, f.data) for name, f in iteritems(self._fields) if f.data is not None)
