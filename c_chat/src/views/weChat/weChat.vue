<template>
	<section>
			<van-nav-bar title="群聊"
									 border
			/>
		<Loading v-if="loading.chatRooms" :text="'获取信息中...'"></Loading>
		<div class="wrap">
			<van-grid clickable :column-num="2"
				border
			>
				<van-grid-item
								icon="home-o"
								text="创建聊天室"
								@click="clickCreateRoom"
				/>
				<van-grid-item
								icon="search"
								text="搜索聊天室"
								url="https://www.baidu.com"
				/>
			</van-grid>

			<van-divider>翻开扑克牌点击就能加入聊天室!</van-divider>

			<van-pull-refresh v-model="loading.pullRefresh"
												@refresh="onRefresh">

			<ul class="card-list clearfix">
				<li class="card" v-for="(room,index) in chatRooms" :key="room.id">
					<div class="card-face">
						<img :src="$settings.ROOM_BACKDEFALT">
					</div>
					<div class="card-back" @click="retrieveChatRoom(room)">
						<img :src="room.img">
					</div>
					<span class="card-text web-font-mid">{{room.name}}</span>
				</li>
			</ul>

			</van-pull-refresh>
			<van-popup round v-model="chatRoom" @click.stop>
				<div class="popup">
					<van-loading v-if="loading.retrieveChatRoom" type="spinner" >
						正在加载中
					</van-loading>
					<div class="room_info">
						<div  class="room-header">
							<img :src="nowChatRoom.img">
						</div>
						<div class="room-content">
							<h1 class="h1">{{nowChatRoom.name}}</h1>
							<div class="web-font-min">
								{{nowChatRoom.desc}}
							</div>
							<div class="web-font-mid info">
								<span class="first-span">
									房主:{{nowChatRoom.founder}}
								</span>
								&nbsp;
								&nbsp;
								&nbsp;
								<span >
									当前房间活跃人数:{{nowChatRoom.nums}}人&nbsp;&nbsp;&nbsp;&nbsp;</span>
							</div>
						</div>
						<div class="room-footer">
							<a  v-if="!inTheRoom" href="#" class="button button-3d button-caution " @click.prevent="joinRoom">
								{{loading.btnLoading?'...加入中':'加入聊天室 >'}}
							</a>
							<div v-else>
								<a  href="#" class="button button-3d button-caution button-extra" @click.prevent="leaveRoom">
									{{loading.btnLeaveRoom?'...离开中':'离开聊天室 >'}}
								</a>
								<a  href="#" class="button button-3d button-caution button-extra2" @click.prevent="joinRoom">
									{{loading.btnLoading?'...加入中':'加入聊天室 >'}}
								</a>
							</div>
						</div>
					</div>
				</div>
			</van-popup>
		</div>

	</section>
</template>

<script>
	import {mapState} from 'vuex'
	import {NavBar} from 'vant'

	import {getChatRooms} from '../../api/index'
  import Loading from '../../components/common/loading/loading'

  export default {
    name: "weChat",
		data(){
      return {
        chatRoom:null,											//是否显示房间弹窗
				nowChatRoom:{},										//当前浏览的房间信息
				loading:{														//加载状态
          all_chatRooms:false,		//聊天室列表页加载状态
					retrieveChatRoom:false,	//聊天室详情页面加载状态
          pullRefresh:false, //下拉刷新
					btnLoading:false,		//加入房间时
          btnLeaveRoom:false	//离开聊天室
				},
				chatRooms:[],   			   //聊天室列表
			}
		},
		components:{
      [NavBar.name]:NavBar,
			Loading
		},
		computed:{
			...mapState(['user','roomList']),
      inTheRoom(){
        let res=this.roomList.indexOf(this.nowChatRoom.id)
        return !(res<0)
      }
		},
		async created() {
     	await this._recrieveChatRooms()
    },

		methods:{
      //获取聊天室数据
      async _recrieveChatRooms(){
        this.loading.all_chatRooms=true
        let res = await getChatRooms({order_by:'-nums'})
        if(res.data.code==='2000'){
          this.chatRooms=res.data.data
        }else {
          this.$toast('网络错误!请重试!')
        }
        this.loading.all_chatRooms=false
			},
      //点击创建聊天室时
      clickCreateRoom(){
				if(this.user.userName==='匿名') return this.$dialog.alert({
          message: '必须登录之后才可以创建聊天室!'
        })
				this.$router.push('/createRoom')
			},
			//点击进入房间详情时
			async retrieveChatRoom(room){
        this.chatRoom=this.loading.retrieveChatRoom=true
				let res=await getChatRooms({},room.id)
				if(res.data.code==='2000'){
					this.nowChatRoom=res.data.data
					this.nowChatRoom.nums=room.nums
				}else {
          this.$toast(res.data.msg)
        }
				this.loading.retrieveChatRoom=false
			},
			//加入聊天室
			joinRoom(){
        this.loading.btnLoading=true
				if(!this.inTheRoom){
					this.$socket.emit('JOINROOM',this.nowChatRoom,(res)=>{
						if(res){
						  this.$store.dispatch('SOCKET_ROOMLIST',this.nowChatRoom.id)
						}
					})
				}
        this.$store.dispatch('receive_nowRoom',this.nowChatRoom)
        this.$router.push('/ChatDetail')
				this.loading.btnLoading=false
			},
			//离开聊天室
      leaveRoom(){
        this.loading.btnLoading=true
        if(this.inTheRoom){
          this.$socket.emit('LEAVEROOM',this.nowChatRoom,(res)=>{
            if(res){
              let index=this.roomList.indexOf(this.nowChatRoom.id)
							if(index>=0){
                let  newRoomList=Array.prototype.slice.call(this.roomList)
                newRoomList.splice(index,1)
                this.$store.dispatch('SOCKET_ROOMLIST',newRoomList)
								this.$toast('离开成功!')
							}
            }
          })
        }
        this.$store.dispatch('receive_nowRoom',this.nowChatRoom)
        this.loading.btnLoading=false
			},
			//下拉刷新
      async onRefresh () {
				await this._recrieveChatRooms()
				this.loading.pullRefresh=false
      },
		}
  }
</script>

<style scoped lang="scss">
	.button-extra2{
		width: 50%!important;
	}
	.button-extra{
		background-color: #1B9AF7;
		width: 50%!important;
		box-shadow: 0 0.18667rem 0 #0880d7,
	}
	.van-loading {
		font-size: 0;
		width: 100%;
		height: 100%;
		text-align: center;
		padding-top: 50%;
	}
	.web-font-mid {
		font-size: 0.32667rem;
	}

	.card-text{
		position: fixed;
		bottom: 0;
		width: 100%;
		right: 0;
	}
	.popup{
		width: 320px;
		height: 11.8rem;
		overflow: hidden;
		.room_info{
			height: 100%;
			width: 100%;
			.room-header{
				width: 100%;
				height: 70%;
				text-align: center;
				margin-top: 5px;
				img{
					object-fit: contain;
				}
			}
			.room-content{
				height: 20%;
				text-align: center;
				.h1{
					margin-bottom: 6px;
				}
				div{
					width: 100%;
					height: 0.98rem;
					text-indent: 50px;
					text-align: -webkit-auto;
					text-align: initial;
					overflow: hidden;
					margin-bottom: 6px;
				}
				.info{
					text-indent: 0;
					text-align: justify;
					text-align-last: justify;

				}

			}
			.room-footer{
				text-align: center;
				height: 10%;
				a{
					width: 100%;
					height: 33px;
					font-size: medium
				}
			}
		}
	}
	img{
		width: 100%;
		height: 100%;
	}
	ul, li {margin: 0;padding: 0;list-style: none;}
	.clearfix {*zoom: 1;}
	.clearfix:after {display: table;content: '';clear: both;}
	.wrap{
		/*margin-top: 46px;*/
	}
	.card-list .card {
		text-align: center;
		float: left;
		position: relative;
		margin-left: 0.43333rem;
		margin-top: 0.3333rem;
		width: 2.75rem;
		height: 4.5rem;
		-webkit-perspective: 600px;
		-moz-perspective: 600px;
		-ms-perspective: 600px;
		perspective: 600px;
	}

	.card-list .card-face,
	.card-list .card-back {
		position: absolute;
		left: 0;
		top: 0;
		-webkit-transition: all 0.5s ease-in-out;
		-o-transition: all 0.5s ease-in-out;
		transition: all 0.5s ease-in-out;
		-webkit-transform-style: perspective-3d;
		-moz-transform-style: perspective-3d;
		-ms-transform-style: perspective-3d;
		transform-style: perspective-3d;
		-webkit-backface-visibility: hidden;
		-moz-backface-visibility: hidden;
		-ms-backface-visibility: hidden;
		backface-visibility: hidden;
	}

	.card-list .card-face {
		z-index: 2;
	}

	.card-list .card-back {
		z-index: 1;
		-webkit-transform: rotateY(-180deg);
		-ms-transform: rotateY(-180deg);
		-o-transform: rotateY(-180deg);
		transform: rotateY(-180deg);
	}

	.card-list .card:hover .card-face {
		z-index: 1;
		-webkit-transform: rotateY(-180deg);
		-ms-transform: rotateY(-180deg);
		-o-transform: rotateY(-180deg);
		transform: rotateY(-180deg);
	}

	.card-list .card:hover .card-back {
		z-index: 2;
		height: 144px;
		-webkit-transform: rotateY(0);
		-ms-transform: rotateY(0);
		-o-transform: rotateY(0);
		transform: rotateY(0);
	}
</style>
