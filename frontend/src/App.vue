<template>
  <div id="nav">
    <div class="menu">
      <el-menu
        router
        :default-active="router.currentRoute.value.fullPath || 'signal'"
        mode="horizontal"
      >
        <el-menu-item index="/signal">单域名查询</el-menu-item>
        <el-menu-item index="/multiple">多域名查询</el-menu-item>
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
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
const nowPath = ref("signal");
const router = useRouter();
console.log(router.currentRoute.value.fullPath);

// watch(
//   () => router,
//   (newValue, oldValue) => {
//     nowPath.value =
//       newValue.currentRoute.value.fullPath.split("/")[1] || ;
//   },
//   { immediate: true }
// );
</script>

<style lang="scss">
#nav {
  .menu {
    width: 300px;
    margin: 0 auto;
    padding-left: 10px;
  }
  .el-menu {
    border-bottom: none;
    .el-menu-item {
      background-color: #fff;
    }
    .el-menu-item:first-child {
      margin-left: 40px;
    }
  }
}
</style>
