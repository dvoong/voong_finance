QUnit.module('Test FirstTransactionPrompt', {
    beforeEach: function(){
	this.xhr = sinon.useFakeXMLHttpRequest();
	this.requests = [];
	this.xhr.onCreate = function(request) { this.requests.push(request); };
	this.server = sinon.fakeServer.create();
    },

    afterEach: function(){
	this.xhr.restore();
    }

})

QUnit.test('creates a first-transaction div and appends to the body', function(assert){
    var body = {append: function(){}};
    var div = {attr: function(){}};
    var select = sinon.stub(d3, 'select').returns(body);
    var append = sinon.stub(body, 'append').returns(div);
    var attr = sinon.stub(div, 'attr');

    first_transaction = new transactions.FirstTransactionPrompt();

    assert.deepEqual(select.firstCall.args, ['body']);
    assert.deepEqual(append.firstCall.args, ['div']);
    assert.deepEqual(attr.firstCall.args, ['id', 'first-entry-prompt']);

    select.restore();
});

QUnit.test('makes ajax call to /api/transaction-form and adds the html to the div', function(assert){
    var get = sinon.stub(jQuery, 'get');

    first_transaction = new transactions.FirstTransactionPrompt();
    
    assert.deepEqual(get.firstCall.args,
		     ['/api/transaction-form',
		      transactions.FirstTransactionPrompt.prototype.append_form]
		    );

    get.restore();
});

QUnit.test('append_form tests', function(assert){
    var first_transaction_div = {append: sinon.stub()};
    var select = sinon.stub(d3, 'select').returns(first_transaction_div);
    var html_response = 'some html';

    transactions.append_form(html_response);

    assert.equal(select.firstCall.args, 'first-entry-prompt');
    assert.deepEqual(first_transaction_div.append.firstCall.args, [html_response])

    select.restore();
});

// QUnit.module("createBalanceChart tests", {
//     beforeEach: function(){
// 	this.div_id = 'balance-chart';
// 	this.data = {
// 	    columns: ['date', 'balance'],
// 	    values: [['2017-01-01', 10], ['2017-01-02', 11]]
// 	};
//     },
//     afterEach: function(){}
// });

// QUnit.test('Pad dates', function(assert){

//     var data = this.data;
//     var start = new Date(2016, 11, 31);
//     var end = new Date(2017, 0, 4);
//     var get_balance = sinon.stub(balance_chart, 'get_balance');
//     get_balance.onCall(0).returns(10);
//     get_balance.onCall(1).returns(11);
    
//     padded_data = balance_chart.pad_dates(data, start, end);

//     expected = {
// 	columns: ['date', 'balance'],
// 	values: [
// 	    ['2016-12-31', 0],
// 	    ['2017-01-01', 10],
// 	    ['2017-01-02', 11],
// 	    ['2017-01-03', 11],
// 	    ['2017-01-04', 11]
// 	]
//     }
    
//     assert.deepEqual(padded_data, expected)
//     get_balance.restore();
    
// });

// QUnit.test('Get dates', function(assert){
//     var dates = balance_chart.dates(this.data);
//     var expected = [new Date('2017-01-01'), new Date('2017-01-02')]
//     assert.deepEqual(dates, expected);
// });

// QUnit.test('Chart initialisation creates a canvas', function(assert){
//     var spy = sinon.spy(balance_chart, 'Canvas');
//     var chart = new balance_chart.BalanceChart(this.data, this.div_id);
//     assert.equal(true, spy.calledOnce);
//     assert.equal(true, spy.calledWith(this.div_id, height=chart.height, width=chart.width, margin=chart.margin), spy.getCall(0));
//     spy.restore();
// });

// QUnit.test('Chart default parameters', function(assert){
//     var chart = new balance_chart.BalanceChart(this.data);
//     assert.equal(chart.div_id, 'balance-chart');
//     assert.equal(chart.height, 300);
//     assert.equal(chart.width, 1200);
//     assert.deepEqual(chart.margin, {top: 20, right: 20, bottom: 70, left: 40});
// });

// QUnit.test('Chart initialisation creates axes', function(assert){
//     var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'create_axes');
//     var chart = new balance_chart.BalanceChart(this.data, this.div_id);
//     assert.equal(true, spy.calledOnce);
//     assert.equal(true, spy.calledWith(chart.canvas));
//     spy.restore();
// });

// QUnit.test('Chart configures axis range', function(assert){
//     var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'configure_axes');
//     var chart = new balance_chart.BalanceChart(this.data, this.div_id);
//     assert.equal(true, spy.calledOnce);
//     assert.equal(true, spy.calledWith(chart.axes, chart.width, chart.height, chart.margin, chart.data));
//     spy.restore();
// });

// QUnit.test('Chart draws axis', function(assert){
//     var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'draw_axes');
//     var chart = new balance_chart.BalanceChart(this.data, this.div_id);
//     assert.equal(true, spy.calledOnce);
//     assert.equal(true, spy.calledWith(chart.axes, chart.canvas));
//     spy.restore();
// });

// QUnit.test('Chart plots the data', function(assert){
//     var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'plot_data');
//     var chart = new balance_chart.BalanceChart(this.data, this.div_id);
//     assert.equal(true, spy.calledOnce);
//     assert.equal(true, spy.calledWith(chart.data, chart.canvas));
//     spy.restore();
// });

// QUnit.test('Label chart', function(assert){
//     var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'label_chart');
//     var chart = new balance_chart.BalanceChart(this.data, this.div_id);
//     assert.equal(true, spy.calledOnce);
//     assert.equal(true, spy.calledWith());
//     spy.restore();
// });

// QUnit.module('Canvas tests', {
// });

// QUnit.test('Canvas creates an svg with appropriate arguments', function(assert){
//     var div_id = 'balance-chart'
//     var height = 1;
//     var width = 2;
//     var margin = {top: 1, right: 2, bottom: 3, left: 4};
//     var spy = sinon.spy(balance_chart, 'Canvas');
//     var canvas = new balance_chart.Canvas(div_id, height, width, margin);
//     assert.equal(canvas.svg.attr('height'), height);
//     assert.equal(canvas.svg.attr('width'), width);
//     assert.equal(canvas.svg.attr('margin'), margin);
//     spy.restore();
// });

// QUnit.module('create_axes tests', {
//     beforeEach: function(){
// 	this.div_id = 'balance-chart';
// 	this.height = 1;
// 	this.width = 10;
// 	this.margin = {top: 1, right: 2, bottom: 3, left: 4};
// 	this.canvas = new balance_chart.Canvas(this.div_id, this.height, this.width, this.margin);
//     }
// });

// QUnit.test('returns an object with properties, xaxis and yaxis', function(assert){

//     var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas)

//     assert.ok(axes.xaxis !== undefined, 'xaxis not found')
//     assert.ok(axes.yaxis !== undefined, 'yaxis not found')
// });

// QUnit.test('xaxis is on the bottom and yaxis is on the left', function(assert){

//     var xaxis = d3.axisBottom(d3.scaleLinear());
//     var yaxis = d3.axisLeft(d3.scaleLinear());
    
//     var stub_x = sinon.stub(d3, 'axisBottom').returns(xaxis);
//     var stub_y = sinon.stub(d3, 'axisLeft').returns(yaxis);
	
//     var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas);

//     assert.ok(axes.xaxis.call == xaxis);
//     assert.ok(axes.yaxis.call == yaxis);

//     stub_x.restore();
//     stub_y.restore();

// });

// QUnit.test('xaxis scale is of type scaleBand', function(assert){
//     var scale = d3.scaleBand();
//     var axis_spy = sinon.spy(d3, 'axisBottom');
//     var scale_stub = sinon.stub(d3, 'scaleBand').returns(scale);
	
//     var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas);

//     assert.ok(axis_spy.calledWith(scale));

//     axis_spy.restore();
//     scale_stub.restore();
// });

// QUnit.test('yaxis is linear', function(assert){
//     var scale = d3.scaleLinear();
//     var axis_spy = sinon.spy(d3, 'axisLeft');
//     var scale_stub = sinon.stub(d3, 'scaleLinear').returns(scale);
	
//     var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas);

//     assert.ok(axis_spy.calledWith(scale));

//     axis_spy.restore();
//     scale_stub.restore();
// });

// QUnit.test('set range of x axis', function(assert){

//     var scale = d3.scaleBand();
//     var stub = sinon.stub(d3, 'scaleBand').returns(scale);
//     var range = sinon.spy(scale, 'rangeRound');
	
//     var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas);

//     assert.ok(range.calledOnce, true);
//     assert.ok(range.calledWith([this.canvas.margin.left, this.canvas.width - this.canvas.margin.right]),
// 	      range.firstCall
// 	     );

//     range.restore();
//     stub.restore();

// });

// QUnit.test('set range of y axis', function(assert){

//     var scale = d3.scaleLinear();
//     var stub = sinon.stub(d3, 'scaleLinear').returns(scale);
//     var range = sinon.spy(scale, 'range');
	
//     var axes = balance_chart.BalanceChart.prototype.create_axes(this.canvas);

//     assert.ok(range.calledOnce, true);
//     assert.ok(range.calledWith([this.canvas.height - this.canvas.margin.bottom,
// 				this.canvas.margin.top]),
// 	      range.firstCall
// 	     );

//     range.restore();
//     stub.restore();

// });

// QUnit.module('configure_axes tests', {
//     beforeEach: function(){
// 	var xscale = d3.scaleBand();
// 	var yscale = d3.scaleLinear();
// 	this.xaxis = d3.axisBottom(xscale);
// 	this.yaxis = d3.axisLeft(yscale);
// 	this.width = 1;
// 	this.height = 2;
// 	this.margin = {top: 1, right: 2, bottom: 3, left: 4};
// 	this.axes = {xaxis: new balance_chart.Axis(this.xaxis), yaxis: new balance_chart.Axis(this.yaxis)};
// 	this.data = {
// 	    columns: ['date', 'balance'],
// 	    values: [['2017-01-01', 10], ['2017-01-02', 11]]
// 	};
//     }
// });

// QUnit.test('set domain of the xaxis', function(assert){

//     var domain_spy = sinon.spy(this.xaxis.scale(), 'domain');
//     var shortened_dates = ['1 Jan', '2 Jan'];
//     var shorten_date_strings_stub = sinon.stub(balance_chart, 'shorten_date_strings').returns(shortened_dates);

//     balance_chart.BalanceChart.prototype.configure_axes(this.axes, this.width, this.height, this.margin, this.data);
    
//     assert.ok(domain_spy.calledOnce);
//     // assert.ok(domain_spy.calledWith(['2017-01-01', '2017-01-02']), domain_spy.firstCall);
//     assert.ok(domain_spy.calledWith(shortened_dates), 'call domain with shortened dates');

//     shorten_date_strings_stub.restore();
// });

// QUnit.test('set domain of the yaxis', function(assert){

//     var domain_spy = sinon.spy(this.yaxis.scale(), 'domain');

//     balance_chart.BalanceChart.prototype.configure_axes(this.axes, this.width, this.height, this.margin, this.data);
    
//     assert.ok(domain_spy.calledOnce);
//     assert.ok(domain_spy.calledWith([0, 11]), domain_spy.firstCall);
// });

// QUnit.module('draw_axes tests', {
//     beforeEach: function(){
// 	this.axes = {xaxis: {}, yaxis: {}};
// 	this.canvas = {};
//     }
// });

// QUnit.test('appends g elements for x and y axes', function(assert){
//     var canvas = new balance_chart.Canvas('balance-chart', 1, 2, {top: 1, right: 2, bottom: 3, left: 4});
//     var axes = balance_chart.BalanceChart.prototype.create_axes(canvas);
    
//     balance_chart.BalanceChart.prototype.draw_axes(axes, canvas);

//     assert.ok(canvas.svg.select('#xaxis').node() !== undefined);
//     assert.ok(canvas.svg.select('#yaxis').node() !== undefined);
// });

// QUnit.module('get_balance', {});

// QUnit.test('test get_balance', function(assert){
//     var date = '2017-01-24';
//     var data = {columns: ['date', 'balance'], values: [['2017-01-24', 10], ['2017-01-25', 22]]};
//     var balance = balance_chart.get_balance(date, data);

//     assert.equal(balance, 10);
// });

// QUnit.module('shorten_date_strings tests', {});

// QUnit.test('shortens an array of date strings', function(assert){
//     var input = ['2017-01-1', '2017-01-02'];
//     var expected = ['1 Jan', '2 Jan'];

//     var output = balance_chart.shorten_date_strings(input);
    
//     assert.deepEqual(output, expected);
// });

// QUnit.test('if input is a string then return just that shortened date string', function(assert){
//     var input = '2017-01-01';
//     var expected = '1 Jan';

//     var output = balance_chart.shorten_date_strings(input);

//     assert.equal(output, expected);
// });

// QUnit.module('label_chart tests', {});

// // QUnit.test('calls add title to the x-axis passing the title and the x-axis element', function(assert){

// //     var label_axis = sinon.spy(balance_chart, 'label_axis');
// //     var data = {columns: ['date', 'balance'], values: [['2017-01-01', 10], ['2017-01-02', 11]]};
// //     var div_id = 'balance-chart';

// //     var chart = new balance_chart.BalanceChart(data, div_id);

// //     assert.ok(label_axis.calledWith(chart.axes.xaxis.element, 'Date'));

// //     label_axis.restore();
// // });

// QUnit.module('label_axis tests', {});

// QUnit.test('something', function(assert){

//     var xaxis = d3.select('body').append('g');

//     balance_chart.label_axis(xaxis, 'Date');

//     console.log(xaxis);
//     assert.equal(xaxis.select('text').text(), 'Date');
    
// });
