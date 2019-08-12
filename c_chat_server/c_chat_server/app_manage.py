# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/18 13:30
from flask import Blueprint

class BluePrintManage(Blueprint):
    """嵌套注册蓝图"""
    def register_blueprint(self, blueprint, **options):
        def deferred(state):
            url_prefix = options.get('url_prefix')
            if url_prefix is None:
                url_prefix = blueprint.url_prefix
            if 'url_prefix' in options:
                del options['url_prefix']
            state.app.register_blueprint(blueprint,url_prefix=url_prefix,**options)
        self.record(deferred)

blue_manage=BluePrintManage('manage',__name__)

#将注册进来的蓝图添加至此出
from globals.globals_manage import gb
from api.v1.v1_manage import v1
blue_manage.register_blueprint(gb)
blue_manage.register_blueprint(v1)