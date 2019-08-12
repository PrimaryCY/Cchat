<template>
	<section>
		<van-tabbar route active-color="red" class="food">
			<van-tabbar-item replace to="/msg" icon="home-o">
				<div :class="fontCls">消息</div>
				<div slot="icon" slot-scope="props" >
					<svg  class="icon-mid" aria-hidden="true">
						<use xlink:href="#icon-xiaoxi"></use>
					</svg>
				</div>
			</van-tabbar-item>
			<van-tabbar-item replace to="/addressList" icon="search">
				<div :class="fontCls">通讯录</div>
				<div slot="icon" slot-scope="props" >
					<svg  class="icon-mid" aria-hidden="true">
						<use xlink:href="#icon-shuben"></use>
					</svg>
				</div>
			</van-tabbar-item>
			<van-tabbar-item replace to="/weChat" icon="search">
				<div :class="fontCls">群聊</div>
				<div slot="icon" slot-scope="props" >
					<svg  class="icon-mid" aria-hidden="true">
						<use xlink:href="#icon-shequn"></use>
					</svg>
				</div>
			</van-tabbar-item>
			<van-tabbar-item replace to="/home" >
				<div :class="fontCls">我的</div>
				<div slot="icon" slot-scope="props" >
					<svg  class="icon-mid" aria-hidden="true">
						<use xlink:href="#icon-haizi"></use>
					</svg>
				</div>
			</van-tabbar-item>
		</van-tabbar>
	</section>
</template>
<script>
  import { Tabbar, TabbarItem } from 'vant';

  export default {
        name: "footerGuide",
		data(){
        	  return {fontCls:{'web-font-min':false}}
		},
	  	components:{
          [Tabbar.name]:Tabbar,
		  [TabbarItem.name]:TabbarItem,
		}
    }
</script>
<style lang="scss">
.food{
	position: absolute!important;
}
</style>

