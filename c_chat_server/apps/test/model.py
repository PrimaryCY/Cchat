# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/20 11:07

from c_chat_server.extensions import db
from sqlalchemy.ext.declarative import DeclarativeMeta


class TestModel(db.Model):
    __tablename__='test'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True,nullable=False)



from sqlalchemy.ext.automap import automap_base



class LevelModel(object):
    AutoBase=automap_base()

    @classmethod
    def model(cls,test_id):
        table_index = test_id // 100
        class_name = 'book_%d' % table_index

        ModelClass = getattr(cls.AutoBase.classes,class_name, None)

        if ModelClass is None:
            ModelClass = type(class_name, (db.Model,), {
                '__module__': __name__,
                '__name__': class_name,
                '__tablename__': 'book_%d' % table_index,
                'id': db.Column(db.Integer, primary_key=True),
                'desc': db.Column(db.Text, default=None),
                'test_id':db.Column(db.Integer,index=True)
            })
            db.create_all()
            cls.AutoBase.prepare(db.engine,reflect=True)
        return ModelClass



