<template>
	<div class="container">
		<van-nav-bar
						border
						title="修改密码"
						left-text="返回"
						left-arrow
						@click-left="$router.back()"
		/>
		<div class="form">
			<form>
			<van-cell-group>
				<van-field
                type="password"
                v-model="text.pwd"
								required
								label="原始密码:"
								right-icon="question-o"
								placeholder="请输入原始密码"
								click-right-icon="$toast('question')"
								clickable
				/>

					<van-field
                  v-model="text.newPwd"
									type="password"
									label="新密码:"
									placeholder="请输入新密码"
									required
									clickable
					/>
				<van-field
                v-model="text.repeatPwd"
								type="password"
								label="确认新密码:"
								placeholder="请重复输入新密码"
								required
								clickable
				/>
			</van-cell-group>
				<van-button hairline :loading="loading.sumbit"  loading-type="spinner" size="large"
				@click.prevent='submit'  type="info" plain round>
					提交>
				</van-button>
			</form>
		</div>
	</div>

</template>

<script>
import {updatePwd} from '../../api/index'
  export default {
    name: "pwd",
		data(){
      return {
        loading:{								//等待状态
          sumbit:null, //点击提交等待
        },
        text:{                  //提交内容
          pwd:'',       //原始密码
          newPwd:'',    //新密码
          repeatPwd:''  //确认新密码
        }
      }
    },
    methods:{
      //提交按钮
      async submit(){
        if(this.text.newPwd!==this.text.repeatPwd)return this.$toast('新密码与旧密码输入不一致!')
        if(!this.text.newPwd.trim())return this.$toast('新密码未填写!')
        if(!this.text.pwd.trim()) return this.$toast('请输入原始密码!')
        if(this.text.pwd===this.text.newPwd)return this.$toast('新密码不可以和旧密码相同!')

        this.loading.sumbit=true
        let res=await updatePwd(this.text)
        if(res.data.code==='2000'){
          this.$toast('修改成功!')
          this.$router.replace('/home')
        }else{
          this.$toast(res.data.msg)
        }
        this.loading.sumbit=false
      }
    }
  }
</script>

<style scoped lang="scss">
.container{
	width: 100%;
	height: 100%;
	position: absolute;
	background-color: whitesmoke;
	.form{
		padding: 23px;
	}
}
.van-button--hairline {
	margin-top: 58px;
	height: 100%;
}
</style>
