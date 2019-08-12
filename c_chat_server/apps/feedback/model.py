# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/30 12:44

from c_chat_server.extensions import db
from utils.baseModel import BaseModel


class FeedbackType(BaseModel,db.Model):
    """反馈问题类型表"""
    __tablename__='feedback_type'

    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True,comment='反馈类型')
    feedbacks=db.relationship('Feedback',backref=db.backref('feedbackType',lazy='joined'),lazy='dynamic')

    @staticmethod
    def init_FeedbackType():
        init_types=['出现广告信息','加载速度慢','功能异常不可用','页面崩溃打不开']
        for i in init_types:
            Ftype = FeedbackType.query.filter(FeedbackType.name == i).first()
            if Ftype is None:
                Ftype = FeedbackType(name=i)
                db.session.add(Ftype)
        db.session.commit()


class Feedback(BaseModel,db.Model):
    """反馈问题"""
    __tablename__='feedback'

    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.TEXT,nullable=False,comment='反馈内容')
    contact=db.Column(db.String(128),comment='反馈联系方式')
    type_id=db.Column(db.Integer,db.ForeignKey('feedback_type.id'),comment='反馈类型')
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),comment='创建人')
    reply_id=db.Column(db.Integer,db.ForeignKey('feedback_reply.id'),comment='官方回复')
    image=db.Column(db.String(256),comment='反馈问题截图封面')
    images=db.relationship('FeedbackImages',lazy='dynamic',backref=db.backref('feedback',lazy='joined'))


class FeedbackReply(BaseModel,db.Model):
    """反馈问题回复表"""
    __tablename__='feedback_reply'

    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(128),nullable=False,comment='回复标题')
    content=db.Column(db.TEXT,nullable=False,comment='回复内容')
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False,comment='回复人')



class FeedbackImages(BaseModel,db.Model):
    """反馈问题截图表"""
    __tablename__='feedback_image'

    id=db.Column(db.Integer,primary_key=True)
    url=db.Column(db.String(256),nullable=False,comment='反馈图片url链接')
    feedback_id=db.Column(db.Integer,db.ForeignKey('feedback.id'),comment='反馈')