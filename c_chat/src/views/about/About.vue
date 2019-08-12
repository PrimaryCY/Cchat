<template>
  <div class="about">
    <van-nav-bar
            border
            title="关于Cchat"
            left-text="返回"
            left-arrow
            @click-left="$router.push('/home')"/>

    <div class="dna">
      <div class="dna_section" v-for="(dna,i) in sequence">
        <div class="node top" v-bind:style="{'animation-delay' : -(i * 300) + 'ms' }"></div>
        <div class="node bottom" v-bind:style="{'animation-delay' : -(i * 300) + 'ms' }"></div>
      </div>
    </div>

  </div>
</template>
<script>
  export default {
    data(){
      return {
        sequence: []
      }
    },
    mounted() {
      this.sequence = new Array(Math.round(document.body.clientWidth/70));
    }
  }

</script>
<style scoped>
  body {
    background:#f7f7f7;
  }
  .site-canvas {
    position:relative;
  }
  .dna {
    position:fixed;
    top:25%;
    left:50%;
    -webkit-transform:translate(-50%,-50%);
    transform:translate(-50%,-50%);
    width:90%;
    height: 250px;
    text-align:center;
    overflow:hidden;
  }
  .dna_section {
    position:relative;
    margin:0 5px;
    width:50px;
    height:250px;
    display:inline-block;
  }
  .dna_section .node {
    position:absolute;
    top:0;
    left:0;
    width:50px;
    height:50px;
    border-radius:100%;
    background:#5E0035;
    -webkit-animation:4s topNode ease-in-out infinite;
    animation:4s topNode ease-in-out infinite;
  }
  @-webkit-keyframes topNode {
    0% {-webkit-transform:scale(0.5);transform:scale(0.5);top:0;z-index:10;opacity:0.75;}
    25% {-webkit-transform:scale(1);transform:scale(1);opacity:1;}
    50% {-webkit-transform:scale(0.5);transform:scale(0.5);top:200px;z-index:0;opacity:0.75;}
    75% {-webkit-transform:scale(0.25);transform:scale(0.25);opacity:0.5;}
    100% {-webkit-transform:scale(0.5);transform:scale(0.5);top:0;opacity:0.75;}
  }
  @keyframes topNode {
    0% {-webkit-transform:scale(0.5);transform:scale(0.5);top:0;z-index:10;opacity:0.75;}
    25% {-webkit-transform:scale(1);transform:scale(1);opacity:1;}
    50% {-webkit-transform:scale(0.5);transform:scale(0.5);top:200px;z-index:0;opacity:0.75;}
    75% {-webkit-transform:scale(0.25);transform:scale(0.25);opacity:0.5;}
    100% {-webkit-transform:scale(0.5);transform:scale(0.5);top:0;opacity:0.75;}
  }
  .dna_section .node.bottom {
    top:auto;
    bottom:0;
    background:#5C80BC;
    -webkit-animation:4s bottomNode ease-in-out infinite;
    animation:4s bottomNode ease-in-out infinite;
  }
  @-webkit-keyframes bottomNode {
    0% {-webkit-transform:scale(0.5);transform:scale(0.5);bottom:0; opacity:0.75;}
    25% {-webkit-transform:scale(0.25);transform:scale(0.25);opacity:0.5;}
    50% {-webkit-transform:scale(0.5);transform:scale(0.5);bottom:200px; opacity:0.75;}
    75% {-webkit-transform:scale(1);transform:scale(1); opacity:1;}
    100% {-webkit-transform:scale(0.5);transform:scale(0.5);bottom:0; opacity:0.75;}
  }
  @keyframes bottomNode {
    0% {-webkit-transform:scale(0.5);transform:scale(0.5);bottom:0; opacity:0.75;}
    25% {-webkit-transform:scale(0.25);transform:scale(0.25);opacity:0.5;}
    50% {-webkit-transform:scale(0.5);transform:scale(0.5);bottom:200px; opacity:0.75;}
    75% {-webkit-transform:scale(1);transform:scale(1); opacity:1;}
    100% {-webkit-transform:scale(0.5);transform:scale(0.5);bottom:0; opacity:0.75;}
  }
</style>
