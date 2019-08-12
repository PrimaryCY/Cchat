<template>
  <div>
  <van-nav-bar
          border
          :title="nowRoom.name"
          left-text="返回"
          left-arrow
          @click-left="$router.back()"/>
  <div class="room-detail">

    <div class="title-img" >
      <van-image fit="scale-down"
                 :src=nowRoom.img
                 click="imgClick" />
    </div>

      <van-cell-group>
        <van-cell>
          <!--        <div class="goods-title">{{ nowRoom.name }}</div>-->
          <div class="goods-price">{{ nowRoom.desc }}</div>
        </van-cell>
        <van-cell class="goods-express">
          <van-col span="8">加入总人数：{{ nowRoom.nums }}</van-col>
          <van-col span="8">创始人：{{ nowRoom.founder }}</van-col>
          <van-col span="8">当前在线人数: {{nowRoom.nums}}人</van-col>
        </van-cell>
      </van-cell-group>

      <van-cell-group class="goods-cell-group">
        <van-cell value="进入店铺" icon="shop-o" is-link click="sorry">
          <div slot="title">
            <span class="van-cell-text">{{nowRoom.name}}</span>
            <van-tag class="goods-tag" type="danger">官方</van-tag>
          </div>
        </van-cell>
        <van-cell title="线下门店" icon="location-o" is-link click="sorry" />
      </van-cell-group>


      <div v-for="(users,index) in userList" :key="index" class="van-cols">
        <van-col span="5" v-for="(user,index) in users" :key="user.id" class="col" >
          <div  class="col-div" @click="showInfo(user)">
            <img :src="user.portrait" >
            <span class="web-font-min">{{user.userName}}</span>
          </div>
        </van-col>
      </div>

  <friend-info v-model="show" :nowUser="nowUser"></friend-info>


  </div>
  </div>
</template>
<script>
  import {mapState} from 'vuex'

  import {getChatRoomUsers} from '../../api/index'

	import friendInfo from '../../components/friendInfo/friendInfo'

  export default {
    data(){
      return {
        userList: [],         //当前聊天室的好友,二维数组
        show:false,            //展示用户信息
        nowUser:{}            //当前查看的用户
      }
    },
    computed:{
      ...mapState(['nowRoom','user'])
    },
    async mounted() {
      //获取好友列表
      if(!this.nowRoom.id){
        this.$router.replace('/weChat')
      }else{
        let  res=await getChatRoomUsers({'id':this.nowRoom.id})
        if(res.data.code==='2000'){
            this.userList=res.data.data
        }else{
          this.$toast(res.data.msg)
        }
      }
    },
    methods:{
      //展示用户详细信息
      async showInfo(user){
        //判断当前用户是否为匿名用户
        if(this.user.userName==='匿名'){
          let alert=await this.$dialog.confirm({
            message:'匿名用户无详细信息!请登录!',
            confirmButtonText:'去登录!',
            closeOnClickOverlay:true
          }).catch(()=>{})
          if(alert){
            this.$router.push('/login')
          }
        }else{
          this.nowUser=user
          this.show=true
        }
      }
    },
    components:{
      friendInfo
    }
  }

</script>
<style scoped lang="scss">
  .room-detail{
    //height: 500px;
    overflow-y: auto;
    width: 100%;
    max-height: 617px;
  }
  .title-img{
    text-align: center;
    margin-top: 1px;
    overflow: hidden;
    width: 100%;
    height: 8rem;
    .van-image{
      width: 100%;
      height: 100%;
    }
  }
  .van-cols{
    margin-left: 0.7rem;
    /*height: 2.06667rem;*/
    .col {
      margin: 3px;
      .col-div {
        /*height: 40px;*/
        margin: 10px;
        img {
          height: 100%;
          width: 100%;
          object-fit: cover;
        }
        span{
          display: flex;
        }
      }
    }
  }
</style>

<style scoped lang="less">
  .goods {
    padding-bottom: 50px;
    &-swipe {
      img {
        width: 100%;
        display: block;
      }
    }
    &-title {
      font-size: 16px;
    }
    &-price {
      color: #f44;
      text-indent: 20px;
    }
    &-express {
      color: #999;
      font-size: 12px;
      padding: 5px 15px;
    }
    &-cell-group {
      margin: 15px 0;
      .van-cell__value {
        color: #999;
      }
    }
    &-tag {
      margin-left: 5px;
    }
  }
</style>
