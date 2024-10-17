<script setup name="calibration">
import getresultHttp from "@/api/getresultHttp";
import OAMain from "@/components/OAMain.vue";
import { ElMessage } from "element-plus";
import { ref, reactive, onMounted, watch, computed } from "vue";
import { updateCharts } from "@/utils/updateCharts.js"; // Import the function
let pagination = reactive({
  total: 0,
  page: 1,
});
let rawdata = ref([]);
let page_size = ref(64);
let filterForm = reactive({
  WALL: 1,
  CB: 22,
  ROB: 15,
  Channel: null,
});

let charts = ref([
  { id: "chart1", yField: "Q0", yLabel: "Q0" },
  { id: "chart2", yField: "Q1", yLabel: "Q1" },
  { id: "chart3", yField: "Sigma0", yLabel: "Sigma0" },
  { id: "chart4", yField: "Sigma1", yLabel: "Sigma1" },
  { id: "chart5", yField: "w", yLabel: "w" },
  { id: "chart6", yField: "alpha", yLabel: "alpha" },
  { id: "chart7", yField: "mu", yLabel: "mu" },
  { id: "chart8", yField: "Chi2NDF", yLabel: "Chi2NDF" },
  { id: "chart9", yField: "gain", yLabel: "Gain" },
]);

// Computed properties to get unique values for WALL, CB, ROB, and Channel
const uniqueWalls = computed(() => {
  const walls = rawdata.value.map((item) => item.WALL);
  return [...new Set(walls)];
});

const uniqueCBs = computed(() => {
  const cbs = rawdata.value.map((item) => item.CB);
  return [...new Set(cbs)];
});

const uniqueROBs = computed(() => {
  const robs = rawdata.value.map((item) => item.ROB);
  return [...new Set(robs)];
});

const uniqueChannels = computed(() => {
  const channels = rawdata.value.map((item) => item.Channel);
  return [...new Set(channels)];
});

async function fetchList(page, page_size) {
  try {
    let tableData = await getresultHttp.getresult(page, page_size, filterForm);
    rawdata.value = tableData.results;
    pagination.total = tableData.count;
    updateCharts(rawdata.value, charts.value); // Update charts after fetching data
  } catch (details) {
    ElMessage.error(details);
  }
}

function onSearch() {
  pagination.page = 1;
  fetchList(1, page_size.value);
}
const onDownload = async () => {
  let rows = tableRef.value.getSelectionRows();
  if (!rows || rows.length === 0) {
    ElMessage.info("Select data");
    return;
  }

  try {
    // Map the selected rows to get their IDs
    let response = await getresultHttp.downloaddata(rows.map((row) => row.id));
    // let response = await staffHttp.downloadStaffs(rows.map(row => row.uid))

    // Create a URL for the blob response
    let href = URL.createObjectURL(response.data);
    const a = document.createElement("a");
    a.href = href;
    a.setAttribute("download", "calibrationdata.csv"); // Use the correct filename
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(href);
  } catch (detail) {
    // Clean up the URL object}
    // } catch (error) {
    //   ElMessage.error(error.message || "Error downloading file");
    // }
    ElMessage.error(detail);
  }
};

let tableRef = ref();

onMounted(() => {
  fetchList(1, page_size.value);
});

watch(
  () => pagination.page,
  (value) => {
    fetchList(value, page_size.value);
  }
);

watch(page_size, (value) => {
  if (pagination.page === 1) {
    fetchList(1, value);
  } else {
    pagination.page = 1;
  }
});
</script>

<template>
  <OAMain title="Calibration result">
    <el-card>
      <el-form :inline="true" class="my-form-inline">
        <el-form-item label="WALL">
          <el-select v-model="filterForm.WALL">
            <el-option
              v-for="wall in uniqueWalls"
              :label="wall"
              :value="wall"
              :key="wall"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="CB">
          <el-select v-model="filterForm.CB">
            <el-option
              v-for="cb in uniqueCBs"
              :label="cb"
              :value="cb"
              :key="cb"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="ROB">
          <el-select v-model="filterForm.ROB">
            <el-option
              v-for="rob in uniqueROBs"
              :label="rob"
              :value="rob"
              :key="rob"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="Channel">
          <el-select v-model="filterForm.Channel">
            <el-option
              v-for="channel in uniqueChannels"
              :label="channel"
              :value="channel"
              :key="channel"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" icon="Search" @click="onSearch"
            >Search</el-button
          >
        </el-form-item>
        <el-form-item>
          <el-button type="danger" icon="Download" @click="onDownload"
            >Download</el-button
          >
        </el-form-item>
      </el-form>
    </el-card>
    <el-card>
      <div class="charts-grid">
        <div v-for="(chart, index) in charts" :key="index" class="chart-item">
          <div :id="chart.id" style="width: 100%; height: 300px"></div>
        </div>
      </div>
    </el-card>
    <el-card>
      <el-table :data="rawdata" ref="tableRef">
        <el-table-column type="selection" width="55"></el-table-column>
        <el-table-column prop="id" label="ID" />
        <el-table-column prop="Date" label="Date" />
        <el-table-column prop="WALL" label="WALL" />
        <el-table-column prop="CB" label="CB" />
        <el-table-column prop="ROB" label="ROB" />
        <el-table-column prop="FEB" label="FEB" />
        <el-table-column prop="Channel" label="Channel" />
        <el-table-column prop="Chi2NDF_peak" label="Chi2NDF" />
        <el-table-column prop="mode" label="Mode" />
        <el-table-column prop="HV" label="HV" />
        <el-table-column prop="gain" label="Gain" />
        <el-table-column prop="N0" label="N0" />
        <el-table-column prop="Q0" label="Q0" />
        <el-table-column prop="Q1" label="Q1" />
        <el-table-column prop="Sigma0" label="Sigma0" />
        <el-table-column prop="Sigma1" label="Sigma1" />
        <el-table-column prop="w" label="w" />
        <el-table-column prop="alpha" label="alpha" />
      </el-table>
      <template #footer>
        <div style="display: flex; justify-content: space-between">
          <el-form-item label="Page:">
            <el-select v-model="page_size" size="small" style="width: 100px">
              <el-option label="8 item/page" :value="8" />
              <el-option label="64 item/page" :value="64" />
              <el-option label="128 item/page" :value="128" />
            </el-select>
          </el-form-item>
          <el-pagination
            background
            layout="prev, pager, next"
            :total="pagination.total"
            v-model:currentPage="pagination.page"
            :page-size="page_size"
          />
        </div>
      </template>
    </el-card>
  </OAMain>
</template>

<style scoped>
.my-form-inline .el-input {
  --el-input-width: 140px;
}

.my-form-inline .el-select {
  --el-select-width: 140px;
}

.el-form--inline .el-form-item {
  margin-right: 20px;
}

.charts-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.chart-item {
  width: 100%;
  height: 300px;
}
</style>
