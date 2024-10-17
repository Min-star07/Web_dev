<script setup name="home">
import OAMain from "@/components/OAMain.vue";
import { ElMessage } from "element-plus";
import { ref, reactive, onMounted, computed } from "vue";
import homeHttp from "@/api/homeHttp";
import * as echarts from "echarts";
import axios from "axios";
// Reactive filter form
const filterForm = reactive({
  WALL: "",
  CB: "",
  ROB: "",
  Channel: "",
});

// Ref to hold raw data and chart URL
const rawdata = ref([]);
const chartQ1Url = ref("");
const chartGainUrl = ref("");
const loading = ref(false); // Loader ref to indicate fetching status
async function fetchChartQ1() {
  try {
    // Make API call to get the image
    const response = await homeHttp.testQ1(filterForm);
    // Check status code and data type
    if (response && response.status === 200) {
      // Verify if the response data is a Blob
      if (response.data instanceof Blob) {
        // console.log("Response Blob:", response.data); // Log the Blob (image) data
        // Create a URL for the Blob data
        const blob = response.data;
        chartQ1Url.value = URL.createObjectURL(blob); // Convert Blob to object URL
        // console.log("Chart image URL:", chartQ1Url.value); // Log the created URL
      } else {
        console.error(
          "Response data is not a Blob. Data type:",
          typeof response.data
        );
      }
    } else {
      throw new Error(`Unexpected response status: ${response?.status}`);
    }
  } catch (error) {
    console.error("Fetch error:", error); // Log any errors that occur during the API call
  }
}

async function fetchChartGain() {
  try {
    // Make API call to get the image
    const response = await homeHttp.testGain(filterForm);
    // Check status code and data type
    if (response && response.status === 200) {
      // Verify if the response data is a Blob
      if (response.data instanceof Blob) {
        // console.log("Response Blob:", response.data); // Log the Blob (image) data
        // Create a URL for the Blob data
        const blob = response.data;
        chartGainUrl.value = URL.createObjectURL(blob); // Convert Blob to object URL
        // console.log("Chart image URL:", chartQ1Url.value); // Log the created URL
      } else {
        console.error(
          "Response data is not a Blob. Data type:",
          typeof response.data
        );
      }
    } else {
      throw new Error(`Unexpected response status: ${response?.status}`);
    }
  } catch (error) {
    console.error("Fetch error:", error); // Log any errors that occur during the API call
  }
}

// Function to fetch data based on filterForm
async function fetchList() {
  loading.value = true;
  try {
    const response = await homeHttp.testresultshow();
    rawdata.value = response;

    // Unique processing for "WALL" values
    let data = rawdata.value.map((item) => item.WALL);
    data = [...new Set(data)];
    let uniqueWallCount = data.length;

    // Initialize the echarts instance
    var myChart = echarts.init(document.getElementById("main"));

    // Specify the configuration items and data for the chart
    var option = {
      title: {
        text: "Installation process",
        left: "center",
      },
      tooltip: {
        trigger: "item",
      },
      series: [
        {
          name: "Access From",
          type: "pie",
          radius: "50%",
          data: [
            {
              value: uniqueWallCount,
              name: "Finished",
              itemStyle: { color: "blue" },
            },
            {
              value: 63 - uniqueWallCount,
              name: "Not finished",
              itemStyle: { color: "red" },
            },
          ],
          emphasis: {
            itemStyle: {
              shadowBlur: 10,
              shadowOffsetX: 0,
              shadowColor: "rgba(0, 0, 0, 0.5)",
            },
          },
        },
      ],
    };
    myChart.setOption(option);
  } catch (error) {
    console.error("Error fetching list:", error); // Log the error for debugging
    ElMessage.error(error.message); // Show error message
  } finally {
    loading.value = false; // Stop loading indicator
  }
}

// Computed properties to get unique values for filters
const uniqueWalls = computed(() => [
  ...new Set(rawdata.value.map((item) => item.WALL)),
]);
const uniqueCBs = computed(() => [
  ...new Set(rawdata.value.map((item) => item.CB)),
]);
const uniqueROBs = computed(() => [
  ...new Set(rawdata.value.map((item) => item.ROB)),
]);
const uniqueChannels = computed(() => [
  ...new Set(rawdata.value.map((item) => item.Channel)),
]);

// Fetch data and chart on component mount
onMounted(async () => {
  fetchList();
  fetchChartQ1();
  fetchChartGain();
});

// Function to handle search
async function onSearch() {
  try {
    await fetchList(); // Fetch the filtered list
    await fetchChartQ1(); // Fetch the filtered chart
    await fetchChartGain(); // Fetch the filtered gain
  } catch (error) {
    console.error("Error during search:", error);
    ElMessage.error(error.message);
  }
}
</script>

<template>
  <OAMain title="HOME">
    <!-- Pie chart rendered with echarts -->
    <el-card>
      <div id="main" style="width: 100%; height: 400px"></div>
    </el-card>

    <!-- Filter Form -->
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
      </el-form>

      <!-- Display dynamically fetched Matplotlib chart with loading indicator -->
      <div class="block">
        <div class="image-container">
          <el-image v-if="chartQ1Url" :src="chartQ1Url" class="image" />
          <div v-else class="image-slot">Loading chart...</div>

          <el-image v-if="chartGainUrl" :src="chartGainUrl" class="image" />
          <div v-else class="image-slot">Loading second chart...</div>
        </div>
      </div>
    </el-card>
  </OAMain>
</template>

<style scoped>
.image-container {
  display: flex; /* Use flexbox for layout */
  justify-content: space-between; /* Optional: space images apart */
  align-items: center; /* Center images vertically */
}

.image {
  width: 48%; /* Adjust width to fit two images in one row */
  margin: 0 1%; /* Optional: Add some margin for spacing */
}

.image-slot {
  width: 48%; /* Match width of images */
  height: 100px; /* Set a fixed height for loading state */
  background-color: #f0f0f0; /* Light grey background for loading state */
  display: flex; /* Center the text */
  justify-content: center;
  align-items: center;
  border: 1px dashed #ccc; /* Optional: dashed border for visual distinction */
}

.my-form-inline .el-input {
  --el-input-width: 140px;
}

.my-form-inline .el-select {
  --el-select-width: 140px;
}

.el-form--inline .el-form-item {
  margin-right: 20px;
}
</style>
