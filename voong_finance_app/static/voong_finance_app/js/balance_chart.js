console.log("balance-chart.js");

var balance_chart = new function(){
    var that = this;
    
    this.BalanceChart = function (data, div_id){

	this.data = data;
	this.div_id = div_id !== undefined ? div_id : 'balance-chart';
	this.canvas = new balance_chart.Canvas(this.div_id,
					   this.height,
					   this.width,
					   this.margin);
	this.axes = this.create_axes(this.canvas);
	this.configure_axes(this.axes, this.width, this.height, this.margin, this.data);
	this.draw_axes(this.axes, this.canvas);
	this.plot_data();
	this.label_chart();

    };

    this.BalanceChart.prototype.create_axes = function(canvas){
	var scalex = d3.scaleBand().rangeRound([canvas.margin.left, canvas.width - canvas.margin.right]);
	var scaley = d3.scaleLinear().range([canvas.height - canvas.margin.bottom, canvas.margin.top]);
	var xaxis = d3.axisBottom(scalex);
	var yaxis = d3.axisLeft(scaley);
	return {xaxis: xaxis, yaxis: yaxis};
    };

    this.BalanceChart.prototype.configure_axes = function(axes, width, height, margin, data){
	var dates = data.values.map(function(d){return d[0]});
	axes.xaxis.scale().domain(dates);
	axes.yaxis.scale().domain([0, d3.max(data.values, function(d){return d[1]})]);
    };

    this.BalanceChart.prototype.draw_axes = function(axes, canvas){
	var g = canvas.svg.append('g');
	g.attr('id', 'xaxis').call(this.axes.xaxis).attr('transform', 'translate(0, ' + (this.canvas.height - this.canvas.margin.bottom) + ')')
    };

    this.BalanceChart.prototype.plot_data = function(){
	
	// var columns = data.columns;
	// var values = data.values;
	// var date_index = columns.indexOf('date');
	// var balance_index = columns.indexOf('balance');
	// this.svg.selectAll(".bar")
	//     .data(values)
	//     .enter().append("rect")
	//     .attr("class", "bar")
	//     .attr("x", function(d) { return that.x(d[date_index]); })
	//     .attr("width", this.x.bandwidth())
	//     .attr("y", function(d) { return that.y(d[balance_chart]); })
	//     .attr("height", function(d) { return that.height - that.y(d[balance_index]); });
    };

    this.BalanceChart.prototype.label_chart = function(){
    };

    this.div_id = 'balance-chart';
    this.BalanceChart.prototype.height = 300;
    this.BalanceChart.prototype.width = 600;
    this.BalanceChart.prototype.margin = {top: 20, right: 20, bottom: 70, left: 40};

    this.pad_dates = function(data, start, end){
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
    };

    this.get_balance = function(date, data){
    };

    this.dates = function(data){
	var dates = [];
	for(var i=0; i<data.values.length; i++){
	    var date_string = data.values[i][0];
	    dates.push(new Date(date_string));
	}
	return dates;
    };

    this.Canvas = function(div_id, height, width, margin) {
	this.div_id = div_id;
	this.height = height;
	this.width = width;
	this.margin = margin;
	this.svg = d3.select('#' + div_id).append('svg')
	    .attr('height', height)
	    .attr('width', width)
	    .attr('margin', margin);

	//console.log(bc.attr('cheese'));
	// console.log(this.svg.attr('width'));
	
	//console.log(d3.selectAll('svg').attr('width'));
	// console.log(this.svg.attr);
	// console.log(this.svg.attr('cheese', 10));
	
	// this.margin = {top: 20, right: 20, bottom: 70, left: 40};
	// this.width = 600 - this.margin.left - this.margin.right;
	// this.height = 300 - this.margin.top - this.margin.bottom;
	// this.svg = d3.select('#' + this.div_id)
	//     .append('svg')
	//     .attr('width', this.width + this.margin.left + this.margin.right)
	//     .attr('height', this.height + this.margin.top + this.margin.bottom)
	//     .append('g')
	//     .attr('transform', 'translate(' + this.margin.left + ',' + this.margin.top + ')');
    };
    
}

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
