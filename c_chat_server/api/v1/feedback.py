# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/7/30 12:14
from flask import request

from apps.feedback.model import FeedbackType,FeedbackImages,Feedback
from utils.resource import View
from utils.tools import getFlatten
from utils.authentication import afterLogin
from c_chat_server.constant import RET,error_map
from c_chat_server.extensions import db
from globals.before_request import token
from apps.feedback.form import FeedbackForm


class FeedbackTypeView(View):

    def get(self):
        """
        * 获取意见反馈类型:
        * 响应:{code:'2000',msg:'ok',data:[{id:1,name:'出现广告信息'},]}
        """
        types=db.session.query(FeedbackType.id,FeedbackType.name).filter(FeedbackType.is_active==True).all()
        return {'code':RET.OK,'msg':error_map[RET.OK],'data':
            [{'id':i[0],'name':i[1]} for i in types]}


#
class FeedbackView(View):
    method_decorators = {
        'post':[afterLogin]
    }


    def post(self):
        """
        * 新建意见反馈:
        * 请求:{type:1,content:'',contact:'',feedbackImages:[]}
        * 响应:{code:'2000',msg:'ok'}
        """
        form=FeedbackForm(data=request.json)
        if form.validate():
            img_list=[FeedbackImages(url=i) for i in form.feedbackImages.data]
            data={
                'type_id':form.data['type'],
                'content':form.data['content'],
                'contact':form.data.get('contact',''),
                'user_id':token.id,
                'images':img_list,
                'image':form.feedbackImages.data[0] if len(form.feedbackImages.data)>0 else ''
            }
            try:
                fb=Feedback(**data)
                db.session.add(fb)
                db.session.commit()
            except Exception as ex:
                db.session.rollback()
                return {'code':RET.SERVERERR,'msg':error_map[RET.SERVERERR]}
            return {'code':RET.OK,'msg':error_map[RET.OK]}
        return {'code':RET.PARAMERR,'msg':getFlatten(form.errors.values())}




