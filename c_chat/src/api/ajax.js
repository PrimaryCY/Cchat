import axios from 'axios'
import VueCookies from 'vue-cookies'

import router from '../router'
import store from '../store/store'

import settings from '../conf/settings'

let service=axios.create({
  baseURL:settings.SERVER_URL,
  timeout:5000,
  headers:{
    'content-type':'application/json'//转换为key=value的格式必须增加content-type
  },
})
let cancel ,promiseArr = {}

//http-请求拦截
// service.interceptors.request.use(
//   config => {
//     if (promiseArr[config.url]) {//发起请求时，取消掉当前正在进行的相同请求
//       promiseArr[config.url]('操作取消')
//       promiseArr[config.url] = cancel
//     }else{
//       promiseArr[config.url] = cancel
//     }
//     return config
//   },
//   error => {
//     return Promise.reject(err)
//   }
// );

service.interceptors.request.use(
  request => {
    if (VueCookies.get('tk')) {  // 判断是否存在token，如果存在的话，则每个http header都加上token
      request.headers.tk = VueCookies.get('tk');
    }
    return request;
  },
  err => {
    return Promise.reject(err);
  });

import {Toast} from "vant"
//http-响应拦截
service.interceptors.response.use(
  response => {
      console.log(response)
      switch(response.data.code) {
        case '4101':
          if(!settings.DEBUG){
            //先不要删除,google浏览器启动会以pc模式启动,而注册用的却是ios的token,所以刚打开时会用户登录失效,刷新一下就好
            VueCookies.remove('tk')
          }
          store.state.userInfo={}
          console.log('用户令牌失效!')
          router.replace({
            path: '/login',
            query: {
              redirect: router.currentRoute.fullPath
            }
          })
          break
      }
      return response;
  },
  error => {
    // switch (error.response.status) {
    //   case 404:
    //     Toast('网络错误:'+error.response.status)
    //     break
    // }
    return Promise.reject(error)
  }
)

export default {
  get(url, param={}) {//get请求
    return new Promise((resolve, reject) => {
      service({
        method: 'get',
        url,
        params: param,
      }).then(res => {
        resolve(res)
      })
    })
  },
  post(url, param) {//post请求
    return new Promise((resolve, reject) => {
      service({
        method: 'post',
        url,
        data: param,
      }).then(res => {
        resolve(res)
      })
    })
  },
  put(url, param) {//put请求
    return new Promise((resolve, reject) => {
      service({
        method: 'put',
        url,
        data: param,
      }).then(res => {
        resolve(res)
      })
    })
  },
  delete(url,param) {//delete请求
    return new Promise((resolve, reject) => {
      service({
        method: 'delete',
        url,
        data: param,
      }).then(res => {
        resolve(res)
      })
    })
  },
  upload(url, data) {//上传文件
    return new Promise((resolve, reject) => {
      let formData=new FormData();
      // formData.append('name',name)
      formData.append('file',data)
      console.log('formData:',formData.get('file'))
      axios({
        method: 'post',
        url,
        data:formData,
        headers: {
          'content-type':'multipart/form-data'
        }
      }).then(res => {
        resolve(res)
      })
    })
  },
}

