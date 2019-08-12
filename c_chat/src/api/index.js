import axios from './ajax'


export const get_goods=()=>axios.get(`/goods`)
export const get_banners=()=>axios.get('/banners')
export const post_login_sms=data=>axios.post('/login/sms',data)
export const post_login_pwd=data=>axios.post('/login/pwd',data)
export const captcha=()=>axios.get('/captcha')

export const delete_login=()=>axios.delete('/login')
export const search=(data)=>axios.get('/search',data)

/*
* 获取邮箱验证码:
* 请求:{email:'907031027@qq.com'}
* 响应:{code:'2000',msg:'ok'}
*/
export const getVerCode=(data)=>axios.post('/api/v1/email',data)
/*
* 登录接口:
* 请求:{email:'907031027@qq.com',code:'123456',username:'',pwd:'',type:1}
* 响应:{token:'1234567890123',user:{完整用户信息}}
* */
export const postLogin=(data)=>axios.post('/api/v1/login',data)
/*
* 获取用户信息:
* 响应:{userName:'907031027',nickName:'nick',email:'907031027@qq.com'}
* */
export const get_user=()=>axios.get('/api/v1/user')
/*
* 注册用户:
* 请求:{userName:'907031027',nickName:'xx',pwd:'1234567',checkPwd:'1234567'}
* 响应:{token:'12345678'}
* */
export const post_user=(user)=>axios.post('/api/v1/user',user)
/*
* 修改用户资料:
* 请求:{area:[{code: "110000",name: "北京市"},{code: "110000",name: "朝阳区"},{code: "110000",name: "望京"}]
* ,birth: "1950-01-01",email: "907031027@qq.com",sex: "男"}
* 响应:{完整用户信息}
* */
export const put_user=(user)=>axios.put('/api/v1/user',user)
/*
* 退出登录:
* 响应:{code:'2000',msg:'ok'}
* */
export const deleteLogin=()=>axios.delete('/api/v1/login')
/*
*修改密码:
*请求:{pwd:'12345678',newPwd:'1111111','repeatPwd':'11111111'}
*响应:{code:'2000',msg:'ok'}
*/
export const updatePwd=(data)=>axios.put('/api/v1/pwd',data)
/*
* 获取意见反馈类型:
* 响应:{code:'2000',msg:'ok',data:[完整的意见反馈类型]}
* */
export const getFeedbackTypes=()=>axios.get('/api/v1/feedbackTypes')
/*
* 意见反馈:
* 请求:{type:1,content:'',contact:'',feedbackImages:[]}
* 响应:{code:'2000',msg:'ok'}
* */
export const postFeedback=(data)=>axios.post('/api/v1/feedback',data)
/*
* 获取聊天室列表
* 响应:[{完整聊天室信息},{完整聊天室信息}]
* */
export  const getChatRooms=(params,id='')=>axios.get('/api/v1/chatRooms'+(id?'/'+id:''),params)
/*
* 创建聊天室
* 请求:{name:'聊天室a',desc:'一个聊天',img:'聊天室封面图'}
* 响应:
* */
export const postChatRooms=(data)=>axios.post('/api/v1/chatRooms',data)
/*
* 获取聊天室好友列表
* 请求:{'id':1}
* 响应:{'data':[
*               [{完整用户信息},{完整用户信息},{完整用户信息}],
*               [{完整用户信息},{完整用户信息}]
*             ]}
* */
export const getChatRoomUsers=(params)=>axios.get('/api/v1/chatRoomUsers',params)
/*
* 添加好友
* 请求:{'id':好友id}
* 响应:{完整的好友信息}
* */
export const postFriend=(data)=>axios.post('/api/v1/friends',data)
/*
* 获取好友申请列表
* 请求:{'type':0[别人发送给我的],1[我发送给别人的]}
* 响应:[{每条请求信息},{每条请求信息}]
* */
export const getFriendCheck=(params)=>axios.get('api/v1/friendCheck',params)
/*
* 处理好友申请
* 请求:{id:好友审核表id,status:要处理的状态值,0[不通过],1[通过],3[忽略]}
* 响应:{完整审核表信息}
* */
export const postFriednCheck=(data)=>axios.post('api/v1/friendCheck',data)
/*
* 获取当前好友列表
* 响应:{'a':[{完整好友信息},{完整好友信息}],'b':[{完整好友信息}]}
* */
export const getFriends=()=>axios.get('/api/v1/friends')
/*
*获取某个好友详细信息
* 请求:url+id
* 响应:{好友完整信息}
* */
export const retrieveFirends=(id)=>axios.get('/api/v1/friends/'+id)
/*
* 获取好友私聊聊天记录
* 请求:{'page':1}
* 响应[{聊天消息},{聊天消息}]
* */
export const getFriendMsg=(roomName)=>axios.get('api/v1/friendMsgs/'+roomName)
/*
* 给好友发送消息
* 请求:{}
* 响应:{完整的聊天信息}
* */
export const  postFriendMsg=(data)=>axios.post('api/v1/friendMsgs',data)
/*
* 获取消息列表
* 响应:[{单条消息},{单条消息},{单条消息}]
* */
export const getFriendMsgList=()=>axios.get('api/v1/friendMsgs')


/*
* 上传文件接口
* 请求:{file:文件对象}
* 响应:{'code':2000,'msg':'ok',url:文件存储后的url}
* */
export const upload=(data)=>axios.upload('/api/v1/upload',data)
