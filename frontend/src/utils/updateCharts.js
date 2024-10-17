import * as echarts from "echarts";

let chartInstances = {};

/**
 * Update the charts with the given raw data and chart configurations.
 * @param {Array} rawdata - The data used for updating the charts.
 * @param {Array} charts - The configurations for each chart to be updated.
 */
export function updateCharts(rawdata, charts) {
  charts.forEach((chart) => {
    let xdata = [];
    let ydata = [];

    // Prepare the data for the chart
    for (let row of rawdata) {
      xdata.push(row.Channel);
      ydata.push(row[chart.yField]);
    }
    let scatterData = xdata.map((x, index) => [x, ydata[index]]);
    const chartDom = document.getElementById(chart.id);

    // Check if the chart DOM element exists
    if (!chartDom) {
      console.warn(`Chart DOM element for ${chart.id} not found.`);
      return; // Exit early if the chart DOM element doesn't exist
    }

    let myChart;
    // Initialize or retrieve the chart instance
    if (chartInstances[chart.id]) {
      myChart = chartInstances[chart.id];
    } else {
      myChart = echarts.init(chartDom);
      chartInstances[chart.id] = myChart;
    }

    // Chart options
    let option = {
      grid: {
        left: "20%",
        right: "20%",
        top: "20%",
        bottom: "20%",
      },
      xAxis: {
        name: "Channel",
        nameLocation: "center",
        nameTextStyle: {
          color: "black",
          fontWeight: "bold",
          padding: 20,
        },
        axisLabel: {
          color: "black",
        },
        axisLine: {
          lineStyle: {
            color: "black",
          },
        },
      },
      yAxis: {
        name: chart.yLabel,
        nameLocation: "center",
        nameTextStyle: {
          color: "black",
          fontWeight: "bold",
          padding: 20,
        },
        axisLabel: {
          color: "black",
        },
        axisLine: {
          lineStyle: {
            color: "black",
          },
        },
      },
      series: [
        {
          symbolSize: 5,
          data: scatterData,
          type: "scatter",
          itemStyle: {
            color: "red", // Point color
          },
        },
      ],
      tooltip: {
        trigger: "axis",
      },
      toolbox: {
        show: true,
        right: "10%",
        top: "5%",
        feature: {
          dataView: { readOnly: false },
          saveAsImage: {},
        },
      },
    };

    // Update chart options and handle errors
    try {
      myChart.setOption(option);
    } catch (error) {
      console.error(`Error setting chart options for ${chart.id}:`, error);
    }
  });
}

// Event listener for resizing charts
window.addEventListener("resize", () => {
  Object.values(chartInstances).forEach((chart) => {
    chart.resize(); // Resize each chart on window resize
  });
});
