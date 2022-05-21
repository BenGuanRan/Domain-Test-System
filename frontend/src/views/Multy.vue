<template>
  <el-upload
    v-loading="ifFinding && !ifGetRes"
    v-if="!ifGetRes"
    drag
    ref="upload"
    class="upload-demo"
    action=""
    :limit="1"
    :on-exceed="handleExceed"
    :http-request="uploadHandler"
    :auto-upload="false"
    :on-change="openFile"
  >
    <el-icon class="el-icon--upload"><upload-filled /></el-icon>
    <div class="el-upload__text">拖拽上传或 <em>点击上传</em></div>
    <template #tip>
      <div class="el-upload__tip text-red">
        最大文件数为1，重复上传将覆盖原有文件！
        <el-link class="download_ex" @click="downloadExampleFile"
          >下载样例文件</el-link
        >
      </div>
    </template>
  </el-upload>
  <el-table
    v-if="domains.length"
    :data="domains"
    :default-sort="{ prop: 'point', order: 'descending' }"
    height="250"
    border
  >
    <el-table-column prop="domain" align="center" label="域名" />
    <el-table-column prop="type" align="center" label="类型" />
    <el-table-column align="center" width="114">
      <template #header>
        <el-button @click="submitUpload" v-if="!ifFinding">批量查询</el-button>
        <el-button
          type="danger"
          @click="stopSearch"
          v-if="ifFinding && !ifGetRes"
        >
          终止查询
        </el-button>
        <el-button type="primary" @click="exportRes" v-if="ifGetRes"
          >一键导出</el-button
        >
      </template>
      <template #default="scope">
        <span v-show="scope.row.over" class="over">√</span>
      </template>
    </el-table-column>
  </el-table>
  <el-card v-if="ifGetRes" shadow="none">
    <h3>查询结果</h3>
    <el-table height="250" :data="res" border style="width: 100%">
      <el-table-column prop="domainName" label="域名" width="180" />
      <el-table-column prop="type" label="类型" width="180" />
      <el-table-column prop="IP" label="IP" />
      <el-table-column prop="point" label="得分" />
      <el-table-column prop="data" label="各项得分" />
    </el-table>
  </el-card>
  <el-card style="margin-top: 20px" shadow="none">
    <h3 v-if="ifGetRes">结果统计</h3>
    <div class="bar_container"></div>
  </el-card>
</template>

<script setup lang="ts">
import { getPoints } from "@/api/multiple";
import { ElMessage } from "element-plus";
import * as XLSX from "xlsx/xlsx.mjs";
import { Checked, Loading } from "@element-plus/icons-vue";
import { ref, onMounted } from "vue";
import { genFileId } from "element-plus";
import { exportExcel } from "@/utils/exportExcel";
import type { UploadInstance, UploadProps, UploadRawFile } from "element-plus";
import { forEach } from "lodash";
import { drawBar } from "@/utils/draw";

onMounted(() => {});

const upload = ref<UploadInstance>();

// 确保最多只能上传一个文件
const handleExceed: UploadProps["onExceed"] = (files) => {
  upload.value!.clearFiles();
  const file = files[0] as UploadRawFile;
  file.uid = genFileId();
  upload.value!.handleStart(file);
};

// 上传结果进行批量查找
const res = ref<any>([]);
const ifFinding = ref<boolean>(false);
const ifGetRes = ref<boolean>(false);
const submitUpload = async () => {
  ifFinding.value = true;
  for (let i = 0; i < domains.value.length; i++) {
    res.value.push(...(await getPoints(i)));
    domains.value[i]["over"] = true;
  }
  ifGetRes.value = true;
  const node: any = document.querySelector(".bar_container");
  node.className = "h_700";
  drawBar(node, [], [], [], [], [], [], []);
};

const uploadHandler = (file: any) => {
  console.log(file);
};

const domains = ref<any>([]);
// 读取文件内容
const openFile = (file: any) => {
  // 若文件类型非excel
  if (!/\.(xls|xlsx|csv)$/.test(file.name.toLowerCase())) {
    ElMessage.error("文件格式不正确！");
    return;
  }
  var reader = new FileReader();
  reader.onload = function () {
    if (reader.result) {
      const data = reader.result;
      const workbook = XLSX.read(data, { type: "binary" });
      const wsname = workbook.SheetNames[0]; // 取第一张表
      const ws = XLSX.utils.sheet_to_json(workbook.Sheets[wsname]);
      domains.value = ws;
    }
  };
  reader.readAsBinaryString(file.raw);
};
const downloadExampleFile = () => {
  return exportExcel(
    [
      {
        domain: "aaa.com",
        type: 0,
        "": "",
        "注意：域名type类型定义，0政府、1服务娱乐、2教育、3公司企业。": "",
      },
      {
        domain: "bbb.com",
        type: 1,
      },
      {
        domain: "ccc.com",
        type: 2,
      },
    ],
    "样例文件",
    []
  );
};
// 导出批量查询结果
const exportRes = () => {
  return exportExcel(res.value, "查询结果", []);
};

// 终止查询
const stopSearch = () => {
  alert("stop");
};
</script>

<style scoped>
.el-upload {
  height: 800px !important;
}
.download_ex {
  font-size: 12px;
  color: #409eff;
}
.over {
  display: inline-block;
  width: 25px;
  height: 25px;
  background-color: #f0f9eb;
  border-radius: 50%;
  color: #67c23a;
  line-height: 25px;
  text-align: center;
}
.loader {
  position: absolute;
  top: 0px;
  bottom: 0px;
  left: 0px;
  right: 0px;
  margin: auto;
  width: 80%;
  height: 100px;
}
.loader span {
  display: block;
  background: #409eff;
  width: 7px;
  height: 100%;
  border-radius: 14px;
  margin-right: 5px;
  float: left;
}
.loader span:last-child {
  margin-right: 0px;
}
.loader span:nth-child(1) {
  animation: load 2.5s 1.4s infinite linear;
}
.loader span:nth-child(2) {
  animation: load 2.5s 1.2s infinite linear;
}
.loader span:nth-child(3) {
  animation: load 2.5s 1s infinite linear;
}
.loader span:nth-child(4) {
  animation: load 2.5s 0.8s infinite linear;
}
.loader span:nth-child(5) {
  animation: load 2.5s 0.6s infinite linear;
}
.loader span:nth-child(6) {
  animation: load 2.5s 0.4s infinite linear;
}
.loader span:nth-child(7) {
  animation: load 2.5s 0.2s infinite linear;
}
.loader span:nth-child(8) {
  animation: load 2.5s 0s infinite linear;
}
.loader span:nth-child(9) {
  animation: load 2.5s 0.2s infinite linear;
}
.loader span:nth-child(10) {
  animation: load 2.5s 0.4s infinite linear;
}
.loader span:nth-child(11) {
  animation: load 2.5s 0.6s infinite linear;
}
.loader span:nth-child(12) {
  animation: load 2.5s 0.8s infinite linear;
}
.loader span:nth-child(13) {
  animation: load 2.5s 1s infinite linear;
}
.loader span:nth-child(14) {
  animation: load 2.5s 1.2s infinite linear;
}
.loader span:nth-child(15) {
  animation: load 2.5s 1.4s infinite linear;
}
@keyframes load {
  0% {
    background: #afaaff;
    transform: scaleY(0.08);
  }
  50% {
    background: #409eff;

    transform: scaleY(1);
  }
  100% {
    background: #afaaff;
    transform: scaleY(0.08);
  }
}
.bar_container {
  width: 100%;
  height: 300px;
}
h3 {
  margin-top: 0;
}
.h_700 {
  height: 700px;
}
</style>