<template>
	<div class="container">
		<van-nav-bar
						border
						title="个人资料"
						left-text="返回"
						left-arrow
						@click-left="$router.back()"
		/>
		<div class="form">
			<div class="portrait" @click="$router.push('/portrait')">
				<img :src="user.portrait">
			</div>
			<form>
				<van-cell-group>
					<van-field
									v-model="input.nickName"
									type="text"
									label="昵称:"
									clickable
					/>

					<van-field
									v-model="input.email"
									type="text"
									label="邮箱:"
									:clickable="!user.is_email"
									:disabled="user.is_email"
					/>
					<van-field
									:value="user.is_email?'已绑定':'未绑定'"
									type="text"
									label="是否绑定邮箱:"
									disabled
					/>

					<van-cell :value="computSex"   @click="show.sex = true">
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

					<van-cell  :value="input.birth" @click="show.birth = true">
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

					<van-cell  :value="computArea" @click="show.area = true">
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
				<van-button hairline :loading="loading.sumbit"  loading-type="spinner" size="large"
										@click.prevent='submit'  type="info" plain round>
					提交>
				</van-button>
			</form>
		</div>
	</div>

</template>

<script>
	import {Area,Picker,DatetimePicker} from 'vant'
	import {mapState} from 'vuex'

  import {put_user} from '../../api/index'
  import areaList from '../../common/area'
  import {formatDate} from '../../filter/formatdate'

  export default {
    name: "pwd",
    data(){
      return {
        areaList:areaList,
        sexs:['男','女'],				//性别选项
        loading:{								//等待状态
          sumbit:null, //点击提交等待
        },
        input:{                  //提交内容
          sex:this.$store.state.user.sex,       			//性别
          email:this.$store.state.user.email?this.$store.state.user.email:'未填写',    //邮箱
          nickName:this.$store.state.user.nickName,   //昵称
					birth:this.$store.state.user.birth?this.$store.state.user.birth:'未填写',			    //生日
					area:'',																    //地区
        },
				show:{									 //是否展示
          sex:false,		//性别
					birth:false,	//生日
					area:false,		//地区
				}
      }
    },
		computed:{
      ...mapState(['user']),
			computArea(){
        //用户选择后展示的
        if(typeof this.input.area === "object"){
          return this.input.area.toString()
				}
        //用户首次进入时展示自己原有数据时展示的
        else {
          if(!this.user.province) return '未填写'
          else {
            let home
            let pro=areaList.province_list[this.user.province]
            let city=areaList.city_list[this.user.city]
            if (this.user.home){
              home=areaList.county_list[this.user.home]
            }
            return `${pro}-${city}-${home?home:''}`
          }
				}
			},
			computSex(){
        if(this.input.sex==='woman'){
          return '女'
				}else if(this.input.sex==='man'){
          return '男'
				}else if(this.input.sex==='secrecy'){
          return '未填写'
				}else{
          return this.input.sex
				}
			}
		},
    methods:{
      //提交按钮
      async submit(){
        if(!/^(\w-*\.*)+@(\w-?)+(\.\w{2,})+$/.test(this.input.email))  return this.$toast('邮箱格式输入不正确!')

        let uploadData={}
       	for(let i in this.input){
       	  if(this.input[i]===this.user[i]){
       	    continue
					}
       	  uploadData[i]=this.input[i]
				}
				if(!uploadData) return this.$toast('修改成功!')

        this.loading.sumbit=true
        let res=await put_user(uploadData)
        if(res.data.code==='2000'){
          this.$toast('修改成功!')
          this.$store.dispatch('modify_userinfo',res.data.data)
          this.$router.replace('/home')
        }else{
          this.$toast(res.data.msg)
        }
        this.loading.sumbit=false
      },
      //确认生日
      confBirth(value){
        this.input.birth=formatDate(value,'yyyy-MM-dd')
        this.show.birth=false
      },
      //确认地区
      confArea(value){
        this.input.area=value
        this.input.area.toString=()=>{
          let temp=''
          let a=0
          Array.prototype.slice.call(this.input.area).forEach((item)=>{
            temp+=(a===0?'':'-')+item.name
            a++
          })
          return temp
        }
        this.show.area=false
      },
      //确认性别
      confSex(sex){
        this.input.sex=sex
        this.show.sex=false
      }
    },
		components:{
      [Area.name]:Area,
			[Picker.name]:Picker,
			[DatetimePicker.name]:DatetimePicker,
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
			.portrait{
				margin-left: 38%;
				margin-bottom: 20px;
				width: 80px;
				height: 80px;
				display: block;
				img{
					border-radius: 50%;
					width: 100%;
					height: 100%;
					object-fit: cover;
				}
			}
		}
	}
	.van-button--hairline {
		margin-top: 0.64667rem;
		height: 100%;
	}
	/deep/ input{
		text-align: right;
	}
	/deep/ span{
		color: black;
	}
</style>

