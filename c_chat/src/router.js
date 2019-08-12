import Vue from 'vue'
import Router from 'vue-router'
import VueCookies from 'vue-cookies'
import {Toast} from 'vant'

import store from './store/store'

Vue.use(Router)

//路由懒加载
const home=()=>import ('./views/home/home.vue')
const addressList=()=>import('./views/addressList/addressList')
const msg=()=>import('./views/msg/msg')
const weChat=()=>import('./views/weChat/weChat')
import login from './views/login/login'
import register from './views/register/register'
import pwd from './views/pwd/pwd'
import portrait from './views/portrait/portrait'
import info from './views/info/info'
import feedback from './views/feedback/feedback'
import  About from './views/about/About'
import createRoom from './views/createRoom/createRoom'
import chatDetail from './views/chatDetail/chatDetail'
import roomDetail from './views/roomDetail/roomDetail'
import myFirendCheck from './views/myFriendCheck/myFriendCheck'
import fApply from './views/myFriendCheck/fApply/fApply'
import sApply from './views/myFriendCheck/sApply/sApply'
import friendChatDetail from './views/friendChatDetail/friendChatDetail'


let VueRouter=new Router({
  //模式变成history,本地没有做相应配置,打包会变成白屏
  mode: 'hash',
  base: process.env.BASE_URL,
  routes: [
    {path:'/',redirect:'/home'},
    {
      path: '/home',
      name: 'home',
      component: home,
      meta:{
        showFooter:true,
        keepAlive:true
      },
    },
    {
      path: '/msg',
      name: 'msg',
      component: msg,
      meta:{
        showFooter:true,
        // keepAlive:true,
      },
    },
    {
      path: '/addressList',
      name: 'addressList',
      component: addressList,
      meta:{
        showFooter:true,
        keepAlive:true,
      }
    },
    {
      path: '/weChat',
      name: 'weChat',
      component: weChat,
      meta:{
        showFooter:true,
        keepAlive:true
      }
    },
    {
      path:'/login',
      name:'login',
      component:login,
      meta:{
        showFooter:false,
        keepAlive:true
      }
    },
    {
      path:'/register',
      name:'register',
      component:register,
      meta:{
        showFooter:false,
        keepAlive:true,
        isScroll:true
      }
    },
    //修改密码页
    {
      path:'/pwd',
      name:'pwd',
      component:pwd,
      meta:{
        showFooter:false,
        keepAlive:true,
        isLogin:true
      },
    },
    //修改头像页
    {
      path:'/portrait',
      name:'portrait',
      component:portrait,
      meta:{
        showFooter:false,
        keepAlive:true,
        isLogin:true
      },
    },
    //个人资料
    {
      path:'/info',
      name:'info',
      component:info,
      meta:{
        showFooter:false,
        keepAlive:true,
        isLogin:true
      },
    },
    //意见反馈
    {
      path:'/feedback',
      name:'feedback',
      component:feedback,
      meta:{
        showFooter:false,
        isLogin:true,
        isScroll:true
      },
    },
    //关于
    {
      path: '/about',
      name: 'about',
      component: About,
      meta:{
        showFooter:true,
        keepAlive:true
      }
    },
    //创建聊天室
    {
      path: '/createRoom',
      name: 'creatRoom',
      component: createRoom,
      meta:{
        showFooter:true,
        keepAlive:true,
        isLogin:true,
     }
    },
    //聊天室聊天
    {
      path: '/chatDetail',
      name: 'chatDetail',
      component: chatDetail,
    },
    //私人聊天室聊天
    {
      path: '/friendChatDetail',
      name: 'friendChatDetail',
      component: friendChatDetail,
    },
    //聊天室简介
    {
      path: '/roomDetail',
      name: 'roomDetail',
      component:roomDetail ,
      meta:{
        isScroll:true
      }
    },
    //我的好友申请
    {
      path:'/myFriendCheck',
      name:'myFriendCheck',
      component:myFirendCheck,
      meta:{
        showFooter:true,
        isScroll:true
      },
      children:[
        {path:'fApply/',component:fApply,meta:{showFooter:true}},
        {path:'sApply/',component:sApply,meta:{showFooter:true}},
        {path:'',redirect: 'fapply'}
      ]
    }
  ]
})

VueRouter.beforeEach((to, from, next) => {
  //如果未登录不可以访问修改用户资料的页面
  if(to.meta.isLogin){
    if(!VueCookies.get('tk')){
      next({
        path: '/login',
        query: {redirect: to.fullPath}   //登录成功后重定向到当前页面
      })
    }
  }
  //如果本地 存在 token 则 不允许直接跳转到 登录页面
  //ios端无法删除cookie
  // if(to.fullPath === "/login"){
  //   if(VueCookies.get('tk')){
  //     next({
  //       path:from.fullPath
  //     });
  //     Toast('您已登录!不可以重复登录!')
  //   }else {
  //     next();
  //   }
  // }else {
  //   next()
  // }
  next()
})

export default VueRouter
