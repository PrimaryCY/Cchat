import Vue from 'vue';
import App from './App.vue';
import router from './router';
import store from './store/store';


import 'amfe-flexible/index.js';                                        //适配手机浏览器

import 'vant/lib/index.css';
import './common/style/vant.scss';                                      //导入全局自定义vant样式
import './common/style/reset.css';
import './common/style/button.css'

import settings from './conf/settings'
import './socket'                                                       //导入socket
Vue.prototype.$settings=settings

import VueCookies from 'vue-cookies';
import {NavBar, PullRefresh,Toast,Loading,Button,Popup,Dialog,Field,
  CellGroup,Cell,Uploader,Icon,Grid,GridItem,Divider,Col,Row,Tag,Image,IndexBar,
  IndexAnchor,Tabs,Tab
} from 'vant';

Vue.use(Grid).use(GridItem);
Vue.use(VueCookies)
Vue.use(NavBar).use(PullRefresh).use(Toast).use(Loading).use(Button).use(Popup).use(Dialog)
  .use(Field).use(CellGroup).use(Cell).use(Uploader).use(Icon).use(GridItem).use(Grid).use(Divider)
  .use(Row).use(Col).use(Tag).use(Image).use(IndexBar).use(IndexAnchor).use(Tab).use(Tabs)





//import './mock/mock'


Vue.config.productionTip = false


new Vue({
  router,
  store,
  render: h => h(App),
  mounted(){
    console.log('in:',this.sockets)
  },
  sockets:{
    connect(){
      //传输token给后台验证
      this.socketEmit('AUTHORIZATION',this.$cookies.get(this.$settings.TOKEN_NAME) || null, flag=>{
        if(flag){
          this.socketEmit('STAT_ONLINE_NUMS')
          this.socketEmit('HISTORY_MESSAGE')
        }
      })
    },
    test(data){
      //console.log('test:',data)
      //console.log('123123123')
    }
  }
}).$mount('#app')
