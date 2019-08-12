# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/20 11:11
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
from flask_cors import CORS
from flask_mail import Mail
from flask_socketio import SocketIO

db=SQLAlchemy()
csrf=CSRFProtect()
cors=CORS()
mail=Mail()
socketIo=SocketIO()