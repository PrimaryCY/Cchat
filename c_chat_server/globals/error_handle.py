    # -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/25 16:15
from flask import jsonify

from c_chat_server.constant import error_map
from globals.globals_manage import gb

# func="""
# @gb.app_errorhandler({code})
# def xx():
#     return jsonify({{'status':{code},'massage':error_map['{code}']}})
# """
#
# for code in error_map:
#     exec(func.format(code=code))