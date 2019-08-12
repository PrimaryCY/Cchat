<style scoped="scoped">
	.w-scroll {
		height: 100%;
		overflow: auto;
		-webkit-overflow-scrolling: touch;
	}
</style>
<template>
	<div ref="scroll" class="w-scroll">
		<slot></slot>
	</div>
</template>
<script>
  export default {
    name: 'scroll',
    data() {
      return {}
    },
    computed: {},
    mounted() {
      this.wScroll(this.$refs.scroll);
    },
    methods: {
      wScroll(elem) {
        var startX = 0,startY = 0;
        document.addEventListener('touchstart', function(evt) {
          var touch = evt.touches[0];
          startX = Number(touch.pageX);
          startY = Number(touch.pageY);
        });
        elem.addEventListener('touchmove', function(ev) {
          var _point = ev.touches[0],
            _top = elem.scrollTop;
          var _bottomFaVal = elem.scrollHeight - elem.offsetHeight;
          //console.log(_top + ":" + _bottomFaVal + ":" + elem.offsetHeight + ":" + elem.scrollHeight);
          if(_top === 0) {
            if(_point.clientY > startY) {
              ev.preventDefault();
            } else {
              ev.stopPropagation();
            }
          } else if(_top === _bottomFaVal) {
            elem.scrollTop--;
          } else if(_top > 0 && _top < _bottomFaVal) {
            ev.stopPropagation();
          } else {
            ev.preventDefault();
          }
        }, {
          passive: false
        });
      }
    },
  }
</script>
