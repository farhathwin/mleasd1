
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

	/*Customer Acquisition*/

	/*Earning Details*/

	var chartdata = [
		{
			name: 'Sales',
			type: 'bar',
			data: [10, 15, 9, 18, 10, 15, 18, 12, 15, 20, 18, 23]
		},
		{
			name: 'Profit',
			type: 'line',
			smooth: true,
			data: [8, 5, 25, 10, 7, 12, 15, 10, 2, 13, 11, 15, 25]
		},
		{
			name: 'Growth',
			type: 'bar',
			data: [10, 14, 10, 15, 9, 25, 16, 20, 14, 13, 22, 11]
		}
	];

	var chart = document.getElementById('earning-details');
	var barChart = echarts.init(chart);

	var option = {
		grid: {
			top: '6',
			right: '0',
			bottom: '17',
			left: '25',
		},
		xAxis: {
			data: ['Jan', 'Feb', 'Mar', 'Apr', 'May', "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
			axisLine: {
				lineStyle: {
					color: 'rgba(0,0,0,0.03)'
				}
			},
			axisLabel: {
				fontSize: 10,
				color: '#bbc1ca'
			}
		},
		tooltip: {
			show: true,
			showContent: true,
			alwaysShowContent: true,
			triggerOn: 'mousemove',
			trigger: 'axis',
			axisPointer:
			{
				label: {
					show: false,
				}
			}

		},
		yAxis: {
			splitLine: {
				lineStyle: {
					color: 'rgba(0,0,0,0.03)'
				}
			},
			axisLine: {
				lineStyle: {
					color: 'rgba(0,0,0,0.03)'
				}
			},
			axisLabel: {
				fontSize: 10,
				color: '#bbc1ca'
			}
		},
		series: chartdata,
		color: [myVarVal, '#fa626b', '#9258f1']
	};

	barChart.setOption(option);

	/*Earning Details*/

	new Morris.Donut({
		element: 'morrisBar9',
		data: [
			{ value: 57, label: 'Current' },
			{ value: 22, label: 'New' },
			{ value: 21, label: 'Retargeted' },
		],
		backgroundColor: '#fff',
		labelColor: '#212529',
		colors: [
			'#1753fc ', '#9258f1', '#fdb901'
		],
		formatter: function (x) { return x + "%" }
	});

	/*Customer Acquisition*/

});

/*Data Table*/