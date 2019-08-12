<template>
	<transition name="load-fade" >
		<div  class="loading">
			<van-loading type="spinner" >
				{{text}}
			</van-loading>
		</div>
	</transition>
</template>

<script>
  export default {
    name: 'Loading', // 定义的组件名称 使用时写法：loading
		props:['text']
  }
</script>

<style scoped lang="scss">

	.loading{
		width: 100%;
		height: 100%;
		text-align: center;
		overflow: hidden;
		z-index: 10;
		.van-loading {
			margin-top: 70%;
			margin-bottom: 100%;
		}
	}

	.load-fade-enter,
	.load-fade-leave-active {
		opacity: 0;
	}
	.load-fade-enter-active,
	.load-fade-leave-active {
		transition: opacity 0.5s;
	}
</style>
