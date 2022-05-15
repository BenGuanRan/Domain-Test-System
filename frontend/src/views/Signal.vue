<template>
  <div id="signal">
    <div class="search_container">
      <el-input
        v-model="search_data.domain_name"
        placeholder="请输入域名"
        class="input-with-select"
      >
        <template #prepend>
          <el-select
            v-model="search_data.domain_type"
            placeholder="域名类型"
            style="width: 100px"
          >
            <el-option label="政府" value="1" />
            <el-option label="服务娱乐" value="2" />
            <el-option label="教育" value="3" />
            <el-option label="公司企业" value="4" />
          </el-select>
        </template>
        <template #append>
          <el-button :icon="Search" @click="search" />
        </template>
      </el-input>
    </div>
    <div>
      <el-card v-if="ifShowResult" shadow="never">
        <el-descriptions
          class="margin-top"
          title="域名基础信息"
          :column="1"
          size="default"
          border
        >
          <template #extra>
            <el-button type="primary" @click="exportData">导出excel</el-button>
          </template>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">域名</div>
            </template>
            {{ signalData.data.domainName }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">IP</div>
            </template>
            {{ signalData.data.IP }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">CNAME</div>
            </template>
            {{ signalData.data.cname }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label> <div class="cell-item">服务商</div></template>
            {{ signalData.data.domainServer }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">NS服务商</div>
            </template>
            {{ signalData.data.nsServer }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">CDN服务商</div>
            </template>
            {{ signalData.data.cdnServer }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
      <el-card shadow="never" style="position: relative">
        <div style="font-size: 20px" class="en_header" v-if="ifShowResult">
          综合评估
        </div>
        <div class="en_body">
          <div class="en_l" v-if="ifShowResult">
            <div>该域名的日访问量为{{ signalData.data.visitCount }}人次</div>
            <h3>此域名综合得分:</h3>
            <div class="point_container">
              <span>{{ signalData.data.point }}</span> 分
              <div class="en_process">
                -9
                <el-progress
                  :percentage="pointToPercent(signalData.data.point)"
                  :color="pointColor"
                >
                  &nbsp; </el-progress
                >+9
              </div>
              <div class="en_ifdanger">{{ signalData.data.pointMessage }}</div>
            </div>
          </div>
          <div ref="node" class="en_r">
            <div class="loading" v-if="ifSearch && !ifShowResult">
              <loading></loading>
            </div>
            <div v-if="!ifSearch">NIST</div>

            <div id="self_charts"></div>
          </div>
        </div>
      </el-card>
      <el-card v-if="ifShowResult" shadow="never">
        <div style="font-size: 20px" class="en_header">具体分析</div>
        <p>
          {{ signalData.data.detailAnalyse }}
        </p>
      </el-card>
    </div>
  </div>
</template>

<script lang='ts' setup>
import Loading from "@/components/Loading.vue";
import { onMounted, reactive, ref, watch } from "vue";
import { Search } from "@element-plus/icons-vue";
import { ElNotification } from "element-plus";
import { getPoint } from "@/api/signal";
import { pointToPercent } from "@/utils/pointSwitch";
import { drawRadar } from "@/utils/draw";
import { exportExcel } from "@/utils/exportExcel";

const ifShowResult = ref(false);
const ifSearch = ref(false);
const search_data = reactive({
  domain_name: "",
  domain_type: "",
});
const signalData = reactive({
  data: {
    domainName: "",
    IP: "",
    cname: [],
    domainServer: "",
    nsServer: "",
    cdnServer: "",
    visitCount: 0,
    point: 0,
    pointMessage: "",
    data: [],
    aveData: [],
    detailAnalyse: "",
  },
});

const search = async () => {
  const { domain_name: n, domain_type: t } = search_data;
  const rule =
    /^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$/;
  console.log(n);

  if (t === "" || !rule.test(n)) {
    ElNotification({
      title: "错误",
      message: "请检查表单正确性",
      type: "error",
    });
    return;
  }
  ifSearch.value = true;
  ifShowResult.value = false;
  signalData.data = await getPoint(n);
  ifShowResult.value = true;
  drawRadar(
    document.getElementById("self_charts"),
    signalData.data.data,
    signalData.data.aveData
  );
};

const pointColor = ref("#f56c6c");
watch(
  () => signalData.data.point,
  (n) => {
    const percent = pointToPercent(n);
    if (percent < 25) return (pointColor.value = "#e36049");
    if (percent < 75) return (pointColor.value = "#e6a23c");
    if (percent <= 100) return (pointColor.value = "#5cb87a");
  }
);
const exportData = () => {
  return exportExcel(signalData.data);
};
</script>

<style lang='scss' scoped>
::v-deep(.el-descriptions__title) {
  font-size: 20px !important;
}
#self_charts {
  width: 100%;
  height: 100%;
}
.loading {
  width: 100%;
  height: 100%;
  margin-bottom: 50px;
}
#signal {
  .search_container {
    width: 500px;
    margin: 30px auto;
  }
  .el-card {
    margin-bottom: 20px;
  }
  .en_header {
    font-weight: 700;
  }
  .en_body {
    margin-top: 20px;
    .en_l {
      float: left;
      width: 50%;
      height: 300px;
      h3 {
        font-weight: normal;
        font-size: 16px;
      }
      .point_container {
        text-align: center;
        span {
          font-weight: 700;
          font-size: 60px;
          color: v-bind(pointColor);
        }
      }
      .en_process {
        margin-top: 20px;
        font-size: 12px;
        vertical-align: center;
      }
      .el-progress {
        width: 60%;
        display: inline-block;
      }
      .en_ifdanger {
        font-weight: 600;
        margin-top: 20px;
        color: v-bind(pointColor);
      }
    }

    .en_r {
      display: inline-block;
      width: 50%;
      height: 400px;
    }
  }
}
</style>