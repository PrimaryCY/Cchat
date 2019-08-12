# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/30 14:33
import re

from sqlalchemy.orm.exc import NoResultFound,MultipleResultsFound
from wtforms.fields import simple,IntegerField,FieldList,SelectField
from wtforms import validators

from apps.feedback.model import FeedbackType
from utils.serializer import BaseForm
from utils.optional import Optional


class FeedbackTypeForm(BaseForm):
    ...


class FeedbackForm(BaseForm):
    """反馈问题form"""
    type=IntegerField(
        label='反馈类型',
        validators=[
            validators.DataRequired(message='反馈类型必须输入!')
        ]
    )

    content=simple.TextAreaField(
        label='反馈内容',
        validators=[
            validators.DataRequired(message='反馈内容必须输入!')
        ]
    )

    contact=simple.StringField(
        label='联系方式',
        validators=[
            Optional()
        ]
    )

    feedbackImages=simple.StringField(
        label='反馈图片',
        validators=[
            Optional(),
        ]
    )

    def validate_type(self,type):
        try:
            FeedbackType.query.filter(FeedbackType.id==type.data).one()
        except NoResultFound:
            raise validators.StopValidation('不存在该分类!')
        except MultipleResultsFound:
            raise validators.StopValidation('不存在该分类!')


    def validate_feedbackImages(self,images):
        if images.data:
            for i in images.data:
                if not re.match('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',i):
                    raise validators.StopValidation('图片不符合规则!')

