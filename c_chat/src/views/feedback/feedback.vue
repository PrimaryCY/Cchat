<template>
	<div>
		<van-nav-bar
						border
						title="意见反馈"
						left-text="返回"
						left-arrow
						@click-left="$router.back()"
						fixed
		>
			<van-icon name="question-o" slot="right" />
		</van-nav-bar>
		<Loading v-if="loading.submit" :text="'正在努力提交中...'"></Loading>

		<div v-else class="form">
			<van-cell-group>
				<van-cell>
					<h2>反馈问题类型:</h2>
					<van-radio-group v-model="input.type">
						<van-radio :name="item.id" v-for="(item,index) in feedbackTypes" :key="item.id">{{item.name}}</van-radio>
					</van-radio-group>

				</van-cell>
				<van-cell>
					<h2>反馈内容:</h2>
					<van-field
									v-model="input.content"
									type="textarea"
									placeholder="请输入反馈内容"
									rows="3"
									required
									clickable
					/>
				</van-cell>
				<van-cell>
					<van-uploader
									v-model="fileList"
									multiple
									:max-count="5"
					/>

				</van-cell>
				<van-cell>
					<h2>联系方式:</h2>
					<van-field
									value="123"
									type="text"
									v-model="input.contact"
					/>
					<div class="aui-view-box-item">
						<p>留下您的联系方式,以便我们了解问题后及时反馈和结果。</p>
					</div>
				</van-cell>
				<van-cell class="center">
					<van-button hairline  size="large"
											@click.prevent='submit'  type="info" plain round>
						提交>
					</van-button>
				</van-cell>

			</van-cell-group>

		</div>
	</div>

</template>

<script>
  import {mapState} from 'vuex'
	import {RadioGroup,Radio} from 'vant'

  import {upload,postFeedback,getFeedbackTypes} from '../../api/index'
	import Loading from '../../components/common/loading/loading'

  export default {
    name: "feedback",
		components:{
      [Radio.name]:Radio,
			[RadioGroup.name]:RadioGroup,
			Loading
		},
    data(){
      return {
        input:{                  															//提交内容
          type:1,																		//反馈类型
					content:'',																//反馈内容
					contact:'',																//联系人
					feedbackImages:[],												//上传图片url列表
        },
        fileList: [],																//上传图片
        loading:{																							//等待内容
          submit:false														  //提交等待
        },
				feedbackTypes:[],																			//反馈类型
      }
    },
    computed:{
      ...mapState(['user'])
    },
		created(){
			this._receiveFeedbackTypes()
		},
    methods:{
      //接收反馈类型
      async _receiveFeedbackTypes(){
        let res=await getFeedbackTypes()
				if(res.data.code==='2000'){
				  this.feedbackTypes=res.data.data
				}else {
				  this.$toast(res.data.msg)
				}
			},
      //提交反馈
      async submit(){
        if(!this.feedbackTypes) return this.$toast('反馈类型未填写,请检查网络刷新重试!')
        if(!this.input.content.trim()) return this.$toast('请描述意见详细!')

				//循环上传图片
				for(let i in this.fileList){
				  let file=this.fileList[i].file
					let res=await upload(file)
					if(res.data.code==='2000'){
            this.input.feedbackImages.push(res.data.url)
					}
				}

        this.loading.submit=true
        let res=await postFeedback(this.input)
        if (res.data.code==='2000'){
          this.$toast('提交成功!')
					this.$router.replace('/home')
        }else {
          this.$toast(res.data.msg)
        }
        this.loading.submit=false
      }
    }
  }
</script>

<style scoped lang="scss">
	h2{
		font-weight: bolder;
	}
	.aui-view-box-item{
		color: #bdbdbd;
		font-size: 10px;
	}
	.van-button--large{
		width: 50%;
	}
	.form{
			height: 551px;
			//position: absolute;
			background-color: #f3f3f7;
			padding: 0.2rem;
			text-align: center;
			//height: 90%;
			.van-cell-group{
				height: 100%;
				margin-top: 46px;
				.center{
					div{
						text-align: center;
					}
				}
			}
		}
	.van-button--hairline {
		height: 100%;
	}
</style>
