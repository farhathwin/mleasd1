
/*Data Table*/

$(function (e) {
  //______Data-Table
  $("#data-table").DataTable({
    language: {
      searchPlaceholder: "Search...",
      sSearch: "",
    },
  });
  // ______Select2
  $(".select2").select2({
    minimumResultsForSearch: Infinity,
    width: '60px'
  });
});

/*Data Table*/

/*closed Apex charts(#bar)*/
function barOne() {
  setTimeout(() => {
    var options1 = {
      series: [
        {
          name: "Amount Used",
          type: "line",
          data: [40, 35, 78, 50, 75, 48, 62, 47, 80, 56, 40, 50],
        },
        {
          name: "Total Budget",
          type: "area",
          data: [45, 30, 65, 35, 50, 70, 38, 60, 36, 65, 32, 45],
        },
      ],
      chart: {
        height: 335,
        type: "line",
        zoom: {
          enabled: false,
        },
        dropShadow: {
          enabled: false,
          enabledOnSeries: undefined,
          top: 5,
          left: 0,
          blur: 0,
          color: "#000",
          opacity: 0,
        },
      },
      grid: {
        borderColor: "rgba(119, 119, 142, 0.1)",
      },
      dataLabels: {
        enabled: false,
      },
      stroke: {
        width: [2, 2],
        curve: "smooth",
        dashArray: [0, 0],
      },
      fill: {
        opacity: [1, 0.1],
        gradient: {
          inverseColors: false,
          shade: "light",
          type: "vertical",
          opacityFrom: 0.85,
          opacityTo: 0.55,
          stops: [0, 20, 50, 100],
        },
      },
      legend: {
        show: true,
        position: "top",
        horizontalAlign: "center",
        fontWeight: 600,
        offsetY: 10,
        tooltipHoverFormatter: function (val, opts) {
          return (
            val +
            " - " +
            opts.w.globals.series[opts.seriesIndex][opts.dataPointIndex] +
            ""
          );
        },
        labels: {
          colors: "#74767c",
        },
        markers: {
          width: 9,
          height: 9,
          strokeWidth: 0,
          radius: 12,
          offsetX: 0,
          offsetY: 0,
        },
      },
      markers: {
        discrete: [
          {
            seriesIndex: 0,
            dataPointIndex: 4,
            fillColor: "#fff",
            strokeColor: myVarVal,
            size: 5,
            shape: "circle",
          },
          {
            seriesIndex: 1,
            dataPointIndex: 6,
            fillColor: "#fff",
            strokeColor: "#9258f1",
            size: 5,
            shape: "circle",
          },
        ],
        hover: {
          sizeOffset: 6,
        },
      },
      colors: [myVarVal, "#9258f1"],
      xaxis: {
        categories: [
          "Jan",
          "Feb",
          "Mar",
          "Apr",
          "May",
          "Jun",
          "Jul",
          "Aug",
          "Sep",
          "Oct",
          "Nov",
          "Dec",
        ],
        axisBorder: {
          show: true,
          color: "rgba(119, 119, 142, 0.05)",
        },
        axisTicks: {
          show: true,
          color: "rgba(119, 119, 142, 0.05)",
        },
      },
      tooltip: {
        y: [
          {
            title: {
              formatter: function (val) {
                return val + " (mins)";
              },
            },
          },
          {
            title: {
              formatter: function (val) {
                return val + " per session";
              },
            },
          },
          {
            title: {
              formatter: function (val) {
                return val;
              },
            },
          },
        ],
      },
      // 

    };
    document.getElementById("barOne").innerHTML = "";
    var chart1 = new ApexCharts(document.querySelector("#barOne"), options1);
    chart1.render();
  }, 300);
}

// CHARTJS LEADS CHART  OPEN
var ctx1 = document.getElementById("leadschart").getContext("2d");
new Chart(ctx1, {
  type: "line",
  data: {
    labels: [
      "Date 1",
      "Date 2",
      "Date 3",
      "Date 4",
      "Date 5",
      "Date 6",
      "Date 7",
      "Date 8",
      "Date 9",
      "Date 10",
      "Date 11",
      "Date 12",
      "Date 13",
      "Date 14",
      "Date 15",
    ],
    datasets: [
      {
        label: "Total Sales",
        data: [32, 54, 32, 88, 10, 72, 52, 32, 69, 48, 32, 58],
        backgroundColor: "transparent",
        borderColor: "#1753fc",
        borderWidth: "2.5",
        pointBorderColor: "transparent",
        pointBackgroundColor: "transparent",
        lineTension: 0.3,
      },
    ],
  },
  options: {
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
        labels: {
          display: false,
        },
      },
      tooltip: {
        enabled: false,
      },
    },
    responsive: true,
    scales: {
      x: {
        ticks: {
          beginAtZero: true,
          fontSize: 10,
          fontColor: "transparent",
        },
        title: {
          display: false,
        },
        grid: {
          display: true,
          color: "transparent",
          drawBorder: false,
        },
        categoryPercentage: 1.0,
        barPercentage: 1.0,
        barDatasetSpacing: 0,
        display: false,
        barThickness: 5,
      },
      y: {
        display: false,
        ticks: {
          display: false,
        },
      },
    },
    title: {
      display: false,
    },
    elements: {
      point: {
        radius: 0,
      },
    },
  },
});
// CHARTJS LEADS CHART CLOSED

// CHARTJS LEADS CHART  OPEN
var ctx1 = document.getElementById("leadschart2").getContext("2d");
new Chart(ctx1, {
  type: "line",
  data: {
    labels: [
      "Date 1",
      "Date 2",
      "Date 3",
      "Date 4",
      "Date 5",
      "Date 6",
      "Date 7",
      "Date 8",
      "Date 9",
      "Date 10",
      "Date 11",
      "Date 12",
      "Date 13",
      "Date 14",
      "Date 15",
    ],
    datasets: [
      {
        label: "Total Sales",
        data: [3, 50, 25, 66, 9, 56, 12, 30, 50, 20, 30, 20],
        backgroundColor: "transparent",
        borderColor: "#9258f1",
        borderWidth: "2.5",
        pointBorderColor: "transparent",
        pointBackgroundColor: "transparent",
        lineTension: 0.3,
      },
    ],
  },
  options: {
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
        labels: {
          display: false,
        },
      },
      tooltip: {
        enabled: false,
      },
    },
    responsive: true,
    scales: {
      x: {
        ticks: {
          beginAtZero: true,
          fontSize: 10,
          fontColor: "transparent",
        },
        title: {
          display: false,
        },
        grid: {
          display: true,
          color: "transparent",
          drawBorder: false,
        },
        categoryPercentage: 1.0,
        barPercentage: 1.0,
        barDatasetSpacing: 0,
        display: false,
        barThickness: 5,
      },
      y: {
        display: false,
        ticks: {
          display: false,
        },
      },
    },
    title: {
      display: false,
    },
    elements: {
      point: {
        radius: 0,
      },
    },
  },
});
// CHARTJS LEADS CHART CLOSED

// CHARTJS LEADS CHART  OPEN
var ctx1 = document.getElementById("leadschart3").getContext("2d");
new Chart(ctx1, {
  type: "line",
  data: {
    labels: [
      "Date 1",
      "Date 2",
      "Date 3",
      "Date 4",
      "Date 5",
      "Date 6",
      "Date 7",
      "Date 8",
      "Date 9",
      "Date 10",
      "Date 11",
      "Date 12",
      "Date 13",
      "Date 14",
      "Date 15",
    ],
    datasets: [
      {
        label: "Total Sales",
        data: [26, 10, 55, 33, 55, 44, 66, 9, 66, 25, 50, 3],
        backgroundColor: "transparent",
        borderColor: "#e34a42",
        borderWidth: "2.5",
        pointBorderColor: "transparent",
        pointBackgroundColor: "transparent",
        lineTension: 0.3,
      },
    ],
  },
  options: {
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
        labels: {
          display: false,
        },
      },
      tooltip: {
        enabled: false,
      },
    },
    responsive: true,
    scales: {
      x: {
        ticks: {
          beginAtZero: true,
          fontSize: 10,
          fontColor: "transparent",
        },
        title: {
          display: false,
        },
        grid: {
          display: true,
          color: "transparent",
          drawBorder: false,
        },
        categoryPercentage: 1.0,
        barPercentage: 1.0,
        barDatasetSpacing: 0,
        display: false,
        barThickness: 5,
      },
      y: {
        display: false,
        ticks: {
          display: false,
        },
      },
    },
    title: {
      display: false,
    },
    elements: {
      point: {
        radius: 0,
      },
    },
  },
});
// CHARTJS LEADS CHART CLOSED

// CHARTJS LEADS CHART  OPEN
var ctx1 = document.getElementById("leadschart4").getContext("2d");
new Chart(ctx1, {
  type: "line",
  data: {
    labels: [
      "Date 1",
      "Date 2",
      "Date 3",
      "Date 4",
      "Date 5",
      "Date 6",
      "Date 7",
      "Date 8",
      "Date 9",
      "Date 10",
      "Date 11",
      "Date 12",
      "Date 13",
      "Date 14",
      "Date 15",
    ],
    datasets: [
      {
        label: "Total Sales",
        data: [9, 2, 27, 8, 81, 10, 45, 25, 66, 20, 87, 12],
        backgroundColor: "transparent",
        borderColor: "#22c03c",
        borderWidth: "2.5",
        pointBorderColor: "transparent",
        pointBackgroundColor: "transparent",
        lineTension: 0.3,
      },
    ],
  },
  options: {
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false,
        labels: {
          display: false,
        },
      },
      tooltip: {
        enabled: false,
      },
    },
    responsive: true,
    scales: {
      x: {
        ticks: {
          beginAtZero: true,
          fontSize: 10,
          fontColor: "transparent",
        },
        title: {
          display: false,
        },
        grid: {
          display: true,
          color: "transparent",
          drawBorder: false,
        },
        categoryPercentage: 1.0,
        barPercentage: 1.0,
        barDatasetSpacing: 0,
        display: false,
        barThickness: 5,
      },
      y: {
        display: false,
        ticks: {
          display: false,
        },
      },
    },
    title: {
      display: false,
    },
    elements: {
      point: {
        radius: 0,
      },
    },
  },
});
// CHARTJS LEADS CHART CLOSED

/*Morris Bar*/

$(function (e) {

  new Morris.Donut({
    element: 'morrisBar9',
    data: [
      { value: 50, label: 'Campaign 1' },
      { value: 30, label: 'Campaign 2' },
      { value: 20, label: 'Campaign 3' },
    ],
    backgroundColor: '#fff',
    labelColor: '#212529',
    colors: [
      '#1753fc ', '#9258f1', '#fdb901'
    ],

    resize: true,
    formatter: function (x) { return x + "%" }
  });

  /* lineChart1 */

  var ctx = $('#lineChart1');
  ctx.height(250);
  var myChart = new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"],
      datasets: [{
        label: "Campaign",
        borderColor: "transparent",
        borderWidth: "4",
        backgroundColor: "#1753fc",
        data: [53, 46, 65, 56, 72, 46, 63],

      }]
    },
    options: {
      scales: {
        x: {
          ticks: {
            fontColor: "#bbc1ca",
          },
          display: true,
          gridLines: {
            color: 'rgba(0,0,0,0.03)'
          }
        },
        y: {
          ticks: {
            fontColor: "#bbc1ca",
          },
          display: true,
          gridLines: {
            display: true,
          }
        }
      },
      legend: {
        display: false,
        labels: {
          fontColor: "#bbc1ca",
        },
      },
      responsive: true,
      maintainAspectRatio: false,
      tooltips: {
        mode: 'index',
        intersect: false,
      },
      tooltips: {},
      hover: {
        mode: 'nearest',
        intersect: true
      }
    }
  });

  /* lineChart1 end */

});

/*Morris Bar*/