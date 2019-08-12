# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/5/9 22:12
from flask_restful import Resource


class View(Resource):
    ...


class ApiView(View):

    def get(self,**kwargs):
        if kwargs.get('id'):
            return self.retrieve(**kwargs)
        return self.list()

    def post(self):
        return self.create()

    def put(self,**kwargs):
        return self.update(**kwargs)

    def delete(self,**kwargs):
        return self.delete(**kwargs)