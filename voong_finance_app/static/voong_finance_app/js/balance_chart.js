console.log("balance-chart.js");

var balance_chart = {

    BalanceChart: function (div_id, data){
	console.log('call BalanceChart');
	console.log('data:');
	console.log(data);
	
	var that = this;
	this.div_id = div_id;
	this.data = data;
	this.margin = {top: 20, right: 20, bottom: 70, left: 40};
	this.width = 600 - this.margin.left - this.margin.right;
	this.height = 300 - this.margin.top - this.margin.bottom;
	this.x = d3.scaleOrdinal()//.range([0, this.width]); // should be an array of the somethings
	this.y = d3.scaleLinear().range([this.height, 0]);

	this.svg = d3.select('#' + this.div_id)
	    .append('svg')
	    .attr('width', this.width + this.margin.left + this.margin.right)
	    .attr('height', this.height + this.margin.top + this.margin.bottom)
	    .append('g')
	    .attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')');

	var columns = data.columns;
	var values = data.values;
	var date_index = columns.indexOf('date');
	var balance_index = columns.indexOf('balance');
	
	this.x.domain([0, values.length]); // .map(function(d) { return d[date_index]; }));
	this.y.domain([0, d3.max(values, function(d) { return d[balance_index]; })]);
	
	this.svg.selectAll(".bar")
	    .data(vals)
	    .enter().append("rect")
	    .attr("class", "bar")
	    .attr("x", function(d) { return that.x(d[date_index]); })
	    .attr("width", this.x.bandwidth())
	    .attr("y", function(d) { return that.y(d[balance_chart]); })
	    .attr("height", function(d) { return that.height - that.y(d[balance_index]); });

    },

    div_id: 'balance-chart',

    pad_dates: function(data, start, end){
	var first_date = new Date(data.values[0][0]);
	var last_date = new Date(data.values[data.values.length-1][0])
	var balance = 0;
	var padded_data = {
	    columns: data.columns,
	    values: []
	};

	for(var i=0; i<=(end - start) / (3600000 * 24); i++){
	    var date = new Date(start);
	    date.setDate(date.getDate() + i);
	    var date_string = date.toISOString().split('T')[0];

	    if(date >= first_date && date <= last_date){
		balance = balance_chart.get_balance(date_string);
	    }
	    padded_data.values.push([date_string, balance]);
	}
	return padded_data;
    },

    get_balance: function(date, data){
    }
    
};

// function createBalanceChart(data){
//     console.log("createBalanceChart");
//     // var balanceChart = new BalanceChart();
//     // balanceChart.create(data);
// };

// vf.createBalanceChart = createBalanceChart;

// function BalanceChart(){
//     var that = this;
//     this.margin = {top: 20, right: 20, bottom: 70, left: 40}
//     this.width = 600 - this.margin.left - this.margin.right,
//     this.height = 300 - this.margin.top - this.margin.bottom;
//     this.x = d3.scaleBand().range([0, this.width]).padding(0.01);
//     this.y = d3.scaleLinear().range([this.height, 0]);
    
//     this.create = function(data){
// 	console.log("BalanceChart.create")
// 	var svg = d3.select('#' + vf.balanceChartId)
// 	    .append("svg")
// 	    .attr("width", this.width + this.margin.left + this.margin.right)
// 	    .attr("height", this.height + this.margin.top + this.margin.bottom)
// 	    .append("g")
// 	    .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

// 	var cols = data.cols;
// 	var vals = data.vals;

// 	colToIndex = {}
// 	for(var i=0; i<cols.length; i++){
// 	    colToIndex[cols[i]] = i;
// 	}

// 	var dateIndex = colToIndex['date'];
// 	var balanceIndex = colToIndex['balance'];
// 	for(var i=0; i<vals.length; i++){
// 	    // vals[i][dateIndex] = d3.isoParse(vals[i][dateIndex]);
// 	    vals[i][dateIndex] = vals[i][dateIndex];
// 	    vals[i][balanceIndex] = +vals[i][balanceIndex];
// 	}

// 	console.log(vals);
// 	// this.x.domain(d3.extent(vals, function(d) { return d[dateIndex]; }));
// 	this.x.domain(vals.map(function(d) { return d[dateIndex]; }));
// 	this.y.domain([0, d3.max(vals, function(d) { return d[balanceIndex]; })]);

// 	console.log(this.x);
// 	console.log(this.y(10.8));
	
// 	svg.selectAll(".bar")
// 	    .data(vals)
// 	    .enter().append("rect")
// 	    .attr("class", "bar")
// 	    .attr("x", function(d) { return that.x(d[dateIndex]); })
// 	    .attr("width", this.x.bandwidth())
// 	    .attr("y", function(d) { return that.y(d[balanceIndex]); })
// 	    .attr("height", function(d) { return that.height - that.y(d[balanceIndex]); });

// 	// add the x Axis
// 	svg.append("g")
// 	    .attr("transform", "translate(0," + this.height + ")")
// 	    .call(d3.axisBottom(this.x));

// 	// add the y Axis
// 	svg.append("g")
// 	    .call(d3.axisLeft(this.y));
	
// 	console.log("width: " + this.width);
// 	console.log("x.bandwidth: " + this.x.bandwidth());
// 	console.log(vals[0][0]);
// 	console.log(vals[1][0]);
// 	console.log(vals[2][0]);
// 	console.log(this.x(vals[0][0]));
// 	console.log(this.x(vals[1][0]));
// 	console.log(this.x(vals[2][0]));
//     }

// };

// function createBalanceChart(data){
//     console.log("createBalanceChart");
//     var balanceChart = new BalanceChart();
//     balanceChart.create(data);
// };

// vf.createBalanceChart = createBalanceChart;
