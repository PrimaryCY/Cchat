import Mock from 'mockjs'

const Random = Mock.Random // Mock.Random 是一个工具类，用于生成各种随机数据

let goods={}

function get() {
  let data=[]
  for (let i = 0; i < 10; i++) {
    let obj={
      name: Random.name(), // 生成姓名
      rating: Random.integer(1,5),
      recent_order_num:Random.integer(50,1000),
      float_minimum_order_amount:Random.integer(0,100),
      float_delivery_fee:Random.integer(0,100),
      supports:[],
    }
    for (let j = 0; j < Random.integer(1,3); j++) {
      obj.supports.push({icon_name:Random.cfirst()})
    }
    data.push(obj)
  }
  return data
}

goods.get=get()
export default goods
