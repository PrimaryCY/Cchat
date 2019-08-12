<template>
	<section >
		<van-nav-bar
						border
						fixed
						title="登录"
						left-text="返回"
						right-text="注册"
						left-arrow
						@click-left="$router.back()"
						@click-right="$router.push('/register')"
		/>
	<div class="login">
		<div class="login-img"></div>
		<section class="login-header">
			<h1 class="web-font-big login-title">Cchat</h1>
			<div class="login_header_title">
				<a href="javascript:;"  @click="flag=true" class="web-font-mid" :class="{on:flag}">邮箱登录</a>
				<a href="javascript:;"  @click="flag=false" class="web-font-mid" :class="{on:!flag}">密码登录</a>
			</div>
		</section>
		<div class="login-content">
			<form>
				<div>
					<transition name="fade" mode="out-in" appear>
					<section v-show="flag">
						<div class="login_message">
							<van-cell-group>
								<van-field
												placeholder="请输入邮箱账号"
												label="邮箱:"
												left-icon="contact"
												v-model="loginData.email"
								/>
								<van-field
												placeholder="请输入验证码"
												label="验证码:"
												v-model="loginData.code"
								>
										<svg  class="icon-min" aria-hidden="true" slot="left-icon">
											<use xlink:href="#icon-yanzhengma"></use>
										</svg>
									<van-button slot="button" size="small" type="danger"
															@click.prevent="getVerCode" :loading="loading.code" loading-text="请求中">
										{{timeCode?timeCode+'秒':'获取验证码'}}
									</van-button>
								</van-field>
							</van-cell-group>
						</div>
					</section>
					</transition>
					<transition name="fade" mode="out-in" appear>
					<section v-show="!flag">
						<div class="login_message">
							<van-cell-group>
								<van-field
												placeholder="请输入用户名"
												label="用户名:"
												left-icon="contact"
												v-model="loginData.userName"
								/>
								<van-field
												placeholder="密码"
												label="密码:"
												:type="circleFlag?'tel':'password'"
												left-icon="contact"
												v-model="loginData.pwd"
								>
										<svg  class="icon-min" aria-hidden="true" slot="left-icon">
											<use xlink:href="#icon-ziyuan"></use>
										</svg>
										<div class="switch_button " slot="right-icon" :class="circleFlag?'on':'off'" @click="circleFlag=!circleFlag">
											<div class="switch_circle" :class="{move:circleFlag}" ></div>
											<span class="switch_text">...</span>
										</div>
								</van-field>
							</van-cell-group>
						</div>
					</section>
					</transition>
				</div>
				<div class="login-hint">
					<router-link to="/register" class="web-font-mid" src="javascript;">还没有账号?一分钟去注册!</router-link>
				</div>
				<div class="login-btn">
					<van-button round type="danger" size="large" hairline :loading="loading.sumbit"
											loading-text="登录中" replace  @click.prevent="sumbit"
					>登录</van-button>
				</div>
			</form>
		</div>
	</div>
	</section>

</template>

<script>
	import {Field,CellGroup} from 'vant'

	import {getVerCode,postLogin}from '../../api/index'


  export default {
    name: "login",
		data(){
      return{
        flag:true,				//切换邮箱登录|密码登录
        circleFlag:false, //切换密码显示
				timeCode:null,		//验证码倒计时
				loading:{					//加载状态
          code:false,	//验证码等待
					sumbit:false//提交等待
				},
				loginData:{				//登录存放的数据
          email:'',		//邮箱
					code:'',		//邮箱验证码
					userName:'',//用户名
					pwd:'',			//密码
					type:null		//登录类型 1:邮箱验证码  2:用户密码
				},
			}
		},
		components:{
      [Field.name]:Field,
			[CellGroup.name]:CellGroup
		},
		methods:{
      //验证码倒计时
			_time() {
        if (!this.timeCode) {
          this.timeCode = 300
          let tid = setInterval(() => {
            this.timeCode--
            if (this.timeCode <= 0) {
              clearInterval(tid)
            }
          }, 1000)
        }
      },
      //获取邮箱验证码
      async getVerCode(){
				let regemail = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
				if(regemail.test(this.loginData.email)){
					this.loading.code=true
					let res=await getVerCode({email:this.loginData.email})
					this.loading.code=false
					if(res.data.code==='2000'){
					  	this.$toast('验证码已发送至邮箱,请查收!')
							this._time()
						}
				}else {
				  this.$toast('邮件格式不符合要求!')
				}
			},
			//登录
			async sumbit(){
			  this.loginData.type=Number(this.flag)
			  if(this.flag){
			    //邮箱验证码登录
          let regemail = /^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/;
          if(!regemail.test(this.loginData.email)) return this.$toast('邮件格式不符合要求!')
          if(this.loginData.code.length!==6) return this.$toast('验证码填写不正确!')

				}else {
			    //用户名密码登录
					if(this.loginData.userName.length<6)return this.$toast('用户名输入错误')
					if(this.loginData.pwd.length<=6) return this.$toast('密码输入错误')
				}

				this.loading.sumbit=true
				let res=await postLogin(this.loginData)
				if(res.data.code==='2000'){
				  this.$store.dispatch('reset_conf')
          this.$cookies.set('tk',res.data.data.token)
					this.$socket.disconnect()
					this.$socket.connect()
					this.$store.dispatch('modify_userinfo',res.data.data.user)
					//回归初始状态
					this.loginData={}
					this.flag=true
				  this.$router.replace('/home')
					this.$socket.emit('authorization',res.data.data.token)
					this.$socket.emit('login')
				}else {
				  this.$toast(res.data.msg)
				}
				this.loading.sumbit=false
			}
    }
  }
</script>

<style scoped lang="scss">
	.login-hint{
		text-align: center;
		position: absolute;
		bottom: 37%;
		margin-left: 90px;
		a{
			color: #ff6c6c;
		}
	}
	.fade-enter,
	.fade-leave-to{
		opacity: 0;
		transform: translateX(600px);
	}
	.fade-enter-active,
	.fade-leave-active{
		opacity: 0.5;
		transition:all 0.5s ease;
	}

	.switch_button{
		font-size: 12px;
		border: 1px solid #ddd;
		border-radius: 8px;
		transition: background-color .3s,border-color .3s;
		padding: 0 6px;
		width :30px;
		height: 16px;
		line-height: 16px;
		color: #fff;
		position: absolute;
		top: 50%;
		right: 10px;
		transform :translateY(-50%);
		&.off{
			background: #fff;
			.switch_text{
				float: right;
				color: #ddd;
			}
		}
		&.on{
			background :lightcoral;
		}
		.switch_circle{
			//transform translateX(27px)
			position :absolute;
			top :-1px;
			left :-1px;
			width :16px;
			height :16px;
			border :1px solid #ddd;
			border-radius :50%;
			background: #fff;
			box-shadow :0 2px 4px 0 rgba(0,0,0,.1);
			transition :transform .3s;
			&.move{
				transform: translateX(27px)
			}
		}
	}
	.van-cell-group{
		background-color: transparent;
	}
	.van-cell{
		background-color: transparent;
		margin: 0px 42px;
		width: 77%;
		/deep/ 	div.van-field__label{
		width: 59px;
		}
		/deep/ .van-field__control{
			width: 67%;
		}
	}

	.login {
		height: 100%;
		width: 100%;
		overflow: hidden;
		position: absolute;
		.login-img{
			background-image: url("../../common/img/LoginRegister3.jpg");
			filter: blur(1px);
			z-index: -1;
			width: 100%;
			height: 100%;
			position: fixed;
			background-size: cover;
		}
		.login-header{
			width: 100%;
			height: 200px;
			overflow: hidden;
			text-align: center;
			.login-title{
				margin-top: 80px;
			}
			.login_header_title{
				padding: 40px;
				font-size: 26px;
				a{
					color:#333;
					padding-bottom :4px;
					&:first-child{
						margin-right: 40px
					}
					&.on {
						color :crimson;
						font-weight :700 ;
						border-bottom: 2px solid crimson
					}
				}
			}
		}
		.login-content{
			form{
			.login-btn{
				width: 259px;
				margin-left: 57px;
				position: absolute;
				bottom: 25%;
			}
			}
		}
	}
</style>

