<template>

	<div id="app" >
		<Loading v-if="loading" :text="'自动登录中...'"></Loading>
		<div v-else>
			<transition name="router-fade" >
				<keep-alive v-if="$route.meta.keepAlive">
					<Scroll v-if="$route.meta.isScroll">
						<router-view></router-view>
					</Scroll>
					<router-view v-else></router-view>
				</keep-alive>

				<div v-if="!$route.meta.keepAlive">
					<Scroll v-if="$route.meta.isScroll">
						<router-view></router-view>
					</Scroll>
					<router-view v-else></router-view>
				</div>
			</transition>
		</div>
		<footer-guide v-if="$route.meta.showFooter"></footer-guide>
	</div>

</template>
<script>
	import footerGuide from './components/footerGuide/footerGuide'
	import Scroll from './components/common/scrollPage/scrollPage'
	import Loading from './components/common/loading/loading'


  export default {
    name: 'App',
		data(){
      return {loading:false}
		},
    components:{
      footerGuide,
			Scroll,
			Loading
    },
    mounted(){
        this.loading=true
        this.$store.dispatch('receive_userinfo',()=>{
					this.loading=false
        })
				setTimeout(()=>{
				  this.loading=false
				},3000)
    },
  }
</script>

<style lang="scss">
	#app{
		overflow-x: hidden;
	}
	.router-fade-enter-active, .router-fade-leave-active {
		transition: all .5s ease;
	}
	.router-fade-enter{
		opacity: 0;
		transform: translateX(100%);
	}
	.router-fade-leave-to {
		opacity: 0;
		transform: translateX(-100%);
		position: absolute;
	}

</style>
