//全局配置文件

let settings={
}

settings.DEBUG=true

if(settings){
  //socket的url地址
  settings.SOCKET_URL='http://127.0.0.1:5000'
  //后台url地址
  settings.SERVER_URL='http://127.0.0.1:5000'
}else {
  settings.SERVER_URL='http://192.168.105.228:5000'
  settings.SOCKET_URL='http://192.168.105.228:5000'
}


settings.TOKEN_NAME='tk'

//聊天室默认背面图
settings.ROOM_BACKDEFALT='http://127.0.0.1:5000/static/default/roomBackDefault.jpg'

export default settings
