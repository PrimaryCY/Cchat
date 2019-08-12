<template>
	<van-popup
					v-model="newShow"
					round
					position="bottom"
					:style="{ height: '70%' }"
	>
		<loading v-if="loading"></loading>
		<div class="global">
		<div class="userInfo">
			<div class="userInfo-title">
				<img :src="nowUser.portrait">
					<h1>用户名:{{nowUser.userName}}</h1>
			</div>
			<div class="userInfo-content">
				<p>
					<span>
						地区:{{userArea}}
					</span>
					<span>
						年龄:{{userAge}}
					</span>
					<span>
						性别:{{userSex}}
					</span>
				</p>
			</div>

			<!-- 上边框 -->
			<div class="van-hairline--top line"></div>
			<div class="userInfo-btn">
				<div v-if="nowUser.id!==user.id">
<!--					<div>-->
<!--						<van-button plain type="danger" round>删除好友</van-button>-->
<!--					</div>-->
					<div>
						<van-button v-if="!nowUser.is_friend"
												plain size="large"
												round type="primary"
												@click.prevent="addFriend">申请添加好友</van-button>
						<van-button v-if="nowUser.is_friend"
												plain size="large"
												round type="primary"
												@click.prevent="goFriendChat(nowUser)">去聊天</van-button>
					</div>
				</div>
			</div>
		</div>
		</div>
	</van-popup>
</template>

<script>
	import {mapState} from 'vuex'

  import areaList from '../../common/area'
	import {postFriend} from '../../api/index'
	import loading from '../../components/common/loading/loading'
  import Loading from "../common/loading/loading"

  export default {
    name: "friendInfo",
    components: {Loading},
		data(){
      return {
        loading:false
      }
		},
    model: {
      //从父组件v-model接收过来的值
      prop: 'show',
    },
		props:['show','nowUser'],
		computed:{
      ...mapState(['user']),
      newShow:{
        get(){
          return this.show
				},
				set(value){
					this.$emit('input',value)
				}
			},
			//获取用户地区
			userArea(){
        if(!this.nowUser.province) return '未填写'
        else {
          let home
          let pro=areaList.province_list[this.nowUser.province]
          let city=areaList.city_list[this.nowUser.city]
          if (this.nowUser.home){
            home=areaList.county_list[this.nowUser.home]
          }
          return `${pro}-${city}-${home?home:''}`
        }
			},
			//获取用户年龄
			userAge(){
        let userBirth=new Date(this.nowUser.birth)
				return (new Date().getFullYear()-userBirth.getFullYear())
			},
			//获取用户性别
			userSex(){
        switch (this.nowUser.sex) {
					case "woman":
					  return '女'
					case "man":
					  return '男'
					default:
					  return '保密'
        }
			},
		},
		methods:{
      async addFriend(){
        this.loading=true
				setTimeout(()=>{
				  this.loading=false
				},10000)

        let data={friend_id:this.nowUser.id}
				let res=await postFriend(data)
				if(res.data.code==='2000'){
					this.$toast('申请成功!请等待好友申请通过!')
				}else {
				  this.$toast(res.data.msg)
				}
        this.newShow=false
				this.loading=false
			},
      goFriendChat(nowUser){
        this.$store.dispatch('receive_nowUser',nowUser)
				this.$router.push('/friendChatDetail')
      }
		},
		component: {
      loading
    }
  }
</script>

<style scoped lang="scss">
	.global{
		height: 100%;
	}
.userInfo{
	background-color: aliceblue;
	height: 100%;
	overflow-y: hidden;
	.userInfo-title{
		height: 70%;
		margin: 7px;
		img{
			width: 100%;
			height: 90%;
			object-fit: cover;
		}
		h1{
			text-align: center;
		}
	}
	.userInfo-content{
		margin: 10px;
		p{
			font-size: 12px;
			display: flex;
			justify-content: space-around;
		}
	}
	.line{
		width: 100%;
		margin-top: 10px;
		height: 10px;
	}
	.userInfo-btn{
		margin: 10px 30px;
	}
}
</style>
