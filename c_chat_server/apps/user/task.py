# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/18 18:48
from flask_mail import Message

from c_chat_server.extensions import mail
from c_chat_server.celery import celery_app


@celery_app.task()
def send_mail(to,code):
    from c_chat_server.wsgi import app
    with app.app_context():
        msg = Message(subject='Cchat邮箱验证!',
                      html=f'Cchat邮箱验证码:{code}',
                      recipients=[to])
        mail.send(msg)

