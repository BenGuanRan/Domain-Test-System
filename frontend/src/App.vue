<template>
  <div id="nav">
    <div class="menu">
      <el-menu router class="el-menu-demo" mode="horizontal">
        <el-menu-item index="signal">单域名查询</el-menu-item>
        <el-menu-item index="multiple">多域名查询</el-menu-item>
      </el-menu>
      <div class="h-6" />
    </div>
  </div>
  <router-view v-slot="{ Component }">
    <keep-alive>
      <component :is="Component" />
    </keep-alive>
  </router-view>
</template>

<script setup lang="ts" >
// import { ref, watch } from "vue";
// import { useRouter } from "vue-router";
// const nowPath = ref("signal");
// const router = useRouter();
// watch(
//   () => router,
//   (newValue, oldValue) => {
//     nowPath.value =
//       newValue.currentRoute.value.fullPath.split("/")[1] || "signal";
//   },
//   { immediate: true }
// );
</script>

<style lang="scss">
#nav {
  .menu {
    width: 240px;
    margin: 0 auto;
    padding-left: 10px;
  }
  .el-menu {
    border-bottom: none;
    .el-menu-item {
      background-color: #fff;
    }
  }
}
</style>
