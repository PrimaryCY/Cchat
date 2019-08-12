<template>
	<div class="chat">
			<van-nav-bar :title="nowRoom.name"
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
<!--		<Loading v-if="loading.chatRooms" :text="'获取信息中...'"></Loading>-->
			<div ref="scroll" :toBottom="true"  class="scroll-wrap" :data="historyMsg">
				<ul >
					<li v-for="(item,index) in historyMsg" :key="item.id"
							:class="{'chat-right':item.user_id == user.id,
              'chat-left':item.user_id != user.id,
              'chat-box':true}">
						<div class="add-time">
							<span>{{item.create_time}}</span>
						</div>
						<div :class="{'toright':item.user_id == user.id,'flex':true}">
              <span v-if="item.user_id != user.id" class="avater">
                <img :src="item.user.portrait"/>
              </span>
							<span class="content">{{item.msg}}</span>
							<span v-if="item.user_id == user.id" class="avater">
                <img :src="user.portrait"/>
              </span>
						</div>
						<div class="author" :class="{right:item.user_id==user.id}">
							<span class="web-font-min">{{item.user.userName}}</span>
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
					<van-button type="info" @click.prevent="sendMsg">
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
	import Scroll from 'better-scroll'

  export default {
    name: "chatDetail",
		data(){
      return {
				input:{								//输入
				  info:''			//用户当前输入
				},
				historyMsg:this.$store.state[this.$store.state.nowRoom.id]
			}
		},
		computed:{
      ...mapState(['nowRoom','user'])
		},
		watch:{
      historyMsg(){
        this.$nextTick(()=>{
          this._initScroll()
          this._scrollToEnd()
				})
			}
    },
		mounted() {
      if(!this.nowRoom.name){
        this.$router.replace('/msg')
			}
			this._initScroll()
    },
		methods:{
      _initScroll() {
        this.bs=new Scroll('.scroll-wrap',{click:true})
        this.bs.on('scroll',(pos)=>{
          if(pos.y > 30){
            this.pulldownMsg = '释放立即刷新'
          }
        })
				this._scrollToEnd()
      },
			_scrollToEnd(){
        this.bs.scrollTo(0,this.bs.maxScrollY,800)
			},
      //发送新消息
      sendMsg(){
        console.log('发送')
        if(!this.input.info) return
        console.log('sssss')
				let data={
          msg:this.input.info,
					room_id:this.nowRoom.id
				}
        this.$socket.emit('NEWMESSAGE',data,(flag)=>{
           	this.$toast('发送成功!')
            this.input.info=''
						this._scrollToEnd()
				})
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
