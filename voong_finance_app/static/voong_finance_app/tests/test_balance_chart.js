QUnit.module("createBalanceChart tests", {
    beforeEach: function(){
	this.div_id = 'balance-chart';
	this.data = {
	    columns: ['date', 'balance'],
	    values: [['2017-01-01', 10], ['2017-01-02', 11]]
	};
    },
    afterEach: function(){}
});

// Qunit.test('Pads 21 days ahead and 21 days behind', function(assert){
//     var balance_chart = new balance_chart.BalanceChart(this.div_id, this.data);
    
// });

QUnit.test('Pad dates', function(assert){

    var data = this.data;
    var start = new Date(2016, 11, 31);
    var end = new Date(2017, 0, 4);
    var get_balance = sinon.stub(balance_chart, 'get_balance');
    get_balance.onCall(0).returns(10);
    get_balance.onCall(1).returns(11);
    
    padded_data = balance_chart.pad_dates(data, start, end);

    expected = {
	columns: ['date', 'balance'],
	values: [
	    ['2016-12-31', 0],
	    ['2017-01-01', 10],
	    ['2017-01-02', 11],
	    ['2017-01-03', 11],
	    ['2017-01-04', 11]
	]
    }
    
    assert.deepEqual(padded_data, expected)
    
});

QUnit.test('Get dates', function(assert){
    var dates = balance_chart.dates(this.data);
    var expected = [new Date('2017-01-01'), new Date('2017-01-02')]
    assert.deepEqual(dates, expected);
});

QUnit.test('Chart initialisation creates a canvas', function(assert){
    var spy = sinon.spy(balance_chart, 'Canvas');
    var chart = new balance_chart.BalanceChart(this.data, this.div_id);
    assert.equal(true, spy.calledOnce);
    assert.equal(true, spy.calledWith(this.div_id, height=chart.height, width=chart.width, margin=chart.margin), spy.getCall(0));
    spy.restore();
});

QUnit.test('Chart default parameters', function(assert){
    var chart = new balance_chart.BalanceChart(this.data);
    assert.equal(chart.div_id, 'balance-chart');
    assert.equal(chart.height, 300);
    assert.equal(chart.width, 600);
    assert.deepEqual(chart.margin, {top: 20, right: 20, bottom: 70, left: 40});
});

QUnit.test('Chart initialisation creates axes', function(assert){
    var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'create_axes');
    var chart = new balance_chart.BalanceChart(this.data, this.div_id);
    assert.equal(true, spy.calledOnce);
    assert.equal(true, spy.calledWith(chart.canvas));
    spy.restore();
});

QUnit.test('Chart configures axis range', function(assert){
    var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'configure_axes');
    var chart = new balance_chart.BalanceChart(this.data, this.div_id);
    assert.equal(true, spy.calledOnce);
    assert.equal(true, spy.calledWith(chart.axes, chart.width, chart.height, chart.margin, chart.data));
    spy.restore();
});

QUnit.test('Chart draws axis', function(assert){
    var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'draw_axes');
    var chart = new balance_chart.BalanceChart(this.data, this.div_id);
    assert.equal(true, spy.calledOnce);
    assert.equal(true, spy.calledWith(chart.axes, chart.canvas));
    spy.restore();
});

QUnit.test('Chart plots the data', function(assert){
    var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'plot_data');
    var chart = new balance_chart.BalanceChart(this.data, this.div_id);
    assert.equal(true, spy.calledOnce);
    assert.equal(true, spy.calledWith());
    spy.restore();
});

QUnit.test('Label chart', function(assert){
    var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'label_chart');
    var chart = new balance_chart.BalanceChart(this.data, this.div_id);
    assert.equal(true, spy.calledOnce);
    assert.equal(true, spy.calledWith());
    spy.restore();
});

QUnit.module('Canvas tests', {
});

QUnit.test('Canvas creates an svg with appropriate arguments', function(assert){
    var div_id = 'balance-chart'
    var height = 1;
    var width = 2;
    var margin = {top: 1, right: 2, bottom: 3, left: 4};
    var spy = sinon.spy(balance_chart, 'Canvas');
    var canvas = new balance_chart.Canvas(div_id, height, width, margin);
    assert.equal(canvas.svg.attr('height'), height);
    assert.equal(canvas.svg.attr('width'), width);
    assert.equal(canvas.svg.attr('margin'), margin);
    spy.restore();
});

QUnit.module('create_axes tests', {
    beforeEach: function(){
	this.div_id = 'balance-chart';
	this.height = 1;
	this.width = 10;
	this.margin = {top: 1, right: 2, bottom: 3, left: 4};
	this.canvas = new balance_chart.Canvas(this.div_id, this.height, this.width, this.margin);
    }
});

QUnit.test('returns an object with properties, xaxis and yaxis', function(assert){

    var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas)

    assert.ok(axes.xaxis !== undefined, 'xaxis not found')
    assert.ok(axes.yaxis !== undefined, 'yaxis not found')
});

QUnit.test('xaxis is on the bottom and yaxis is on the left', function(assert){

    var xaxis = d3.axisBottom(d3.scaleLinear());
    var yaxis = d3.axisLeft(d3.scaleLinear());
    
    var stub_x = sinon.stub(d3, 'axisBottom').returns(xaxis);
    var stub_y = sinon.stub(d3, 'axisLeft').returns(yaxis);
	
    var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas);

    assert.ok(axes.xaxis == xaxis);
    assert.ok(axes.yaxis == yaxis);

    stub_x.restore();
    stub_y.restore();

});

QUnit.test('xaxis scale is of type scaleBand', function(assert){
    var scale = d3.scaleBand();
    var axis_spy = sinon.spy(d3, 'axisBottom');
    var scale_stub = sinon.stub(d3, 'scaleBand').returns(scale);
	
    var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas);

    assert.ok(axis_spy.calledWith(scale));

    axis_spy.restore();
    scale_stub.restore();
});

QUnit.test('yaxis is linear', function(assert){
    var scale = d3.scaleLinear();
    var axis_spy = sinon.spy(d3, 'axisLeft');
    var scale_stub = sinon.stub(d3, 'scaleLinear').returns(scale);
	
    var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas);

    assert.ok(axis_spy.calledWith(scale));

    axis_spy.restore();
    scale_stub.restore();
});

QUnit.test('set range of x axis', function(assert){

    var scale = d3.scaleBand();
    var stub = sinon.stub(d3, 'scaleBand').returns(scale);
    var range = sinon.spy(scale, 'rangeRound');
	
    var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas);

    assert.ok(range.calledOnce, true);
    assert.ok(range.calledWith([this.canvas.margin.left, this.canvas.width - this.canvas.margin.right]),
	      range.firstCall
	     );

    range.restore();
    stub.restore();

});

QUnit.test('set range of y axis', function(assert){

    var scale = d3.scaleLinear();
    var stub = sinon.stub(d3, 'scaleLinear').returns(scale);
    var range = sinon.spy(scale, 'range');
	
    var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas);

    assert.ok(range.calledOnce, true);
    assert.ok(range.calledWith([this.canvas.height - this.canvas.margin.bottom,
				this.canvas.margin.top]),
	      range.firstCall
	     );

    range.restore();
    stub.restore();

});

QUnit.module('configure_axes tests', {
    beforeEach: function(){
	var xscale = d3.scaleBand();
	var yscale = d3.scaleLinear();
	this.xaxis = d3.axisBottom(xscale);
	this.yaxis = d3.axisLeft(yscale);
	this.width = 1;
	this.height = 2;
	this.margin = {top: 1, right: 2, bottom: 3, left: 4};
	this.axes = {xaxis: this.xaxis, yaxis: this.yaxis};
	this.data = {
	    columns: ['date', 'balance'],
	    values: [['2017-01-01', 10], ['2017-01-02', 11]]
	};
    }
});

QUnit.test('set domain of the xaxis', function(assert){

    var domain_spy = sinon.spy(this.xaxis.scale(), 'domain');

    balance_chart.BalanceChart.prototype.configure_axes(this.axes, this.width, this.height, this.margin, this.data);
    
    assert.ok(domain_spy.calledOnce);
    assert.ok(domain_spy.calledWith(['2017-01-01', '2017-01-02']), domain_spy.firstCall);
});

QUnit.test('set domain of the yaxis', function(assert){

    var domain_spy = sinon.spy(this.yaxis.scale(), 'domain');

    balance_chart.BalanceChart.prototype.configure_axes(this.axes, this.width, this.height, this.margin, this.data);
    
    assert.ok(domain_spy.calledOnce);
    assert.ok(domain_spy.calledWith([0, 11]), domain_spy.firstCall);
});

QUnit.module('draw_axes tests', {
    beforeEach: function(){
	this.axes = {xaxis: {}, yaxis: {}};
	this.canvas = {};
    }
});

QUnit.test('', function(assert){
    assert.ok(false, 'todo');
    
});
