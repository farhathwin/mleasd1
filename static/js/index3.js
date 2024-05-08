
/* sparkline_bar1 */
$(".sparkline_bar1").sparkline([2, 4, 3, 4, 5, 4], {
  type: 'bar',
  height: 50,
  width: 50,
  barWidth: 5,
  barSpacing: 9,
  colorMap: {
    '9': '#a1a1a1'
  },
  barColor: '#f33540'
});
/* sparkline_bar1 end */

/* sparkline_bar2 */
$(".sparkline_bar2").sparkline([2, 4, 3, 4, 5, 4], {
  type: 'bar',
  height: 50,
  width: 50,
  barWidth: 5,
  barSpacing: 9,
  colorMap: {
    '9': '#a1a1a1'
  },
  barColor: '#1753fc'
});
/* sparkline_bar2 end */

/* sparkline_bar3 */
$(".sparkline_bar3").sparkline([2, 4, 3, 4, 5, 4], {
  type: 'bar',
  height: 50,
  width: 50,
  barWidth: 5,
  barSpacing: 9,
  colorMap: {
    '9': '#a1a1a1'
  },
  barColor: '#3582ec'
});
/* sparkline_bar3 end */

/* sparkline_bar4 */
$(".sparkline_bar4").sparkline([2, 4, 3, 4, 5, 4], {
  type: 'bar',
  height: 50,
  width: 50,
  barWidth: 5,
  barSpacing: 9,
  colorMap: {
    '9': '#a1a1a1'
  },
  barColor: '#f35e90'
});
/* sparkline_bar4 end */

/*Area Chart*/

function areaChart() {
  setTimeout(() => {
    var options = {
      series: [{
      name: 'Team A',
      data: [26, 44, 65, 33, 75, 32, 100]
    }, {
      name: 'Team B',
      data: [100, 59, 74, 17, 34, 52, 41]
    }],
      chart: {
      height: 350,
      type: 'area'
    },
    colors: [myVarVal, "#9258f1"],
    dataLabels: {
      enabled: false
    },
    stroke: {
      curve: 'smooth',
      width: ["3", "3"]
    },
    legend: {
      position: "top",
      horizontalAlign: "center",
      fontSize: "14px",
      fontFamily: "Poppins",
      labels: {
          colors: "#74767c"
      },
      markers: {
          width: 9,
          height: 9,
          strokeWidth: 0,
          radius: 12,
          offsetX: -3,
          offsetY: 0,
      },
      itemMargin: {
          horizontal: 10
      }
    },
    grid: {
      borderColor: 'rgba(119, 119, 142, 0.1)'
    },
    xaxis: {
      type: 'datetime',
      categories: ["2018-09-19T00:00:00.000Z", "2018-09-19T01:30:00.000Z", "2018-09-19T02:30:00.000Z", "2018-09-19T03:30:00.000Z", "2018-09-19T04:30:00.000Z", "2018-09-19T05:30:00.000Z", "2018-09-19T06:30:00.000Z"],
      axisBorder: {
        show: true,
        color: 'rgba(119, 119, 142, 0.05)',
        offsetX: 0,
        offsetY: 0,
      },
      labels: {
        style: {
          colors: '#7987a1',
        }
      },
      axisTicks: {
        show: true,
        borderType: 'solid',
        color: 'rgba(119, 119, 142, 0.05)',
        width: 6,
        offsetX: 0,
        offsetY: 0
      }
    },
    tooltip: {
      x: {
        format: 'dd/MM/yy HH:mm'
      },
    },
    };
    
    document.querySelector("#chart3").innerHTML = "";
    var chart = new ApexCharts(document.querySelector("#chart3"), options);
    chart.render();
  }, 100);
}

/*Area Chart*/

/*Project Report*/

function projectReport() {
	setTimeout(() => {
		var options = {
			series: [{
				name: 'Project One',
				data: [50, 33, 41, 67, 22, 43, 19, 62, 15, 26, 56, 12]
			}, {
				name: 'Project Two',
				data: [30, 15, 20, 8, 13, 27, 38, 10, 18, 22, 32, 29]
			},
			],
			chart: {
				type: 'bar',
				height: 310,
				stacked: true,
				toolbar: {
					show: true
				},
				zoom: {
					enabled: true
				}
			},
			colors: ["var(--primary-8)", "#e4e7ed"],
			responsive: [{
				breakpoint: 480,
				options: {
					legend: {
						position: 'bottom',
						offsetX: -10,
						offsetY: 0
					}
				}
			}],
			plotOptions: {
				bar: {
					horizontal: false,
					borderRadius: 0,
					columnWidth: "50%",
					dataLabels: {
						total: {
							enabled: true,
							style: {
								fontSize: '13px',
								fontWeight: 900
							}
						}
					}
				},
			},
			grid: {
				borderColor: "rgba(119, 119, 142, 0.1)",
			},
			xaxis: {
				type: 'month',
				categories: ['Jan', 'Feb', 'Mar', 'Apr',
					'May', 'Jun', 'Jul', 'Aug', "Sep", "Oct", "Nov", "Dec"
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
			legend: {
				position: 'bottom',
				offsetY: 8,
				fontFamily: "Poppins",
				fontSize: "12px",
				labels: {
					colors: "#74767c",
				},
				markers: {
					width: 9,
					height: 9,
					strokeWidth: 0,
					radius: 12,
					offsetX: -2,
					offsetY: -1,
				},
				itemMargin: {
					horizontal: 10,
					vertical: 0
				},
			},
			dataLabels: {
				enabled: false
			},
			fill: {
				opacity: 1
			}
		};

		document.getElementById("projectReport").innerHTML = "";
		var chart = new ApexCharts(document.querySelector("#projectReport"), options);
		chart.render();
	}, 300);
}

/*Project Report*/