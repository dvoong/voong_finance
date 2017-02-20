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
    var start = new Date(2016, 12, 31);
    var end = new Date(2017, 1, 4);

    console.log(data);
    
    padded_data = balance_chart.pad_dates(data, start, end);

    expected = {
	columns: ['date', 'balance'],
	values: [
	    ('2016-12-31', 0),
	    ('2017-01-01', 10),
	    ('2017-01-02', 11),
	    ('2017-01-03', 11),
	    ('2017-01-04', 11)
	]
    }
    
    assert.equal(padded_data, expected)
    
});

QUnit.test('Get dates', function(assert){
    var dates = balance_chart.dates(this.data);
    var expected = [new Date('2017-01-01'), new Date('2017-01-02')]
    assert.equal(dates, expected);
});
