# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/18 14:17

from flask import Blueprint

gb=Blueprint('globals',__name__)



from .before_request import *
from .signals import *
from .error_handle import *