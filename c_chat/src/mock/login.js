import Mock from 'mockjs'

const random = Mock.Random // Mock.Random 是一个工具类，用于生成各种随机数据

let login={}

function post() {
    return  {
      code:'2000',
      msg:'ok',
      data:{
        token:'tokens2w12e21e',
        user:{
          userName:'修改后的',
          age:random.integer(12,80),
          money:random.float(0,1000,0,1),
          nickName:random.cname(),
          email:'90703107@qq.com'
        },
      }
    }
}

function del(){
  return {
    code:'2000',
    msg:'ok'
  }
}


login.post=post()
login.delete=del()
export default login

