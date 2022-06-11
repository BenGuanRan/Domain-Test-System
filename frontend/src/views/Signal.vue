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
            <el-option label="娱乐服务" value="2" />
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
            {{ signalData.data.register }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">NS服务商</div>
            </template>
            {{ signalData.data.NSServer }}
          </el-descriptions-item>
          <el-descriptions-item>
            <template #label>
              <div class="cell-item">CDN服务商</div>
            </template>
            {{ signalData.data.CDNServer || "暂无" }}
          </el-descriptions-item>
        </el-descriptions>
      </el-card>
      <el-card shadow="never" style="position: relative">
        <div class="en_body">
          <div class="beauty_box" v-if="!ifSearch"></div>
          <div class="en_l" v-if="ifShowResult">
            <div style="font-size: 20px; margin-top: -20px" class="en_header">
              综合评估
            </div>
            <div v-if="signalData.data.visit_count">
              该域名的日访问量为
              <span class="visit_color" style="font-size: 20px">{{
                signalData.data.visit_count
              }}</span>
              人次
            </div>
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
              <div class="en_ifdanger">{{ signalData.data.pointmessage }}</div>
            </div>
          </div>
          <div ref="node" class="en_r">
            <div class="loading" v-if="ifSearch && !ifShowResult">
              <loading></loading>
            </div>

            <div id="self_charts"></div>
          </div>
        </div>
      </el-card>
      <el-card v-if="ifShowResult" shadow="never">
        <div style="font-size: 20px" class="en_header">具体分析</div>
        <p v-if="signalData.data.pointmessage === '不存在风险'">
          该域名综合影响力
          <span :style="{ color: randerColor[1], fontSize: '18px' }">
            {{ signalData.data.detailanalyse[0] }}
          </span>
          ,该类型域名平均得分为
          <span :style="{ color: randerColor[2], fontSize: '18px' }">
            {{ signalData.data.detailanalyse[1] }}
          </span>
          ,从域名解析背后实体的国家属性来看此域名是安全的!
        </p>
        <p v-else>
          该域名综合影响力
          <span :style="{ color: randerColor[1], fontSize: '18px' }">
            {{ signalData.data.detailanalyse[0] }}
          </span>
          ,该类型域名平均得分为
          <span :style="{ color: randerColor[2], fontSize: '18px' }">
            {{ signalData.data.detailanalyse[1] }}
          </span>
          ,此域名除顶级域名一项之外，
          <span :style="{ color: randerColor[3], fontSize: '18px' }">
            {{ signalData.data.detailanalyse[2] }}
          </span>
          一项得分最低，
          <span :style="{ color: randerColor[4], fontSize: '18px' }">
            {{ signalData.data.detailanalyse[3] }}
          </span>
          ,修改后域名的总体得分为
          <span :style="{ color: randerColor[5], fontSize: '18px' }">
            {{ signalData.data.detailanalyse[4] }} </span
          >!
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
    register: "",
    NSServer: "",
    CDNServer: "",
    visit_count: 0,
    point: 0,
    pointmessage: "",
    data: [],
    avedata: [],
    detailanalyse: "",
  },
});

onMounted(() => {
  // 添加全局enter事件
  document.onkeyup = (e) => {
    if (e.keyCode === 13) {
      document.onkeyup = null;
      return search();
    }
  };
});

const search = async () => {
  const { domain_name: n, domain_type: t } = search_data;
  const rule =
    /^(?=^.{3,255}$)[a-zA-Z0-9][-a-zA-Z0-9]{0,62}(\.[a-zA-Z0-9][-a-zA-Z0-9]{0,62})+$/;
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
  signalData.data = (await getPoint(n, t)).data;
  console.log(signalData.data);

  ifShowResult.value = true;
  drawRadar(
    document.getElementById("self_charts"),
    signalData.data.data,
    signalData.data.avedata
  );
};

// 颜色管理
const pointColor = ref("#f56c6c");
const visitColor = ref("#f56c6c");
const randerColor = ref([""]);
watch(
  () => signalData.data.point,
  (n) => {
    const percent = pointToPercent(n);
    if (percent < 25) return (pointColor.value = "#e36049");
    if (percent < 75) return (pointColor.value = "#e6a23c");
    if (percent <= 100) return (pointColor.value = "#5cb87a");
  }
);
watch(
  () => signalData.data.visit_count,
  (n) => {
    if (n < 10000) return (visitColor.value = "#27bdde");
    if (n < 100000) return (visitColor.value = "#fedd42");
    if (n <= 1000000) return (visitColor.value = "#fb972a");
    if (n > 1000000) return (visitColor.value = "#f74e60");
  }
);
watch(
  () => signalData.data.pointmessage,
  (n) => {
    const colors = [
      "#48c9b0",
      "#198ae0",
      "#26c0de",
      "#23d28f",
      "#bc6aa9",
      "#bdb76b",
      "#fd982f",
      "#f94c66",
      "#a85661",
      "#6d5741",
      "#259544",
    ];
    let num = Math.floor(Math.random() * (10 - 0 + 1)) + 0;
    console.log(num);

    if (n === "存在一定风险") {
      // 随机五个颜色
      for (let i = 0; i < 5; i++) {
        randerColor.value.push(colors[num++ % 11]);
      }
    } else {
      // 随机两个颜色
      for (let i = 0; i < 2; i++) {
        randerColor.value.push(colors[num++ % 11]);
      }
    }
    console.log(randerColor.value);
  }
);
const exportData = () => {
  return exportExcel(signalData.data);
};
</script>

<style lang='scss' scoped>
.beauty_box {
  background-image: url(../assets/logo.png);
  z-index: 1;
  background-position: center 8%;
  background-size: 60%;
  background-repeat: no-repeat;
  position: absolute;
  width: 100%;
  height: 1000px;
}
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
  font-weight: 500;
  .search_container {
    background-color: #fff;
    width: 500px;
    margin: 30px auto;
  }
  .el-card {
    margin-bottom: 20px;
  }
  .en_header {
    margin-bottom: 20px;
    font-weight: 700;
  }
  .en_body {
    height: 100%;
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
        margin-top: 50px;
        text-align: center;
        span {
          font-weight: 700;
          font-size: 60px;
          color: v-bind(pointColor);
        }
      }
      .en_process {
        margin-top: 30px;
        font-size: 12px;
        vertical-align: center;
      }
      .el-progress {
        width: 60%;
        display: inline-block;
      }
      .en_ifdanger {
        font-size: 30px;
        font-weight: 600;
        margin-top: 40px;
        color: v-bind(pointColor);
      }
      .visit_color {
        color: v-bind(visitColor);
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