<template>
	<div>
		<van-nav-bar
						border
						title="创建聊天室"
						left-text="返回"
						left-arrow
						@click-left="$router.back()"
		/>

		<div class="form">
			<van-cell-group>
				<van-cell>
					<h2>聊天室名称:</h2>
					<van-field
									v-model="input.name"
									placeholder="请输入聊天室名称"
									rows="3"
									required
									clickable
					/>
				</van-cell>
				<van-cell>
					<h2>聊天室封面图</h2>
					<van-uploader
									v-model="fileList"
									:max-count="1"
					/>
				</van-cell>

				<van-cell>
					<h2>聊天室简介:</h2>
					<van-field
									v-model="input.desc"
									type="textarea"
									placeholder="请输入聊天室简介"
									rows="3"
									required
									clickable
					/>
				</van-cell>
				<van-cell class="center">
					<van-button hairline  size="large"  :loading="loading" loading-text="创建中..."
											@click.prevent='submit'  type="info" plain round>
						提交>
					</van-button>
				</van-cell>

			</van-cell-group>

		</div>
	</div>

</template>

<script>
	import {upload,postChatRooms} from '../../api/index'

  export default {
    name: "createRoom",
		data(){
      return {
        input:{
          name:'',				//聊天室名称
					desc:'',				//聊天室简介
          img:'',					//聊天室封面图
				},
        fileList: [],																//上传图片
				loading:false   	//上传等待
			}
		},
		methods: {
      //提交反馈
      async submit() {
        if (!this.input.name.trim()) return this.$toast('聊天室名称未填写')
        if (!this.input.desc.trim()) return this.$toast('聊天室简介未填写')

        //循环上传图片
        for (let i in this.fileList) {
          let file = this.fileList[i].file
          let res = await upload(file)
          if (res.data.code === '2000') {
            this.input.img = res.data.url
          }
        }

        this.loading=true
        let res=await postChatRooms(this.input)
        if (res.data.code==='2000'){
          this.$toast('提交成功!')
          this.$router.replace('/home')
        }else {
          this.$toast(res.data.msg)
        }
        this.loading=false

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
			//margin-top: 46px;
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
