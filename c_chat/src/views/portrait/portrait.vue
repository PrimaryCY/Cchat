<template>
	<div class="container">
		<van-nav-bar
						border
						title="修改头像"
						left-text="返回"
						left-arrow
						@click-left="$router.back()"
		/>
		<Loading v-if="loading.submit" :text="'正在努力上传中...'"></Loading>
		<div v-else class="form">
			<form>
				<div class="port-min">
						<img :src="input.portrait">
				</div>
				<div class="port-mid">
					<img :src="input.portrait">
				</div>
				<div class="port-max">
					<img :src="input.portrait">
				</div>
				<van-uploader   :after-read="submit"
												upload-text="请上传头像" accept="image/*">
					</van-uploader>
				<van-button hairline :loading="loading.save"  loading-type="spinner" size="large"
										@click.prevent='save'  type="info" plain round loading-text="保存中...">
					保存>
				</van-button>

			</form>
		</div>
	</div>

</template>

<script>
	import {mapState} from 'vuex'

  import {upload,put_user} from '../../api/index'

  export default {
    name: "pwd",
    data(){
      return {
        input:{                  													//提交内容
          portrait:this.$store.state.user.portrait, //新头像
        },
        fileList: [
          { url:this.$store.state.user.portrait }
        ],
				loading:{																					//等待内容
          save:false,															//保存等待
					submit:false														//上传等待
				}
      }
    },
		computed:{
      ...mapState(['user'])
		},
    methods:{

      //上传
      async submit(file){
        if(file===this.user.portrait) return this.$toast('请上传头像!')
				this.loading.sumbit=true
				let res=await upload(file.file)
				if (res.data.code==='2000'){
				  this.input.portrait=res.data.url
					this.$toast('上传成功!')
				}else {
				  this.$toast('上传失败请重试!')
				}
        this.loading.sumbit=false
      },

			//保存头像
			async save(){
        if(this.user.portrait===this.input.portrait) return this.$toast('请上传头像!')
        this.loading.save=true
        let res=await put_user({portrait:this.input.portrait})
        if (res.data.code==='2000'){
          this.$toast('修改成功!')
					this.$store.dispatch('modify_userinfo',res.data.data)
					this.$router.push('/home')
        }else {
          this.$toast(res.data.msg)
        }
        this.loading.save=false
			}
    }
  }
</script>

<style scoped lang="scss">
	.van-button--large{
		width: 50%;
	}

	/deep/ .van-uploader__upload{
		width: 100% !important;
		height: 3rem !important;
	}
	/deep/.van-uploader__preview-delete{
		right: -25px!important;
	}
	.van-uploader{
		display: block;
	}
	/deep/ .van-image__img{
		border-radius: 50%;
	}
	.container{
		width: 100%;
		height: 100%;
		position: absolute;
		background-color: whitesmoke;
		.form{
			padding: 0.9rem;
			text-align: center;
			.port-min{
				width: 60px;
				height: 60px;
				display: block;
				margin-left: 2.5667rem;
				img{
					border-radius: 50%;
					width: 100%;
					height: 100%;
					object-fit: cover;
				}
			}
			.port-mid{
				width: 80px;
				height: 80px;
				display: block;
				position:relative;
				img {
					position: absolute;
					border-radius: 50%;
					object-fit: cover;
					width: 100%;
					height: 100%;
					left: 185%;
				}
			}
			.port-max{
				width: 100px;
				height: 100px;
				display: block;
				margin-left: 1.26667rem;
				margin-bottom: 14px;
				img {
					border-radius: 50%;
					width: 100%;
					height: 100%;
					object-fit: cover;
				}
			}
		}
	}
	.van-button--hairline {
		height: 100%;
	}
</style>
