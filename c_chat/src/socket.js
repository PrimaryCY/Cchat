import Vue from 'vue';
import VueCookie from 'vue-cookies'
import VueSocketIO from "vue-socket.io";
import socketio from 'socket.io-client';
import store from './store/store';

import settings from './conf/settings'

Vue.use(new VueSocketIO({
  debug: true,
  connection: socketio(settings.SOCKET_URL),
  vuex: {
    store,
    actionPrefix: 'SOCKET_',
    mutationPrefix: 'SOCKET_'
  },
}))



Vue.prototype.socketEmit=function (MessageName,data={},cb) {
  // let tk=VueCookie.get(settings.TOKEN_NAME)
  // console.log('tk',tk)
  // let finaData
  // if(tk){
  //   finaData=[tk,data]
  // }else {
  //   finaData=[null,data]
  // }

  //socketio请求拦截
  this.$socket.emit(MessageName,data,res=>{
    if(res&&res.code){
      switch (res.code) {
        case '4101':
          this.$cookies.set('tk','',1)
          this.$cookies.remove("tk");
          this.$store.dispatch("reset_conf");
          this.$toast('用户失效!请重新登录!')
          this.$router.replace('/login')
          this.$socket.disconnect()
          break
      }
    }
    cb&&cb(res)
  })
}
