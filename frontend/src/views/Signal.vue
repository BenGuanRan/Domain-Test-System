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
    <el-card shadow="hover">
      <el-descriptions
        class="margin-top"
        title="域名基础信息"
        :column="1"
        size="default"
        border
      >
        <template #extra>
          <el-button type="primary">导出excel</el-button>
        </template>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">域名</div>
          </template>
          www.baidu.com
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">IP</div>
          </template>
          127.0.0.1
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">CNAME</div>
          </template>
          a.cm、b.cc、aran.cc
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label> <div class="cell-item">服务商</div></template>
          阿里云
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">NS服务商</div>
          </template>
          No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
        </el-descriptions-item>
        <el-descriptions-item>
          <template #label>
            <div class="cell-item">CDN服务商</div>
          </template>
          No.1188, Wuzhong Avenue, Wuzhong District, Suzhou, Jiangsu Province
        </el-descriptions-item>
      </el-descriptions>
    </el-card>
    <el-card shadow="hover">
      <div style="font-size: 20px" class="en_header">综合评估</div>
      <div class="en_body">
        <div class="en_l">
          <h3>此域名综合得分:</h3>
          <div class="point_container">
            <span>{{ point }}</span> 分
            <div class="en_process">
              -9
              <el-progress
                :percentage="pointToPercent(point)"
                :color="pointColor"
              >
                &nbsp; </el-progress
              >+9
            </div>
            <div class="en_ifdanger">该域名存在风险！</div>
          </div>
        </div>
        <div class="en_c"></div>
        <div class="en_r"></div>
      </div>
    </el-card>
  </div>
</template>

<script lang='ts' setup>
import { reactive, ref, watch } from "vue";
import { Search } from "@element-plus/icons-vue";
import { ElNotification } from "element-plus";
import { getPoint } from "@/api/signal";
import { pointToPercent } from "@/utils/pointSwitch";

const search_data = reactive({
  domain_name: "",
  domain_type: "",
});
const point = ref(0);
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
  point.value = await getPoint(n);
};

const pointColor = ref("#f56c6c");
watch(point, (n) => {
  const percent = pointToPercent(n);
  if (percent < 25) return (pointColor.value = "#e36049");
  if (percent < 75) return (pointColor.value = "#e6a23c");
  if (percent <= 100) return (pointColor.value = "#5cb87a");
});
</script>

<style lang='scss' scoped>
::v-deep(.el-descriptions__title) {
  font-size: 20px !important;
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
      width: 33.33%;
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

    .en_c {
      width: 33.33%;
      
    }
  }
}
</style>