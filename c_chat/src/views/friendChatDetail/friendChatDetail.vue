<template>
	<div class="chat">
			<van-nav-bar :title="nowUser.user.remark"
									 border
									 left-text="返回"
									 left-arrow
									 @click-left="$router.back()"
			>
				<svg class="icon-min"
						 aria-hidden="true"
						 slot="right"
						 @click="$router.push('/roomDetail')">
					<use xlink:href="#icon-guanyu" />
				</svg>
			</van-nav-bar>
		<Loading v-if="isLoading" :text="'获取信息中...'"></Loading>
			<div ref="scroll" :toBottom="true"  class="scroll-wrap" :data="friendHistoryMsg">
				<ul >
					<li v-for="(item,index) in friendHistoryMsg" :key="item.id"
							:class="{'chat-right':item.from_user_id == user.id,
              'chat-left':item.from_user_id != user.id,
              'chat-box':true}">
						<div class="add-time">
							<span>{{item.create_time}}</span>
						</div>
						<div :class="{'toright':item.from_user_id == user.id,'flex':true}">
              <span v-if="item.from_user_id != user.id" class="avater">
                <img :src="nowUser.portrait"/>
              </span>
							<span class="content">{{item.msg}}</span>
							<span v-if="item.from_user_id == user.id" class="avater">
                <img :src="user.portrait"/>
              </span>
						</div>
						<div v-if="item.from_user_id==user.id" class="author" :class="{right:item.from_user_id==user.id}">
							<span class="web-font-min">{{user.userName}}</span>
						</div>
						<div v-else class="author" :class="{right:item.from_user_id==user.id}">
							<span class="web-font-min">{{nowUser.userName}}</span>
						</div>
					</li>
				</ul>
			</div>
		<div class="footer">
			<van-row >
				<van-col  span="18">
					<van-field  v-model="input.info" placeholder="请输入信息" />
				</van-col>
				<van-col  span="6">
					<van-button type="info" @click.prevent="sendMsg"
											:loading="btnLoading"
					>
						发送
					</van-button>
				</van-col>
			</van-row>
		</div>
			</div>
</template>

<script>
	import {mapState} from 'vuex'

  import Loading from '../../components/common/loading/loading'
	import {postFriendMsg} from '../../api/index'
	import Scroll from 'better-scroll'

  export default {
    name: "friendChatDetail",
		data(){
      return {
        isLoading:false,			//获取历史记录等待
				input:{								//输入
				  info:''			//用户当前输入
				},
				btnLoading:false,						//发送消息等待
			}
		},
		components:{
      Loading
		},
		computed:{
      ...mapState(['nowUser','user','friendHistoryMsg'])
		},
		watch:{
      friendHistoryMsg(){
        this.$nextTick(()=>{
          this._initScroll()
          this._scrollToEnd()
				})
			}
    },
		mounted() {
      if(!this.nowUser.userName){
        this.$router.replace('/msg')
				return
			}
			this._initHistoryMsg()
    },
		methods:{
      //获取历史聊天记录
      async _initHistoryMsg(){
        this.isLoading=true
				setTimeout(()=>{
				  this.isLoading=false
				},10000)
       	this.$store.dispatch('receive_friend_history',
					{room:this.nowUser.user.room,
						cb: ()=>this.isLoading=false})
			},
      _initScroll() {
        this.bs=new Scroll('.scroll-wrap',{click:true})
				this._scrollToEnd()
      },
			_scrollToEnd(){
        this.bs.scrollTo(0,this.bs.maxScrollY,800)
			},
      //发送新消息
      async sendMsg(){
        console.log('发送')
				this.btnLoading=true
				setTimeout(()=>{
				  this.btnLoading=false
				},10000)
        if(!this.input.info) return
				let data={
          msg:this.input.info,
					room:this.nowUser.user.room,
					type:1,
					to_user_id:this.nowUser.id,
				}
       	let res=await postFriendMsg(data)
				if(res.data.code==='2000'){
				  this.$store.state.friendHistoryMsg.push(res.data.data)
				}else{
				  this.$toast(res.data.msg)
				}
        this.btnLoading=false
			}
		},
  }
</script>

<style scoped lang="scss">
	.author{
		display: block;
		margin: 0 7px;
		&.right{
			text-align: right;
		}
	}
	.van-button--normal {
		padding: 0px 0.46rem;
		font-size: 0.37333rem;
	}
	.van-loading {
		font-size: 0;
		/*width: 100%;*/
		/*height: 100%;*/
		text-align: center;
		padding-top: 50%;
	}
	.web-font-mid {
		font-size: 0.32667rem;
	}
	.chat{
		position: absolute;
		width: 100%;
		.scroll-wrap{
			overflow:hidden;
			max-height:572px;
			margin-bottom: 3px;
			/*margin-bottom:50px;*/
		}
		.footer{
			bottom: 2px;
			position: fixed;
			width: 99%;
			border: 1px solid black;
			border-radius: 4px;
			button{
				width: 100%;
			}
		}
	}


</style>

<style lang="less" scoped>
		.chat-box {
			width: 100%;
			margin-bottom: 10px;
			.add-time {
				margin: 0 auto;
				text-align: center;
				font-size: 14px;
				line-height: 1.5rem;
				height: 1.5rem;
				span {
					background-color: rgba(172, 172, 177, 0.29);
					color: white;
					border-radius: 5px;
					padding: 2px 5px;
				}
			}
			.flex {
				display: flex;
			}
			.avater {
				margin: 0 10px;
				width: 40px;
				height: 40px;
				img {
					width: 100%;
					border-radius: 50%;
					object-fit: cover;
					height: 100%;
				}
			}
			.content {
				max-width: 220px;
				background-color: greenyellow;
				line-height: 25px;
				padding: 7px 1rem;
				overflow-wrap: break-word;
				word-break: break-all;
				border-radius: 10px;
			}
		}
		.chat-right {
			.flex {
				align-items: center;
				justify-content: flex-end
			}
			.toright {
				span {
				}
			}
			.content {
				background-color: orange;
				color: white;
			}
		}
</style>
