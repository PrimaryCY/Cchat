import os

from celery import Celery

from c_chat_server.wsgi import app


# 创建应用
celery_app = Celery(app.name,broker=app.config['CELERY']['CELERY_BROKER_URL'])
# 从django.conf:settings中加载celery配置
celery_app.conf.update(app.config.get('CELERY',{}))


#celery -A c_chat_server.celery.celery_app worker -l info --pool=eventlet