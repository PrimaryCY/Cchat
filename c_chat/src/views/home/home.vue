<template>
  <div>
    <van-nav-bar title="个人中心"
                 border>
      <svg v-if="user.userName"
           class="icon-min"
           aria-hidden="true"
           slot="right"
           @click="logOut">
        <use xlink:href="#icon-dengchu" />
      </svg>
    </van-nav-bar>
    <Loading v-if="loadingLogout"
             text="退出登录中"></Loading>
    <van-pull-refresh v-model="isLoading"
                      :disabled="!user.userName"
                      @refresh="onRefresh">
      <!--登陆页面-->
      <div v-if="user.nickName"
           class="global">
        <div class="user-poster user-base-image"
             :style="{backgroundImage:`url(${baseImg})`}"></div>
        <div class="user-poster">
          <van-image fit="cover"
                     round
                     width="2.25rem"
                     height="2.25rem"
                     :src=user.portrait
                     @click="imgClick" />
          <section class="user-info">
            <ul>
              <li class="web-font-mid user-li">{{user.nickName}}</li>
              <li class="web-font-min user-li"
                  v-show="user.email">邮箱:{{user.email}}</li>
              <li class="web-font-min user-li">{{user.is_email?'已绑定邮箱':'未绑定邮箱'}}</li>
            </ul>
          </section>
        </div>
        <van-row class="user-links">
          <van-col span="6">
            <div @click="$router.push('/info')">
              <van-icon name="pending-payment" class="special"/>个人资料
            </div>
          </van-col>
          <van-col span="6">
            <div  @click="$router.push('/pwd')">
              <van-icon >
                <svg  class="icon-min" aria-hidden="true">
                  <use  xlink:href="#icon-mima"></use>
                </svg>
              </van-icon>
<!--              <van-icon name="records" />-->
              修改密码

            </div>
          </van-col>
          <van-col span="6">
            <div @click="$router.push('/portrait')">
<!--              <van-icon name="records" />修改头像-->
              <van-icon>
                <svg  class="icon-min" aria-hidden="true">
                  <use  :xlink:href="user.sex===1?'#icon-icon31':'#icon-icon26'"></use>
                </svg>
              </van-icon>
              修改头像
            </div>
          </van-col>
          <van-col span="6">
						<div @click="logOut">
<!--              <van-icon name="logistics" />退出登录-->
              <van-icon >
                <svg  class="icon-min" aria-hidden="true">
                  <use  xlink:href="#icon-likaichumen"></use>
                </svg>
              </van-icon>
              退出登录
						</div>
          </van-col>
        </van-row>

        <van-cell-group class="user-group">
          <van-cell icon="records"
                    title="全部申请"
                    is-link to="/myFriendCheck"/>
          <van-cell icon="points"
                    title="数据统计"
                    is-link />
          <van-cell icon="gift-o"
                    title="意见反馈" to="/feedback"
                    is-link/>
          <van-cell icon="gold-coin-o"
                    title="关于Cchat"
                    is-link to="/about" />
        </van-cell-group>
      </div>
      <!--未登录页面-->
      <div v-else
           class="global">
        <div class="user-poster user-base-image"
             :style="{backgroundImage:`url(${baseImg})`}"></div>
        <div class="user-poster">
          <!--未登录情况下用于占位使用,勿删-->
        </div>
        <div class="not-login">
          <van-button round
                      type="danger"
                      size="large"
                      hairline
                      :loading="loading"
                      loading-text="跳转中..."
                      replace
                      @click.prevent="$router.push('/login')">注册/登录</van-button>
        </div>
      </div>
    </van-pull-refresh>
  </div>
</template>

<script>
import { Row, Col, Icon, Cell, CellGroup, Image, ImagePreview } from "vant";
import { mapState } from "vuex";

import { deleteLogin } from "../../api/index";
import Loading from "../../components/common/loading/loading";

export default {
  data () {
    return {
      //baseImg:'https://img.yzcdn.cn/public_files/2017/10/23/8690bb321356070e0b8c4404d087f8fd.png',
      baseImg: require("../../common/img/HomeDefault.jpg"),
      isLoading: false,
      loading: false, //登录注册按钮加载,
      loadingLogout: false //退出登录加载
    };
  },
  components: {
    [Row.name]: Row,
    [Col.name]: Col,
    [Icon.name]: Icon,
    [Cell.name]: Cell,
    [CellGroup.name]: CellGroup,
    [Image.name]: Image,
    Loading
  },
  methods: {
    imgClick () {
      ImagePreview([this.user.portrait]);
    },
    //下拉刷新
    onRefresh () {
      if ($cookies.get("tk")) {
        this.$store.dispatch("receive_userinfo", () => {
          this.$toast("刷新成功");
          this.isLoading = false;
        });
      }
    },
    async logOut () {
      let dialog = await this.$dialog
        .confirm({
          message: "你真的要离开吗?...",
          closeOnClickOverlay: true
        })
        .catch(() => { });
      if (dialog === "confirm") {
        this.loadingLogout = true;
        let res = await deleteLogin();
        if (res.data.code === "2000") {
          //兼容手机浏览器,手机浏览器无法删除cookies
          this.$cookies.set('tk','',1)
          this.$cookies.remove("tk");
          this.$store.dispatch("reset_conf");
          //this.$socket.emit('logOut')
          //用户退出登录后重新连接服务端
          this.$socket.disconnect()
          this.$socket.connect()
        } else {
          this.$toast(res.data.msg);
        }
        this.loadingLogout = false;
      }
    }
  },
  computed: {
    ...mapState(["user"])
  }
};
</script>

<style lang="less" scoped>
/*//下拉刷新*/
/*.van-pull-refresh{*/
/*		margin-top: 20px;*/
/*}*/
.special{
  margin-top: 3px;
}

/deep/ .van-loading {
  margin-top: 17px;
}

.global {
  height: 547px;
}
.user {
  &-poster {
    width: 100%;
    height: 55vw;
    display: block;
    text-align: center;
  }
  &-base-image {
    position: fixed;
    left: 0px;
    filter: blur(1px);
    z-index: -1;
    background-size: 375px 226px;
    border-radius: 0px 0px 80px 80px;
  }
  &-group {
    margin-bottom: 15px;
  }
  &-links {
    padding: 0.22rem 0;
    font-size: 12px;
    text-align: center;
    background-color: #fff;
    .van-icon {
      display: block;
      font-size: 24px;
      margin-bottom: 3px;
    }
  }
  &-info {
    text-align: center;
    width: 100%;
    margin-top: 10px;
    .user-li {
      padding: 1px;
    }
  }
}
.van-image {
  margin-top: 1.43333rem;
}
/*未登录时content样式*/
.not-login {
  margin: 50px;
  margin-top: 100px;
}
</style>
