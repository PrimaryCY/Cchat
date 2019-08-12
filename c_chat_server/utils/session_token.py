# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/22 0:11
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,cors_allowed_origins='*')

@socketio.on('connect')
def xx(*args):
    print('嘿嘿!',args)
    return {1,2,3}

@socketio.on('my event')
def cc(*args):
    print('my event',args)
    return {2,3,4}

if __name__ == '__main__':
    import engineio
    import eventlet

    socketio.run(app, host='127.0.0.1',port=5000, debug=True,use_reloader=False)
    app.run()