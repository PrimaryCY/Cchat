<template>
	<div class="global">
		<van-nav-bar
						title="我的申请"
						left-text="返回"
						left-arrow
						@click-left="$router.back()"
						border
		/>
		<div class="tab">
			<van-tabs v-model="active" @click="onClick">
				<van-tab  :title="'好友申请'" >
				</van-tab>
				<van-tab :title="'我的申请'" >
				</van-tab>
			</van-tabs>
		</div>
		<router-view></router-view>
	</div>
</template>

<script>
  export default {
    name: "myFriendCheck",
		data(){
      return {
        active:0
			}
		},
		methods:{
      onClick(name, title) {
        if(name===0){
					this.$router.replace('/myFriendCheck/fApply')
				}else {
          this.$router.replace('/myFriendCheck/sApply')
				}
      }
		}
  }
</script>

<style scoped lang="scss">
	.global{
		.tab{
			/*margin-top: 46px;*/
		}
	}
</style>
