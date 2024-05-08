
/*Statistics*/

function barChart() {
  setTimeout(() => {
    var options = {
      series: [{
        name: 'Male',
        data: [44, 55, 57, 56, 61, 58, 63, 60, 66, 39, 67, 84],
      }, {
        name: 'Female',
        data: [76, 85, 101, 98, 87, 105, 91, 114, 94, 62, 88, 59],
      }, {
        name: 'Others',
        data: [35, 41, 36, 26, 45, 48, 52, 53, 41, 28, 47, 54],
      }],
      colors: [myVarVal, "#9258f1", "#00b9ff"],
      chart: {
        type: 'bar',
        height: 300,
        dropShadow: {
          enabled: false,
          enabledOnSeries: undefined,
          top: 5,
          left: 0,
          blur: 0,
          color: "#000",
          opacity: 0,
        }
      },
      grid: {
        borderColor: "rgba(119, 119, 142, 0.1)",
      },
      plotOptions: {
        bar: {
          horizontal: false,
          columnWidth: '50%',
          endingShape: 'rounded',
          borderRadius: 5
        },
      },
      dataLabels: {
        enabled: false
      },
      stroke: {
        show: true,
        width: 2,
        colors: ['transparent']
      },
      xaxis: {
        categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
        axisTicks: {
          show: true,
          color: "rgba(119, 119, 142, 0.05)",
        },
        axisBorder: {
          show: true,
          color: "rgba(119, 119, 142, 0.05)",
        }
      },
      yaxis: {
      },
      legend: {
        position: "top",
        horizontalAlign: "right",
        fontSize: "14px",
        fontFamily: "Poppins",
        offsetY: 10,
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
        itemMargin: {
          horizontal: 10
        }
      },
      fill: {
        opacity: 1
      },
      tooltip: {
        y: {
          formatter: function (val) {
            return val + " Patients"
          }
        }
      }
    };

    document.querySelector("#statistics").innerHTML = "";
    var chart = new ApexCharts(document.querySelector("#statistics"), options);
    chart.render();
  }, 100);
}

/*Statistics*/

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

/*Pie Chart*/

var options = {
  series: [44, 55, 41, 17, 15],
  colors: ["#1753fccc", "#9258fccc", "#00b9fccc", "#22c03ccc", "#ee335ccc"],
  labels: ["Excellent", "Great", "Good", "Average", "Poor"],
  chart: {
    type: 'donut',
    height: 315
  },
  dataLabels: {
    enabled: true,
    dropShadow: {
      enabled: false,
    }
  },
  legend: {
    position: "bottom",
    offsetX: 0,
    offsetY: 10,
    fontSize: "15px",
    fontFamily: "Poppins",
    labels: {
      colors: "#74767c",
    },
    markers: {
      width: 9,
      height: 9,
      strokeWidth: 0,
      radius: 12,
      offsetX: -5,
      offsetY: -1,
    },
    itemMargin: {
      vertical: 10,
    },
  },
  responsive: [{
    breakpoint: 480,
    options: {
      chart: {
        width: 200
      },
      legend: {
        position: 'bottom',
        fontFamily: ""
      }
    }
  }]
};

var chart = new ApexCharts(document.querySelector("#pieChart"), options);
chart.render();

/*Pie Chart*/