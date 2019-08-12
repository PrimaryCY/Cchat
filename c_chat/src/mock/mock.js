import Mock from 'mockjs'

Mock.setup({
  timeout: '2000-4000'
})

function Api(uri){
  return new RegExp("http:\/\/127.0.0.1:5000\/"+uri)
}

import loginMock from './login'
import userMock from './user'

Mock.mock(Api('code'),'post',{})
Mock.mock(Api('login'),'post',loginMock.post)
Mock.mock(Api('login'),'delete',loginMock.delete)

//用户  crud
Mock.mock(Api('user'),'get',userMock.get)
Mock.mock(Api('user'),'post',userMock.post)
Mock.mock(Api('user'),'put',userMock.put)

