<template>
	<div class="global">
		<van-nav-bar
						title="消息"
						border
		/>
		<div class="tab">
			<van-tabs v-model="active"
								animated
								swipeable
								@click="onClick"
			>
				<van-tab  :title="'好友消息'" >
				</van-tab>
				<van-tab :title="'群聊消息'" >
				</van-tab>
			</van-tabs>
		</div>
		<component :is="componentName"></component>
	</div>
</template>

<script>
	import friend from '../../components/friend/friend'
	import friendGroup from '../../components/friendGroup/friendGroup'

  export default {
    name: "msg",
    data(){
      return {
        active:0,						//默认展示页
				componentName:'friend'
      }
    },
    methods:{
      onClick(name, title) {
        if(name===0){
          this.componentName='friend'
        }else {
          this.componentName='friendGroup'
        }
      }
    },
		components:{
      friend,
			friendGroup
		}
  }
</script>

<style scoped lang="scss">

</style>
