<template>
  <div class="signal">
    <el-card shadow="hover"> Hover </el-card>
  </div>
</template>

<script lang='ts' setup>
import { reactive, ref } from "vue";

const num = ref(0);
const data = reactive({});
</script>

<style lang='scss' scoped>
</style>