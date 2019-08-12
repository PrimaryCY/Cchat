# <font color=#ca0c16> Cchat
**flask+vue+socketio实时在线聊天web系统**
<br>
<br>
&nbsp;&nbsp;&nbsp;&nbsp;之前学习socketio部分,一直找不到好的教程,git上面也都是些小demo,不能放入实际生产环境中运行,于是自己就写了这个项目,里面还有很多bug,有一部分功能待完善,主体业务功能已经实现,希望能够对大家学习socketio部分有所帮助,大家如果有什么好的建议可以提给我.共同进步!
<br>
个人qq:907031027

---
### <font color=#ca0c16>项目展示
![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170433.png?raw=true)

![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170433.png?raw=true)
![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170444.png?raw=true)
![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170458.png?raw=true)
![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170530.png?raw=true)
![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170539.png?raw=true)
![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170547.png?raw=true)
![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170558.png?raw=true)
![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170610.png?raw=true)
![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170622.png?raw=true)
![avatar](https://github.com/PrimaryCY/Cchat/blob/dev/c_chat_server/static/project/QQ%E6%88%AA%E5%9B%BE20190812170630.png?raw=true)

---
### <font color=#ca0c16>前端技术使用
    - vue
    - vuex
    - vue-socketio
    - vue-cookies
    - vant
    - vue-router
    - vue-cli3
    - axios
    
---
### <font color=#ca0c16>后端技术使用
    - flask
    - flask-socketio
    - flask-sqlalchemy
    - flask-mail
    - flask-restful
    - flask-wtform
    - celery

---
### <font color=#ca0c16>关系型数据库选型
    - mysql

---
### <font color=#ca0c16>非关系型数据库选型
    - redis

### <font color=#ca0c16>项目运行
*后台部分:*
```
cd c_chat_server
pip3 install -r requirements.txt #python安装依赖
```

打开manage.py文件
```
if __name__ == '__main__':
    socketIo.run(app,host='0.0.0.0',debug=True)
    #app.run()
    #manage.run()
```
修改为
```
if __name__ == '__main__':
    #socketIo.run(app,host='0.0.0.0',debug=True)
    #app.run()
    manage.run()
```
```
python manage.py db migrate
python manage.py upgrade
#再将manage.py--#socketIo.run(app,host='0.0.0.0',debug=True)的注释打开
python manage.py
```
*前端部分:*
```
cd c_chat
npm install
npm run serve
```
