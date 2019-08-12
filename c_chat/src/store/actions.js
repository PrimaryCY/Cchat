import {
  RECEIVE_USERINFO,
  RECEIVE_CONNECTSTATUS,
  RECEIVE_ROOMLIST,
  RECIVE_NOWROOM,
  RETSET_CONF,
  NEW_MESSAGE,
  RECEIVE_HISTORY_MESSAGE,
  RECEIVE_FRIENDS,
  RECEIVE_USER,
  RECEIVE_FRIEND_HISTORY,
  RECEIVE_SOCKET_FRIEND_HISTORY,
  RECEIVE_FRIEND_MSG_LIST, RECEIVE_SOCKET_FRIEND_HISTORY_LIST
} from "./mutations-types"

import {
  get_user,
  getFriendMsg,
  getFriendMsgList
} from "../api/index"
import axios from '../api/ajax'
import Vue from 'vue-socket.io'


export default {

  async receive_userinfo({commit},callback){
    //存储用户信息
    let user=await get_user()
    if(user.data.code==='2000'){
      let user_info=user.data.data
      commit(RECEIVE_USERINFO,user_info)
    }
    callback && callback()
  },
  async modify_userinfo({commit},data){
    //修改本地用户信息
    commit(RECEIVE_USERINFO,data)
  },
  receive_nowRoom({commit},data){
    //当前访问的聊天室
    commit(RECIVE_NOWROOM,data)
  },
  reset_conf({commit}){
    //重置所有状态
    commit(RETSET_CONF)
  },
  receive_nowUser({commit},nowUser){
    commit(RECEIVE_USER,nowUser)
  },

  SOCKET_CONNECT({commit},data){
    //接收连接状态
    commit(RECEIVE_CONNECTSTATUS,data)
  },
  SOCKET_ROOMLIST({commit},data){
    //接收用户当前所有加入的聊天室
    //console.log('vm',this._vm)
    commit(RECEIVE_ROOMLIST,data)
    // console.log('Roomlist',data)
  },
  SOCKET_RECEIVE_HISTORY_MESSAGE({commit},data){
    //接收用户的聊天历史记录
    commit(RECEIVE_HISTORY_MESSAGE,data)
  },
  SOCKET_NEW_MESSAGE({commit}, data) {
    //接收实时发送过来的聊天信息
    commit(NEW_MESSAGE,data)
  },
  SOCKET_USER_JOIN({commit},data){
    console.log(data)
  },
  SOCKET_FRIENDS({commit},data){
    //接收用户当前所有的好友列表
    commit(RECEIVE_FRIENDS,data)
  },

  //获取单个好友历史消息
  async receive_friend_history({commit},{room,cb}){

      let res=await getFriendMsg(room)
      if(res.data.code==='2000'){
        commit(RECEIVE_SOCKET_FRIEND_HISTORY_LIST,res.data.data)
      }else{
        this._vm.$toast('请检查您的网络连接是否正确')
      }
      cb&&cb()
  },
  //获取消息列表
  async receive_friend_msg_list({commit},cb){
    let res=await getFriendMsgList()
    if(res.data.code==='2000'){
      commit(RECEIVE_FRIEND_MSG_LIST,res.data.data)
    }else {
      this._vm.$toast(res.data.msg)
    }
    cb&&cb()
  },
  //接收服务端发来的消息
  SOCKET_FRIEND_NEW_MSG({commit},msg){
    console.log('收到消息!')
    commit(RECEIVE_SOCKET_FRIEND_HISTORY,msg)
  }
}
