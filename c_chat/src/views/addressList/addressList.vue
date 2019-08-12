<template>
	<div style="min-height: 620px">
		<van-nav-bar
						title="好友列表"
						border
		/>
		<div class="group-wrap">
				<ul class="van-index-bar__sidebar" >
					<li class="van-index-bar__index web-font-mid" v-for="(key,index) of friendsDictKey"
							:key="index"  @click="moveTo(index)" :class="{current:index===currentIndex}">
						{{key}}
					</li>
				</ul>
		</div>
		<div class="wrap" :toBottom="true" >
			<div>
			<loading v-if="globalLoading" text="加载中"></loading>
			<!--			下拉刷新-->
			<van-pull-refresh v-model="isLoading" @refresh="onRefresh" ref="pull">
				<div ref="friend">
					<ul >
					<li class="friend-group"v-for="(friend,index) of friendsDictKey" :key="index">
					<h1 class="web-font-mid group-title">{{friend}}</h1>
					<ul>
						<li v-for="(f,index) in friendsDict[friend]"  :key="f.id">
							<van-cell
											:clickable="true"
											size="large"
											@click="showInfo(f)"
							>
								<div slot="title" class="title">
									<van-image
													fit="cover"
													round
													width="35"
													height="35"
													:src="f.portrait"
									/>
									<span class="text">{{f.user.remark}}</span>
								</div>

							</van-cell>
						</li>
					</ul>
				</li>
					</ul>
				</div>
			</van-pull-refresh>
		</div>
		</div>
		<friend-info v-model="show" :nowUser="nowUser"></friend-info>
	</div>
</template>

<script>
	import Scroll from 'better-scroll'

	import loading from '../../components/common/loading/loading'
	import {getFriends} from '../../api/index'
	import friendInfo from '../../components/friendInfo/friendInfo'

	export default {
    name: "addressList",
		data(){
      return {
        globalLoading:false,			//全局刷新
				isLoading:false,						//下拉刷新
				scrollX:0,
				scrollY:0,
				friendGroups:[],						//好友分组y轴坐标
				friendsDict:{},							//好友数据
				nowUser:{},									//用户当前查看的好友
				show:false,									//是否展示好友信息组件
			}
		},
		components:{
      loading,
			friendInfo
		},
		methods:{
      //获得初始数据
			async _initFriendsDict(){
			  this.globalLoading=true
				let res=await getFriends()
				if(res.data.code==='2000'){
				  this.friendsDict=res.data.data
				}else{
				  this.$toast('网络错误!请刷新重试!')
				}
				this.globalLoading=false
				setTimeout(()=>{
				  this.globalLoading=false
				})
			},
      _initScroll() {
        this.bs=new Scroll('.wrap',{click:true})
        //绑定滑动事件监听
        this.bs.on('scroll',({x,y})=>{
          console.log(y)
          this.scrollY=Math.abs(y)
        })
        //绑定滑动停止的监听,解决惯性滑动bug
        this.bs.on('scrollEnd',({x,y})=>{
          this.scrollY=Math.abs(y)
        })
      },
      //初始化tops
      _initTops(){
        let top=0
        //获取所有的分类标题的位置
        const arrli=this.$refs.friend.getElementsByClassName('friend-group')
        this.friendGroups.push(top)     //添加第一个元素
        Array.prototype.slice.call(arrli).forEach(item=>{
          top += item.clientHeight
          this.friendGroups.push(top)
        })
      },
      //点击元素滚动到指定位置
      moveTo(index){
        let y=this.friendGroups[index]
        this.scrollY=y
        this.bs.scrollTo(0,-y,500)
      },
      //下拉刷新
      async onRefresh() {
        this.isLoading=true
      	setTimeout(()=>{
      	  this.$toast('刷新成功!')
      	  this.isLoading=false
				},1000)
      },
      //展示用户详细信息
      showInfo(user){
				this.nowUser=user
				this.show=true
      }
		},
		mounted() {
      this._initFriendsDict()
    },
		computed:{
      //获取所有好友字典中的key值,因为vue自动帮我取值不给我key,没办法只能这么做
      friendsDictKey(){
        let a=[]
				for (let i in this.friendsDict){
				  a.push(i)
				}
				return a
			},
      //计算当前滚动在friendGroups中的下标位置
      currentIndex(){
        const index=this.friendGroups.findIndex((top,index)=>{
          let t=top-13
          let i=this.friendGroups[index+1]-13
          return this.scrollY>t&&this.scrollY<i
        })
        return index
      },
		},
		watch:{
      friendsDict(){
        this.$nextTick(()=>{
          this._initScroll()
          this._initTops()
				})
			}
		}
  }
</script>


<style scoped lang="scss">
	.current{
		color: red!important;
	}
	.van-pull-refresh {
		min-height: 500px;
	}
	.group-title{
		background-color: #e5e5e5;
		padding-left: 10px;
		color: #969799;
	}
	.van-index-bar__sidebar {
		right: 5px;
		top: 45% !important;
	}
	.group-wrap{
		position: fixed;
		right: 0px;
		line-height: 100%;
		text-align: center;
		z-index: 1;
	}
	/deep/ .van-pull-refresh__track{
		height: 100%;
	}
	.wrap {
		overflow: hidden;
		max-height: 570px;
		margin-bottom: 3px;
	}
	.title{
		.text{
			float:left;
			line-height:35px;
			margin-left: 10px;
		}
		.van-image{
			float: left;
		}
	}
	.btn{
		height: 0.66667rem;
		margin-top: 2px;
	}
</style>
