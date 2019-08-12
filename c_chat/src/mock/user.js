import Mock from 'mockjs'

const random = Mock.Random // Mock.Random 是一个工具类，用于生成各种随机数据

let user={}

function get() {
  let data={
    code:'2000',
    msg:'ok',
    data:{userName:'907031027',
      age:random.integer(12,80),
      money:random.float(0,1000,0,1),
      nickName:random.cname(),
      email:'90703107@qq.com'
    }
  }
  return data
}

function post(){
  let data={
    code:'2000',
    msg:'ok',
    data:{
      token:'dwdjkdanejksnadnad'
    }
  }
  return data
}

function put(){
  return  {
    code:'2000',
    msg:'ok',
    data:{userName:'修改后的',
      age:random.integer(12,80),
      money:random.float(0,1000,0,1),
      nickName:random.cname(),
      email:'90703107@qq.com'
    }
  }
}



user.get=get()
user.post=post()
user.put=put()
export default user
