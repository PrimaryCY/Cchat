# -*- coding: utf-8 -*-
# author:CY
# datetime:2019/6/18 11:25
from flask_script import Manager
from flask_migrate import MigrateCommand,Migrate

from c_chat_server.wsgi import app
from c_chat_server.extensions import db,socketIo



manage=Manager(app)

@manage.option('-i','--name', dest='name')
@manage.command
def init(*args,**kwargs):
    print(args)
    print(kwargs)
    print('init')


migrate=Migrate(app,db,'./apps/migrations')
manage.add_command('db',MigrateCommand)
#manage.add_command('init',init)




if __name__ == '__main__':
    socketIo.run(app,host='0.0.0.0',debug=True)
    #app.run()
    #manage.run()