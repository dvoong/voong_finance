console.log("balance-chart.js");

var balance_chart = new function(){
    var that = this;

    this.div_id = 'balance-chart'
    
    this.BalanceChart = function (data, div_id, width, height, margin){
	this.div_id = div_id !== undefined ? div_id : that.div_id;
	this.height = height !== undefined ? height: 300 ;
	this.width = width !== undefined ? width : 1200;
	this.margin = margin !== undefined ? margin : {top: 20, right: 20, bottom: 70, left: 40};

	this.data = data;
	this.div_id = div_id !== undefined ? div_id : 'balance-chart';
	this.canvas = new balance_chart.Canvas(this.div_id,
					   this.height,
					   this.width,
					   this.margin);
	this.axes = this.create_axes(this.canvas);
	this.configure_axes(this.axes, this.width, this.height, this.margin, this.data);
	this.draw_axes(this.axes, this.canvas);
	this.plot_data(this.data, this.canvas);
	this.label_chart();

    };

    this.BalanceChart.prototype.create_axes = function(canvas){
	var scalex = d3.scaleBand()
	    .rangeRound([canvas.margin.left, canvas.width - canvas.margin.right])
	    .padding(0.05);
	var scaley = d3.scaleLinear().range([canvas.height - canvas.margin.bottom, canvas.margin.top]);
	var xaxis = d3.axisBottom(scalex);
	var yaxis = d3.axisLeft(scaley);
	return {xaxis: new balance_chart.Axis(xaxis), yaxis: new balance_chart.Axis(yaxis)};
	// return {xaxis: xaxis, yaxis: yaxis};
    };

    this.BalanceChart.prototype.configure_axes = function(axes, width, height, margin, data){
	var dates = data.values.map(function(d){return d[0]});
	var dates = balance_chart.shorten_date_strings(dates);
	axes.xaxis.call.scale().domain(dates);
	var ymax = d3.max(data.values, function(d){return d[1]});
	var ymin = d3.min(data.values, function(d){return d[1]});
	axes.yaxis.call.scale().domain([Math.min(0, ymin), ymax]);
    };

    this.BalanceChart.prototype.draw_axes = function(axes, canvas){
	var g = canvas.svg.append('g')
	    .attr('id', 'x-axis')
	    .call(axes.xaxis.call)
	    .attr('transform', 'translate(0, ' + (canvas.height - canvas.margin.bottom) + ')');
	axes.xaxis.element = g;

	var g = canvas.svg.append('g')
	    .attr('id', 'y-axis')
	    .call(axes.yaxis.call)
	    .attr('transform', 'translate(' + canvas.margin.left + ', 0)');
	axes.yaxis.element = g;

	return axes;
    };

    this.BalanceChart.prototype.plot_data = function(data, canvas){

	var that = this;
	var bar_width = this.axes.xaxis.call.scale().bandwidth();
	canvas.svg.selectAll('.bar')
	    .data(data.values)
	    .enter().append('rect')
	    .attr('class', 'bar')
	    .attr('balance', function(d){return d[1]})
	    .attr('date', function(d){return d[0]})
	    .attr('x', function(d){
		return that.axes.xaxis.call.scale()(
		    balance_chart.shorten_date_strings(d[0])
		);
	    })
	    .attr('width', bar_width)
	    .attr('y', function(d){return that.axes.yaxis.call.scale()(d[1]);})
	    .attr('height', function(d){return canvas.height - canvas.margin.bottom - that.axes.yaxis.call.scale()(d[1])});
    };

    this.BalanceChart.prototype.label_chart = function(){
	//balance_chart.label_axis(this.axes.xaxis.element, 'Date', this.canvas.width / 2, this.canvas.margin.bottom / 2);
	
    };

    this.get_balance = function(d){
	return d[1];
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
    };

    this.shorten_date_strings = function(dates){
	if(Array.isArray(dates)){
	    var dates = dates.map(this.shorten_date_strings);
	    return dates;
	} else {
	    var date = new Date(dates);
	    date_string = date.getDate() + ' ' + date.toLocaleString('en-GB', { month: "short" })
	    return date_string;
	}
    };

    this.label_axis = function(axis, label, x, y){
	axis.append('g')
	    .append("text")
	    .attr("text-anchor", "middle")
            .attr("transform", "translate(" + x + ", " + y + ")")
	    .text("Date")
	    .attr('fill', '#000');
    }

    this.Axis = function(call){
	this.call = call;
    };

    this.update_data = function(data){
	var bars = _chart.canvas.svg.selectAll('.bar');
	var dates = balance_chart.get_dates(data.values);
	var filtered_bars = balance_chart.filter_bars_by_date(bars, dates);
	filtered_bars.data(data.values)
	    .transition()
	    .attr('y', balance_chart.get_y)
	    .attr('height', balance_chart.get_height)
	    .attr('balance', balance_chart.get_balance);
    };

    this.get_dates = function(values){
	output = [];
	for(var i=0; i<values.length; i++){
	    output.push(values[i][0]);
	}
	return output;
    };

    this.filter_bars_by_date = function(bars, dates){
	output = []
	nodes = bars.nodes();
	for(var i=0; i<dates.length; i++){
	    for(var j=0; j<nodes.length; j++){
		if($(nodes[j]).attr('date') == dates[i]){
		    output.push(nodes[j]);
		    break;
		}
	    }
	}
	return d3.selectAll(output);
    };

    this.get_y = function(d){
	var balance = balance_chart.get_balance(d);
	var scale = _chart.axes.yaxis.call.scale();
	return scale(balance);
    };

    this.get_height = function(d){
	var balance = balance_chart.get_balance(d);
	var scale = _chart.axes.yaxis.call.scale();
	var scaled_balance = scale(balance);
	return _chart.height - _chart.margin.bottom - scaled_balance;
    };

    this.get_balances = function(callback){
	$.get('/api/get-balances', callback);
    };

}
