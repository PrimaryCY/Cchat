<template>
	<div class="wrap" :toBottom="true" >
		<div>
			<Loading v-if="globalLoading" text="加载中"></Loading>
<!--			下拉刷新-->
			<van-pull-refresh v-model="isLoading" @refresh="onRefresh">

		<ul>
			<li v-for="(apply,index) in fApplyList" :key="apply.id">
				<van-cell
								:clickable="true"
								size="large" >
					<div slot="title" class="title">
						<van-image
										fit="cover"
										round
										width="35"
										height="35"
										:src="apply.user.portrait"
						/>
						<span class="text">{{apply.user.userName}}</span>
					</div>
					<van-button v-if="apply.status===0"
											type="danger"
											slot="default"
											size="mini"
											class="btn"
											disabled
					>
						已拒绝
					</van-button>
					<van-button v-if="apply.status===1"
											type="primary"
											slot="default"
											size="mini"
											class="btn"
											disabled
					>
						已同意
					</van-button>
					<van-button v-if="apply.status===3"
											type="primary"
											slot="default"
											size="mini"
											class="btn"
											disabled
					>
						已忽略
					</van-button>
					<div v-if="apply.status===2" slot="default">
						<van-button
												type="info"
												size="mini"
												class="btn"
												@click="postApply(apply,1)"
						>
							同意
						</van-button>
						<van-button
										type="info"
										size="mini"
										class="btn"
										@click="postApply(apply,0)"
						>
							拒绝
						</van-button>
						<van-button
										type="warning"
										size="mini"
										class="btn"
										@click="postApply(apply,3)"
						>
							忽略
						</van-button>
					</div>

				</van-cell>
			</li>
		</ul>
			</van-pull-refresh>
		</div>
	</div>
</template>

<script>
	import Scroll from 'better-scroll'

  import {getFriendCheck, postFeedback, postFriednCheck} from '../../../api/index'
  import Loading from "../../../components/common/loading/loading";

  export default {
    name: "fApply",
		components:{
      Loading
		},
		data(){
      return {
        globalLoading:false,							//全局加载
				isLoading:false,						//下拉刷新加载
				fApplyList:[],								//审核数据
			}
		},
		mounted() {
			this._initFAppplyList()
    },
		methods:{
      //初始化请求数据
			async _initFAppplyList(){
			  this.globalLoading=true
			  let params={type:0}
			  let res=await getFriendCheck(params)
				if (res.data.code==='2000'){
				  this.fApplyList=res.data.data
				}else{
				  this.$toast('网络请求错误!请刷新重试')
				}
				this.globalLoading=false
				setTimeout(()=>{
				  this.globalLoading=false
				},1000)
			},
      _initScroll() {
        this.bs=new Scroll('.wrap',{click:true})
        this.bs.on('scroll',(pos)=>{
          if(pos.y > 0){
            this.bs.closePullUp()
          }
        })
      },
			//下拉刷新
      async onRefresh() {
        let params={type:0}
        let res=await getFriendCheck(params)
        if (res.data.code==='2000'){
          this.fApplyList=res.data.data
          this.$toast('刷新成功');
        }else{
          this.$toast('网络请求错误!请刷新重试')
        }
        this.isLoading = false;
      },
			//处理好友审核单
			async postApply(apply,status){
			  let data={id:apply.id,status}
				let res=await postFriednCheck(data)
				if(res.data.code==='2000'){
				  this.$toast('处理成功!')
					apply.status=status
				}else {
				  this.$toast(res.data.msg)
				}
			}
		},
		watch:{
      //数据发生变化及时更新scroll
      fApplyList(){
        this.$nextTick(()=>{
          this._initScroll()
        })
			}
		},
  }
</script>

<style scoped lang="scss">
	/deep/ .van-pull-refresh__track{
		height: 14rem;
	}
.wrap{
	overflow: hidden;
	max-height:523px;
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
