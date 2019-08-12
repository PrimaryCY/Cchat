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
  RECEIVE_SOCKET_FRIEND_HISTORY,
  RECEIVE_FRIEND_MSG_LIST,
  RECEIVE_SOCKET_FRIEND_HISTORY_LIST
} from './mutations-types'
import Vue from 'vue'

export default {

  // [INCREMENT_FOOD_COUNT](state,food){
  //   if(food.count){
  //    food.count++
  //   }else {
  //     //使vue能够监视新增的count属性
  //     Vue.set(food,'count',1)
  //     state.cartFoods.push(food)
  //   }
  // },
  //重置所有信息
  [RETSET_CONF](state){
    state.user={}
    state.nowRoom={}
    state.connectStatus=false
    state.roomList=[]
  },
  //保存用户信息
  [RECEIVE_USERINFO](state,user){
    state.user=user
  },
  //保存当前访问的聊天室
  [RECIVE_NOWROOM](state,data){
    state.nowRoom=data
  },
  //存储socket连接状态
  [RECEIVE_CONNECTSTATUS](state,data){
    state.connectStatus=data
  },
  //存储当前用户加入所有的聊天室
  [RECEIVE_ROOMLIST](state,data){
    if(typeof data ==="number"){
      state.roomList.push(data)
    }else {
      state.roomList=data
    }
  },
  //接收新的实时消息
  [NEW_MESSAGE](state,data){
    console.log('data:',data)
    if(!state[data['room_id']]){
      state[data['room_id']]=[]
    }
    state[data['room_id']].push(data)
  },
  //获取最新的十条历史记录
  [RECEIVE_HISTORY_MESSAGE](state,data){
    state[data['room_id']]=data['data']
  },

  //保存当前正在浏览的好友信息
  [RECEIVE_USER](state,nowUser){
    state.nowUser=nowUser
  },
  //保存当前查看的聊天记录
  [RECEIVE_SOCKET_FRIEND_HISTORY_LIST](state,msg){
    state.friendHistoryMsg=msg
  },
  //保存socket传入的信息
  [RECEIVE_SOCKET_FRIEND_HISTORY](state,msg){
    if(state.nowUser.id===msg.from_user_id){
      //这里可以再加上已读未读!
      state.friendHistoryMsg.push(msg)
    }
  },
  //获取消息列表数据
  [RECEIVE_FRIEND_MSG_LIST](state,data){
    state.friendMsgList=data
  }
}
