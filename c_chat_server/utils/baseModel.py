# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/26 21:40
import datetime
from datetime import date
from collections import Iterable

from sqlalchemy import Column,DATETIME,Boolean
from sqlalchemy_utils.types.choice import Choice
from sqlalchemy.orm import backref, relationship, object_session
from sqlalchemy.ext.hybrid import hybrid_method
from sqlalchemy.orm.session import Session
from sqlalchemy.ext.declarative import declared_attr

from globals.signals import before_create,after_create


class BaseModel(object):

    def __init__(self,**kwargs):
        before_create.send('before_create',model=self,**kwargs)
        super().__init__(**kwargs)
        #after_create.send('after_create',model=self,**kwargs)

    @declared_attr
    def create_time(cls):
        return Column("create_time", DATETIME,default=datetime.datetime.now,
                      nullable=True,comment='创建时间')

    @declared_attr
    def update_time(cls):
        return Column("update_time", DATETIME,default=datetime.datetime.now,onupdate=datetime.datetime.now,nullable=True,comment='修改时间')


    @declared_attr
    def is_active(cls):
        return Column('is_active',Boolean,default=True,comment='状态',nullable=True)

    @hybrid_method
    def to_dict(self,values:Iterable=None):
        """
        将Model转化为dict
        :param values: 指定转换哪些字段
        :return: dict
        """
        temp={}
        for c in values or self.__table__.columns:
            attr=getattr(self, c if isinstance(c,str) else c.name)
            if isinstance(attr,datetime.datetime) or isinstance(attr,date):
                attr=attr.strftime('%Y-%m-%d %H:%M:%S')
            elif isinstance(attr,Choice):
                attr=attr.value
            temp[c if isinstance(c,str) else c.name]=attr
        return temp