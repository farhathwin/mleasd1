
/*Bar Chart*/

function revenueStatistics() {
	setTimeout(() => {

		var options = {
			series: [{
				name: 'Revenue',
				type: 'area',
				data: [44, 55, 31, 47, 31, 43, 26, 41, 31, 47, 33, 49]
			}, {
				name: 'Profit',
				type: 'line',
				data: [55, 69, 45, 61, 43, 54, 37, 52, 44, 61, 43, 74]
			}],
			colors: [myVarVal, "#9258f1"],
			chart: {
				height: 375,
				type: 'line',
			},
			stroke: {
				width: [3, 3],
				curve: "smooth",
				dashArray: [0, 2],
			},
			fill: {
				type: 'solid',
				opacity: [0.35, 1],
			},
			legend: {
				show: true,
				position: "top",
				horizontalAlign: "center",
				fontFamily: "Poppins",
				fontSize: "14px",
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
				itemMargin: {
					horizontal: 10
				}
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
			labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep ', 'Oct', 'Nov', 'Dec'],
			markers: {
				size: 0
			},
			grid: {
				borderColor: "rgba(119, 119, 142, 0.1)",
			},
			xaxis: {
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
				shared: true,
				intersect: false,
				y: {
					formatter: function (y) {
						if (typeof y !== "undefined") {
							return y.toFixed(0) + " points";
						}
						return y;
					}
				}
			}
		};

		document.getElementById("revenueStatistics").innerHTML = "";
		var chart = new ApexCharts(document.querySelector("#revenueStatistics"), options);
		chart.render();
	}, 300);

}

/*Bar Chart*/

/*Customer Retention*/

var options = {
	series: [44, 55, 41],
	labels: ["Existing Customers", "New Customers", "Visiting Customers"],
	chart: {
		type: 'donut',
		height: 330,
	},
	dataLabels: {
		enabled: true,
		dropShadow: {
			enabled: false,
		}
	},
	legend: {
		show: true,
		position: "bottom",
		horizontalAlign: "center",
		fontFamily: "Poppins",
		fontSize: "12px",
		offsetX: -10,
		labels: {
			colors: "#74767c",
		},
	},
	responsive: [{
		breakpoint: 480,
		options: {
			chart: {
				width: 200
			},
			legend: {
				position: 'bottom'
			}
		}
	}]
};

var chart = new ApexCharts(document.querySelector("#customerRetention"), options);
chart.render();

/*Customer Retention*/
