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
    var chart = new balance_chart.BalanceChart(this.div_id, this.data);
    assert.equal(true, spy.calledOnce);
});

QUnit.test('Chart initialisation creates axes', function(assert){
    var spy = sinon.spy(balance_chart.BalanceChart.prototype, 'create_axes');
    var chart = new balance_chart.BalanceChart(this.div_id, this.data);
    assert.equal(true, spy.calledOnce);
    assert.equal(true, spy.calledWith(chart.canvas));
});

QUnit.test('Chart configures axis range', function(assert){
    assert.equal(true, false, 'todo');
});
