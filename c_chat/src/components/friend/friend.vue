<template>
	<div class="wrap" :toBottom="true" >
		<div>
			<Loading v-if="globalLoading" text="加载中"></Loading>

				<ul>
					<li class="msg" v-for="(item,index) in friendMsgList " :key="item.id" @click="goToFirendChat(item.user.friend_id)">
						<van-cell  clickable
											 border
						>
							<div slot="default" class="content">
								<p class="web-font-mid username">{{item.user.remark}}</p>
								<p class="web-font-min msg">{{item.msg}}</p>
							</div>
							<div slot="icon" class="portrait">
								<img :src="item.user.user.portrait">
							</div>
							<div slot="right-icon">
								<van-tag type="danger"
												 mark
								>标签
								</van-tag>
							</div>
						</van-cell>
					</li>
				</ul>
		</div>
		<friend-info v-model="show" :nowUser="nowUser"></friend-info>
	</div>
</template>

<script>
  import Scroll from 'better-scroll'
	import {mapState} from 'vuex'

  import Loading from "../../components/common/loading/loading";
  import friendInfo from '../../components/friendInfo/friendInfo'
  import {retrieveFirends} from '../../api/index'

  export default {
    name: "friend",
    components:{
      Loading,
			friendInfo
    },
    data(){
      return {
        globalLoading:false,							//全局加载
				show:false,												//是否展示好友资料
				nowUser:{}												//好友资料中的好友信息
      }
    },
    mounted() {
      this.globalLoading=true
			setTimeout(()=>{
			  this.globalLoading=false
			},10000)
      this.$store.dispatch('receive_friend_msg_list', ()=>{
          this.globalLoading=false
			})
    },
    methods:{
      _initScroll() {
        this.bs=new Scroll('.wrap',{click:true})
      },
      async goToFirendChat(id){
				let res=await retrieveFirends(id)
				if(res.data.code==='2000'){
          this.nowUser=res.data.data
          this.show=true
				}else {
				  this.$toast(res.data.data)
				}
			}
    },
    watch:{
      //数据发生变化及时更新scroll
      friendMsgList(){
        this.$nextTick(()=>{
          this._initScroll()
        })
      }
    },
		computed:{
      ...mapState(['friendMsgList'])
		},

  }
</script>


<style scoped lang="scss">
	.wrap{
		overflow: hidden;
		max-height:523px;
		margin-bottom: 3px;
	}
	.portrait{
		width: 15%;
		img{
			width: 100%;
			height: 100%;
			object-fit: cover;
			border-radius: 50%;
		}
	}
	.content{
		margin-left: 10px;
		.username{

		}
		.msg{
			color: #7e8c8d;
		}
	}
</style>
