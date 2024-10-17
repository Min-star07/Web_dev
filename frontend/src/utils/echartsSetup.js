import * as echarts from "echarts";

export function setupChart(domElement, data, xLabel, yLabel) {
  let chart;
  if (echarts.getInstanceByDom(domElement)) {
    chart = echarts.getInstanceByDom(domElement);
  } else {
    chart = echarts.init(domElement);
  }

  const option = {
    xAxis: {
      type: "category",
      name: xLabel,
      nameLocation: "middle",
      nameGap: 25,
      axisLine: {
        lineStyle: {
          color: "black", // X-axis line color
        },
      },
      axisLabel: {
        color: "black", // X-axis label color
      },
      nameTextStyle: {
        color: "black", // X-axis name color
      },
    },
    yAxis: {
      type: "value",
      name: yLabel,
      nameLocation: "middle",
      nameGap: 40,
      axisLine: {
        lineStyle: {
          color: "black", // Y-axis line color
        },
      },
      axisLabel: {
        color: "black", // Y-axis label color
      },
      nameTextStyle: {
        color: "black", // Y-axis name color
      },
    },
    grid: {
      show: true,
      borderColor: "gray", // Grid border color
    },
    series: [
      {
        symbolSize: 5,
        data,
        type: "scatter",
        itemStyle: {
          color: "red", // Point color
        },
        lineStyle: {
          color: "black", // Line color
        },
      },
    ],
  };

  chart.setOption(option);
  return chart;
}
src / utils / updateCharts.js;
