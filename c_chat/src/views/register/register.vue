<template>
	<div>
		<van-nav-bar
						title="注册"
						left-text="返回"
						right-text="登录"
						left-arrow
						@click-left="$router.back()"
						@click-right="$router.replace('/login')"
						border
						fixed
		/>
		<div class="login">
			<div class="login-img"></div>
			<section class="login-header">
				<h1 class="web-font-big login-title">Cchat</h1>
				<van-steps
								:active="active"
								active-icon="success"
								active-color="#07c160"
								class="register-steps"
				>
					<van-step>注册</van-step>
					<van-step>完善资料</van-step>
				</van-steps>
			</section>
			<div class="login-content">
				<div class="login-content">
					<form>
						<div v-if="active===0">
							<transition name="fade" mode="out-in" appear>
								<!--为了实现动画加上的flag-->
								<section v-show="flag">
									<div class="login_message">
										<van-cell-group :border="true">

												<van-field
																placeholder="用户名在6-20位(登录使用)"
																label="用户名:"
																left-icon="contact"
																input-align="center"
																v-model="user.userName"
																label-align="2222222222222"
																required
												/>
											<van-field
															placeholder="请输入小于20位昵称"
															label="昵称:"
															input-align="center"
															v-model="user.nickName"
															required
															>
												<svg  class="icon-min" aria-hidden="true" slot="left-icon">
													<use xlink:href="#icon-nicheng"></use>
												</svg>
											</van-field>
											<van-field
															placeholder="密码最少6位,由字母和数字的组成"
															label="密码:"
															type="password"
															input-align="center"
															v-model="user.pwd"
															required
											>
												<svg  class="icon-min" aria-hidden="true" slot="left-icon">
													<use xlink:href="#icon-ziyuan"></use>
												</svg>
											</van-field>
											<van-field
															placeholder="请重复输入密码"
															label="确认密码:"
															type="password"
															input-align="center"
															v-model="user.checkPwd"
															required
											>
												<svg  class="icon-min" aria-hidden="true" slot="left-icon">
													<use xlink:href="#icon-mima"></use>
												</svg>
											</van-field>
										</van-cell-group>
									</div>
									<div class="register-btn">
										<van-button round type="danger" size="large" hairline :loading="loading.register"
																loading-text="注册中" replace  @click.prevent="clickRegister"
										>注册</van-button>
									</div>
								</section>
							</transition>
						</div>
						<div v-if="active===1">
							<transition name="fade" mode="out-in" appear>
								<section v-show="flag">
									<div class="login_message">
										<van-cell-group>

											<van-field
															placeholder="请输入邮箱(找回密码时使用)"
															label="邮箱:"
															left-icon="contact"
															input-align="center"
															v-model="info.email"
											>
												<svg  class="icon-min" aria-hidden="true" slot="left-icon">
													<use xlink:href="#icon-youxiang"></use>
												</svg>
											</van-field>


											<van-cell :value="info.sex||'请选择性别'"   @click="show.sex = true">
												<div slot="title">
													<svg  class="icon-min" aria-hidden="true" >
														<use xlink:href="#icon-nianling-"></use>
													</svg>
													性别:
												</div>
											</van-cell>
											<van-popup v-model="show.sex" position="bottom" round>
												<van-picker :columns="sexs"   show-toolbar
																		@confirm="confSex"  @cancel="show.sex=false"
																		:default-index="0"/>
											</van-popup>

											<van-cell  :value="info.birth.toString()||'请选择生日'" @click="show.birth = true">
												<div slot="title">
													<svg  class="icon-min" aria-hidden="true" >
														<use xlink:href="#icon-nianling-"></use>
													</svg>
													生日:
												</div>
											</van-cell>
											<van-popup v-model="show.birth" position="bottom" round>
												<van-datetime-picker
																type="date"
																:min-date="new Date(50,0,1)"
																:max-date="new Date()"
																@confirm="confBirth"
																@cancel="show.birth = false"
												/>
											</van-popup>

											<van-cell  :value="info.area.toString()||'请选择地区'" @click="show.area = true">
												<div slot="title">
													<svg  class="icon-min" aria-hidden="true" >
														<use xlink:href="#icon-chengshi"></use>
													</svg>
													省/市/区:
												</div>
											</van-cell>
											<van-popup v-model="show.area" position="bottom" round>
												<van-area
																ref="area"
																value="110000"
																:area-list="areaList"
																@confirm="confArea"
																@cancel="show.area = false"
																:style="{ height: '50%' }"
												/>
											</van-popup>
										</van-cell-group>
									</div>
									<div class="register-btn">
										<router-link to="/home" class="register-btn-msg web-font-mid">
										>跳过,以后再完善!</router-link>
										<van-button round type="danger" size="large" hairline :loading="loading.complete"
																loading-text="注册中" replace  @click.prevent="clickComplete"
										>提交资料</van-button>
									</div>
								</section>
							</transition>
						</div>

					</form>

				</div>
			</div>
		</div>
	</div>
</template>

<script>
  import {Field,CellGroup,Radio,RadioGroup,Cell,Step,Steps,Area,Picker,DatetimePicker} from 'vant'

	import areaList from '../../common/area'
	import {post_user,put_user} from '../../api/index'
	import {formatDate} from '../../filter/formatdate'

  export default {
    name: "register",
		data(){
      return {
        user:{								//注册用户信息
          userName: '',//用户名
					nickName: '',//用户昵称
					pwd:'',			 //密码
					checkPwd:'', //确认密码
				},
				info:{								//完善用户信息
					area:'',		//地区
					sex:'',			//性别
					birth:'',		//生日
					email:''		//邮箱
				},
        flag:true,		//为了实现动画
      	loading:{							//加载状态
          register:false, //注册信息
					complete:false, //完善资料
				},
        circleFlag:true, //切换密码显示
      	radio:'',
				active:0,					//当前步骤
				areaList:areaList,
				show:{
          birth:false,		//显示年龄框
					area:false,			//显示地区框
					sex:false
				},
				sexs:['男','女']
      }
		},
    components:{
      [Field.name]:Field,
      [CellGroup.name]:CellGroup,
			[Radio.name]:Radio,
			[RadioGroup.name]:RadioGroup,
			[Cell.name]:Cell,
			[Step.name]:Step,
			[Steps.name]:Steps,
			[Area.name]:Area,
			[Picker.name]:Picker,
			[DatetimePicker.name]:DatetimePicker
    },
		methods:{
      //点击注册按钮
      async clickRegister(){
				let {userName,pwd,nickName,checkPwd}=this.user
				if(pwd!==checkPwd){
				  this.$toast('密码输入不一致')
					return
				}
				if(pwd.length<=6){
				  this.$toast('密码应大于6位')
					return
				}
				if(userName.length<6){
					this.$toast('用户名最少6位')
					return
				}
				if(!nickName.trim()){
				  this.$toast('昵称为必填项')
					return
				}

				this.loading.register=true
				let res=await post_user(this.user)
				if(res.data.code==='2000'&&res.data.data.token){
          this.$cookies.set('tk',res.data.data.token)
					this.$store.dispatch('receive_userinfo')
					this.$socket.disconnect()
					this.$socket.connect()
				}else {
				  this.$toast(res.data.msg)
					this.loading.register=false
					return
				}
        this.active++
				this.loading.register=false
			},
			async clickComplete(){
				if(!/^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/.test(this.info.email))  return this.$toast('邮箱格式输入不正确!')
				if(!this.info.birth)   return  this.$toast('生日未输入')
				if(!this.info.sex)     return  this.$toast('性别未输入')
				if(!this.info.area)    return  this.$toast('地区未选择')

				console.log(this.info)
				this.loading.complete=true

				let res=await put_user(this.info)
				if(res.data.code==='2000'){
          this.$store.dispatch('modify_userinfo',res.data.data)
					this.$router.replace('/home')
				}else {
				  this.$toast(res.data.msg)
				}
				this.loading.complete=false
			},
			//确认生日
			confBirth(value){
        this.info.birth=formatDate(value,'yyyy-MM-dd')
				this.show.birth=false
			},
			//确认地区
			confArea(value){
        this.info.area=value
				this.info.area.toString=()=>{
          let temp=''
					let a=0
          Array.prototype.slice.call(this.info.area).forEach((item)=>{
            temp+=(a===0?'':'-')+item.name
						a++
					})
					return temp
				}
				this.show.area=false
			},
			//确认性别
			confSex(sex){
        this.info.sex=sex
				this.show.sex=false
			}
		},
  }
</script>

<style scoped lang="scss">
	//提示文本
	.label{
		width: 300px;
		.label-helper{
			color: #969799;
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
		margin: 12px 17px;
		width: 92%;
		/deep/ 	div.van-field__label{
			width: 73px;
		}
		/deep/ .van-field__control{
			width: 100%;
			//margin-left: 42px;
		}
	}
	.register-sex-redio{
		width: 50%;
		/deep/ .van-cell{
			margin: -13px 17px;
		}
	}
	.login {
		height: 551px;

		/*overflow: auto;*/
		.login-img{
			background-image: url("../../common/img/LoginRegister3.jpg");
			filter: blur(1px);
			z-index: -1;
			width: 100%;
			height: 100%;
			position: fixed;
			background-size:cover
		}
		.login-header{
			width: 100%;
			height: 150px;
			overflow: hidden;
			text-align: center;
			.login-title{
				margin-top: 60px;
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
			height: 100%;
			form{
				//注册按钮
				.register-btn{
					text-align: center;
					width: 259px;
					margin-left: 60px;
					/*position: absolute;*/
					margin-top: 30px;
					.register-btn-msg{
						display: block;
						margin: 30px;
						color: crimson;
					}
				}
			}
		}
	}
	.register-steps{
		text-align: -webkit-left;
		background-color: transparent;
		width: 80%;
		margin-left: 28px;
		margin-top: 22px;
		/deep/ .van-step__circle-container{
			background-color: transparent;
		}
		/deep/ .van-step__line{

		}
		/deep/ .van-step__title{
			font-size: 18px;
			font-weight: bold;
			color: #7d7e80;
		}
	}
</style>

