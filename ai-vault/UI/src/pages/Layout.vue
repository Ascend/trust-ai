<template>
  <div class="main bg_img">
    <app-header class="app-header"></app-header>
    <app-sider class="app-sider"></app-sider>
    <router-view class="main-content"/>
  </div>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue';
import AppSider from '@/components/AppSider.vue';

export default {
    name: "layout",
    data() {
        return {};
    },
    components: {
      AppHeader,
      AppSider
    }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main {
  width: 100%;
  height: 100%;
}

.bg_img{
  background: url(../assets/bg_user_home.png) center no-repeat;
  background-size: cover;
  position: absolute;
}

.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 50px;
  z-index: 2000;
}

.app-sider{
  position: fixed;
  width: 200px;
  top: 50px;
  padding: 16px 0 16px 24px;
}

.main-content {
  margin-left: 240px;
  padding: 66px 24px 0 24px;
  height: calc(100vh - 80px);
}
</style>
<style>
.main-content {
  color: #fffffe;
}
.el-dialog__header{
  border-bottom: 1px solid #3E4551;
}
.el-dialog__title {
  font-size: 16px;
  color: #FFFFFE;
  line-height: 24px;
  font-weight: 500;
}
.el-dialog__footer {
  text-align: center;
}
.dialog-button {
  font-size: 14px;
  line-height: 18px;
  padding: 5px 15px;
}
.dialog-tip {
  font-size: 12px;
  color: #CFD5DD;
  display: flex;
}

</style>
