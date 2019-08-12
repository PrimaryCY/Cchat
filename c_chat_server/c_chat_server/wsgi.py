# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/17 16:28
import sys
import os
import click
sys.path.insert(0,'..')

from flask import Flask

from c_chat_server.app_manage import blue_manage
from c_chat_server import settings
from c_chat_server.extensions import db,cors,mail,socketIo
from apps.user.model import Role
from apps.feedback.model import FeedbackType


def create_application():
    """application工厂函数"""
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    app = Flask(__name__,root_path=BASE_DIR)

    register_extensions(app)
    register_blueprint(app)
    register_command(app)

    print(app.url_map)
    return app


def register_extensions(app):
    """注册扩展"""
    env=os.environ.get('FLASK_ENV','development')
    setting=settings.SETTING_MAPPING.get(env)
    assert setting,(
        f'配置文件:{env}不存在!,当前存在映射:{settings.SETTING_MAPPING}'
    )

    setting.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    cors.init_app(app,resources="/*",supports_credentials=True)
    socketIo.init_app(app,cors_allowed_origins='*')

    #csrf.init_app(app)
    return socketIo


def register_blueprint(app):
    """注册全局蓝图"""
    app.register_blueprint(blue_manage)


def register_command(app):
    """注册自定义命令"""
    @app.cli.command()
    def init():
        click.echo('Initializing the roles and permissions...')
        Role.init_role()
        click.echo('Initializing the FeedbackType...')
        FeedbackType.init_FeedbackType()
        click.echo('Done.')


app=create_application()


if __name__ == '__main__':
    socketIo.run(app)
