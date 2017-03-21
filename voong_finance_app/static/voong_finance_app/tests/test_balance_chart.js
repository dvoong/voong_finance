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
    assert.equal(chart.width, 1200);
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
    assert.equal(true, spy.calledWith(chart.data, chart.canvas));
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

    assert.ok(axes.xaxis.call == xaxis);
    assert.ok(axes.yaxis.call == yaxis);

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
	this.axes = {xaxis: new balance_chart.Axis(this.xaxis), yaxis: new balance_chart.Axis(this.yaxis)};
	this.data = {
	    columns: ['date', 'balance'],
	    values: [['2017-01-01', 10], ['2017-01-02', 11]]
	};
    }
});

QUnit.test('set domain of the xaxis', function(assert){

    var domain_spy = sinon.spy(this.xaxis.scale(), 'domain');
    var shortened_dates = ['1 Jan', '2 Jan'];
    var shorten_date_strings_stub = sinon.stub(balance_chart, 'shorten_date_strings').returns(shortened_dates);

    balance_chart.BalanceChart.prototype.configure_axes(this.axes, this.width, this.height, this.margin, this.data);
    
    assert.ok(domain_spy.calledOnce);
    // assert.ok(domain_spy.calledWith(['2017-01-01', '2017-01-02']), domain_spy.firstCall);
    assert.ok(domain_spy.calledWith(shortened_dates), 'call domain with shortened dates');

    shorten_date_strings_stub.restore();
});

QUnit.test('set domain of the yaxis', function(assert){

    var domain_spy = sinon.spy(this.yaxis.scale(), 'domain');

    balance_chart.BalanceChart.prototype.configure_axes(this.axes, this.width, this.height, this.margin, this.data);
    
    assert.ok(domain_spy.calledOnce);
    assert.ok(domain_spy.calledWith([0, 11]), domain_spy.firstCall);
});

QUnit.test('negative balances', function(assert){

    var domain_spy = sinon.spy(this.yaxis.scale(), 'domain');

    this.data.values[0][1] = -10;

    balance_chart.BalanceChart.prototype.configure_axes(this.axes, this.width, this.height, this.margin, this.data);
    
    assert.ok(domain_spy.calledOnce);
    assert.ok(domain_spy.calledWith([-10, 11]), domain_spy.firstCall);
});

QUnit.module('draw_axes tests', {
    beforeEach: function(){
	this.axes = {xaxis: {}, yaxis: {}};
	this.canvas = {};
    }
});

QUnit.test('appends g elements for x and y axes', function(assert){
    var canvas = new balance_chart.Canvas('balance-chart', 1, 2, {top: 1, right: 2, bottom: 3, left: 4});
    var axes = balance_chart.BalanceChart.prototype.create_axes(canvas);
    
    balance_chart.BalanceChart.prototype.draw_axes(axes, canvas);

    assert.ok(canvas.svg.select('#xaxis').node() !== undefined);
    assert.ok(canvas.svg.select('#yaxis').node() !== undefined);
});

QUnit.module('get_balance', {});

QUnit.test('test get_balance', function(assert){
    var data = [['2017-01-24', 10], ['2017-01-25', 22]]
    var balance = balance_chart.get_balance(data[0]);

    assert.equal(balance, 10);
});

QUnit.module('shorten_date_strings tests', {});

QUnit.test('shortens an array of date strings', function(assert){
    var input = ['2017-01-1', '2017-01-02'];
    var expected = ['1 Jan', '2 Jan'];

    var output = balance_chart.shorten_date_strings(input);
    
    assert.deepEqual(output, expected);
});

QUnit.test('if input is a string then return just that shortened date string', function(assert){
    var input = '2017-01-01';
    var expected = '1 Jan';

    var output = balance_chart.shorten_date_strings(input);

    assert.equal(output, expected);
});

QUnit.module('label_chart tests', {});

// QUnit.test('calls add title to the x-axis passing the title and the x-axis element', function(assert){

//     var label_axis = sinon.spy(balance_chart, 'label_axis');
//     var data = {columns: ['date', 'balance'], values: [['2017-01-01', 10], ['2017-01-02', 11]]};
//     var div_id = 'balance-chart';

//     var chart = new balance_chart.BalanceChart(data, div_id);

//     assert.ok(label_axis.calledWith(chart.axes.xaxis.element, 'Date'));

//     label_axis.restore();
// });

QUnit.module('label_axis tests', {});

QUnit.test('something', function(assert){

    var xaxis = d3.select('body').append('g');

    balance_chart.label_axis(xaxis, 'Date');

    assert.equal(xaxis.select('text').text(), 'Date');
    
});

QUnit.module('update_data', {
    beforeEach: function(){
	this.data = {'columns': ['date', 'balance'], 'values': [['2017-03-01', 10], ['2017-03-02', 20]]};
	this.bars = [];
	this.selectAll = sinon.stub(_chart.canvas.svg, 'selectAll').returns(this.bars);
	this.filtered_bars = {transition: function(){}, data: function(){}, attr: function(){}};
	this.filter_bars_by_date = sinon.stub(balance_chart, 'filter_bars_by_date').returns(this.filtered_bars);
	this.data_binder = sinon.stub(this.filtered_bars, 'data').returns(this.filtered_bars);
	this.transition = sinon.stub(this.filtered_bars, 'transition').returns(this.filtered_bars);
	this.attr = sinon.stub(this.filtered_bars, 'attr');
	this.attr.returns(this.filtered_bars);
	this.get_y = sinon.stub(balance_chart, 'get_y');
	this.get_height = sinon.stub(balance_chart, 'get_height');
	this.get_balance = sinon.stub(balance_chart, 'get_balance');
	this.dates = [];
	this.get_dates = sinon.stub(balance_chart, 'get_dates').returns(this.dates);
    },
    afterEach: function(){
	this.selectAll.restore();
	this.filter_bars_by_date.restore();
	this.transition.restore();
	this.get_y.restore();
	this.get_height.restore();
	this.get_balance.restore();
	this.get_dates.restore();
    }
});

// takes some data
// gets the bars from the balance_chart
// filters bars with matching dates to the response
// rebinds the data to the filtered bars
// creates a transition from the filtered bars
// set y attribute using the date from the response and the scale from the balance chart
// set the height attribute using the balance from the response and scale from the balance chart
// set the balance attribute of the bar

QUnit.test('gets bars from the balance_chart', function(assert){

    balance_chart.update_data(this.data);

    assert.deepEqual(this.selectAll.firstCall.args, ['.bar']);
});

QUnit.test('filters_bars_with_matching_dates_to_the_data', function(assert){

    balance_chart.update_data(this.data);

    assert.deepEqual(this.get_dates.firstCall.args, [this.data.values]);
    assert.deepEqual(this.filter_bars_by_date.firstCall.args, [this.bars, this.dates]);
});

QUnit.test('rebinds the data to the filtered bars', function(assert){

    balance_chart.update_data(this.data);

    assert.deepEqual(this.data_binder.firstCall.args, [this.data.values]);
});

QUnit.test('creates transition from filtered bars', function(assert){

    balance_chart.update_data(this.data);

    assert.deepEqual(this.transition.firstCall.args, []);
});

QUnit.test('set y attribute using the date from the response and the scale from the balance chart', function(assert){

    balance_chart.update_data(this.data);

    assert.deepEqual(this.attr.firstCall.args, ['y', this.get_y]);
});

QUnit.test('set the height attribute using the balance from the response and scale from the balance chart', function(assert){

    balance_chart.update_data(this.data);

    assert.deepEqual(this.attr.secondCall.args, ['height', this.get_height]);
});

QUnit.test('set the balance attribute of the bar', function(assert){

    balance_chart.update_data(this.data);

    assert.deepEqual(this.attr.thirdCall.args, ['balance', this.get_balance]);
    
});

QUnit.module('get_dates', {});

QUnit.test('get_dates', function(assert){
    dates = balance_chart.get_dates([['2017-03-02', 10], ['2017-03-03', 11]]);

    assert.deepEqual(dates, ['2017-03-02', '2017-03-03'])
});

QUnit.module('filter_bars_by_date', {
    beforeEach: function(){
	this.nodes = [{attr: function(date){return '2017-03-01'}},
		      {attr: function(date){return '2017-03-02'}},
		      {attr: function(date){return '2017-03-03'}},
		     ];
	this.bars = {
	    nodes: sinon.stub().returns(this.nodes)
	};
	this.dates = ['2017-03-02', '2017-03-03'];
	this.filtered_bars = [this.nodes[1], this.nodes2]
	this.selectAll = sinon.stub(d3, 'selectAll').returns(this.filtered_bars);
    },

    afterEach: function(){
	this.selectAll.restore();
    }

});

QUnit.test('', function(assert){

    var output = balance_chart.filter_bars_by_date(this.bars, this.dates);

    assert.deepEqual(output, this.filtered_bars);
});

QUnit.module('get_y', {
    beforeEach: function(){
	this.scale = sinon.stub();
	this.get_scale = sinon.stub(_chart.axes.yaxis.call, 'scale').returns(this.scale);
	this.balance = 10;
	this.get_balance = sinon.stub(balance_chart, 'get_balance').returns(this.balance);
	this.data = ['2017-03-01', this.balance]
    },
    afterEach: function(){
	this.get_scale.restore();
	this.get_balance.restore();
    }
});

// call the chart scale function on the balance
QUnit.test('', function(assert){
    
    balance_chart.get_y(this.data);

    assert.deepEqual(this.get_balance.firstCall.args, [this.data]);
    assert.deepEqual(this.get_scale.firstCall.args, []);
    assert.deepEqual(this.scale.firstCall.args, [this.balance]);
});

QUnit.module('get_height', {
    beforeEach: function(){
	_chart.height = 12;
	_chart.margin = {bottom: 2};
	this.balance = 10;
	this.data = ['2017-03-01', this.balance]
	this.scaled_balance = 3
	
	this.scale = sinon.stub().returns(this.scaled_balance);
	this.get_scale = sinon.stub(_chart.axes.yaxis.call, 'scale').returns(this.scale);
	this.get_balance = sinon.stub(balance_chart, 'get_balance').returns(this.balance);
    },
    afterEach: function(){
	this.get_scale.restore();
	this.get_balance.restore();
    }
});

QUnit.test('', function(assert){

    var height = balance_chart.get_height(this.data);

    assert.deepEqual(this.get_balance.firstCall.args, [this.data]);
    assert.deepEqual(this.get_scale.firstCall.args, []);
    assert.deepEqual(this.scale.firstCall.args, [this.balance]);
    assert.equal(height, _chart.height - _chart.margin.bottom - this.scaled_balance);
    
});

function stub(object, func, stubs){
    var stub = sinon.stub(object, func);
    stubs.push(stub);
    return stub;
}

function restore_stubs(stubs){
    for(var i=0; i<stubs.length; i++){
	stubs[i].restore();
    }
}

QUnit.module('get_balances', {
    beforeEach: function(){
	this.stubs = [];
	this.get = stub($, 'get', this.stubs);
    },
    afterEach: function(){
	restore_stubs(this.stubs);
    }
});
// makes ajax request to /api/get-balances
// on success: call the callback with the response data
QUnit.test('', function(assert){

    balance_chart.get_balances(this.callback);

    assert.deepEqual(this.get.firstCall.args, ['/api/get-balances', this.callback]);
});
