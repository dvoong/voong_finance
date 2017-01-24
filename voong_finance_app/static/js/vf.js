console.log('vf.js');

var vf = {};

function BalanceChart(){
    var that = this;
    this.margin = {top: 20, right: 20, bottom: 70, left: 40}
    this.width = 600 - this.margin.left - this.margin.right,
    this.height = 300 - this.margin.top - this.margin.bottom;
    this.x = d3.scaleBand().range([0, this.width]).padding(0.01);
    this.y = d3.scaleLinear().range([this.height, 0]);
    
    this.create = function(data){
	console.log("BalanceChart.create")
	var svg = d3.select('#' + vf.balanceChartId)
	    .append("svg")
	    .attr("width", this.width + this.margin.left + this.margin.right)
	    .attr("height", this.height + this.margin.top + this.margin.bottom)
	    .append("g")
	    .attr("transform", "translate(" + this.margin.left + "," + this.margin.top + ")");

	var cols = data.cols;
	var vals = data.vals;

	colToIndex = {}
	for(var i=0; i<cols.length; i++){
	    colToIndex[cols[i]] = i;
	}

	var dateIndex = colToIndex['date'];
	var balanceIndex = colToIndex['balance'];
	for(var i=0; i<vals.length; i++){
	    // vals[i][dateIndex] = d3.isoParse(vals[i][dateIndex]);
	    vals[i][dateIndex] = vals[i][dateIndex];
	    vals[i][balanceIndex] = +vals[i][balanceIndex];
	}

	console.log(vals);
	// this.x.domain(d3.extent(vals, function(d) { return d[dateIndex]; }));
	this.x.domain(vals.map(function(d) { return d[dateIndex]; }));
	this.y.domain([0, d3.max(vals, function(d) { return d[balanceIndex]; })]);

	console.log(this.x);
	console.log(this.y(10.8));
	
	svg.selectAll(".bar")
	    .data(vals)
	    .enter().append("rect")
	    .attr("class", "bar")
	    .attr("x", function(d) { return that.x(d[dateIndex]); })
	    .attr("width", this.x.bandwidth())
	    .attr("y", function(d) { return that.y(d[balanceIndex]); })
	    .attr("height", function(d) { return that.height - that.y(d[balanceIndex]); });

	// add the x Axis
	svg.append("g")
	    .attr("transform", "translate(0," + this.height + ")")
	    .call(d3.axisBottom(this.x));

	// add the y Axis
	svg.append("g")
	    .call(d3.axisLeft(this.y));
	
	console.log("width: " + this.width);
	console.log("x.bandwidth: " + this.x.bandwidth());
	console.log(vals[0][0]);
	console.log(vals[1][0]);
	console.log(vals[2][0]);
	console.log(this.x(vals[0][0]));
	console.log(this.x(vals[1][0]));
	console.log(this.x(vals[2][0]));
    }

};

function createBalanceChart(data){
    console.log("createBalanceChart");
    var balanceChart = new BalanceChart();
    balanceChart.create(data);
};

vf.createBalanceChart = createBalanceChart;
