<template>
  <div class="DisplayPage">
    <el-card class="display_container" shadow="never">
      <div class="selece_container">
        <el-select v-model="number" style="width: 100px" placeholder="Select">
          <el-option key="1" :label="1000" :value="1000" />
          <el-option key="2" :label="10000" :value="10000" />
          <el-option key="3" :label="100000" :value="100000" />
        </el-select>
        <el-select v-model="kind" style="width: 100px" placeholder="Select">
          <el-option key="1" label="综合得分" :value="1" />
          <el-option key="1" label="IP得分" :value="2" />
          <el-option key="1" label="CNAME得分" :value="3" />
          <el-option key="1" label="服务商得分" :value="4" />
          <el-option key="1" label="NS服务商分" :value="5" />
          <el-option key="1" label="DNS服务商分" :value="6" />
          <el-option key="1" label="顶级域得分" :value="7" />
        </el-select>
      </div>

      <div class="displayer"></div>
    </el-card>
  </div>
</template>

<script lang='ts' setup>
import { reactive, ref, onMounted } from "vue";
import { drawComplex } from "@/utils/draw";

const number = ref("");
const kind = ref("");

onMounted(() => {
  const node = document.querySelector(".displayer");
  drawComplex(node);
});

const num = ref(0);
const data = reactive({});
</script>

<style lang='scss' scoped>
.DisplayPage {
  height: 100%;
}
.display_container {
  position: relative;
  height: 100%;
  width: 100%;
}
::v-deep(.el-card__body) {
  height: 100% !important;
}
.displayer {
  height: 100%;
}
.selece_container {
  width: 200px;
  position: absolute;
  right: 20px;
  top: 40px;
}
</style>