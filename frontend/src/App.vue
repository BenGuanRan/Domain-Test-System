<template>
  <div id="nav">
    <el-container>
      <el-aside width="200px">
        <el-menu
          background-color="#f5f7fa"
          style="height: 100%; over-flow: hidden"
          router
          :default-active="router.currentRoute.value.fullPath || 'search'"
          class="el-menu-vertical-demo"
          ><div class="logo_container"></div>
          <el-menu-item index="/search">
            <el-icon><icon-menu /></el-icon>
            <span>域名综合评估</span>
          </el-menu-item>
          <el-menu-item index="/display">
            <el-icon><icon-menu /></el-icon>
            <span>国内域名现状展示</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main
        ><router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive> </router-view
      ></el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts" >
import { ref } from "vue";
import { useRouter } from "vue-router";
import SearchPage from "@/views/SearchPage.vue";
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
::v-deep(.el-aside) {
  height: 100%;
}
.el-container {
  height: 100%;
}
.el-aside {
  overflow: hidden !important;
}
.el-main {
  height: 100% !important;
  background-color: #fff;
}
.el-menu {
  border: none !important;
}
.logo_container {
  height: 60px;
}
#nav {
  height: 100%;
}
.logo_container {
  background-image: url(./assets/logo2.png);
  background-size: 90%;
  background-position: center;
  background-repeat: no-repeat;
  background-color: #f5f7fa;
}
</style>
