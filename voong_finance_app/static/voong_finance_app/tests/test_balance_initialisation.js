QUnit.module("Balance Initialisation Tests", {
    beforeEach: function(){
	this.balance_initialisation = new balance_initialisation.BalanceInitialisation();
	this.xhr = sinon.useFakeXMLHttpRequest();
	this.requests = [];
	this.xhr.onCreate = function(request) { this.requests.push(request); };
	this.server = sinon.fakeServer.create();
	this.data = {date: '2017-01-24', balance: 4344.40};
	this.response_data = {columns: ['date', 'balance'], values: [['2017-01-24', 4344.40]]};
	this.BalanceChart = sinon.stub(balance_chart, 'BalanceChart')
    },
    afterEach: function(){
	this.xhr.restore();
	this.BalanceChart.restore();
    }
});

QUnit.test('Submission of the form makes an ajax call to the initialise_balance api', function(assert){
    var stub = sinon.stub(jQuery, 'post');
    var url = balance_initialisation.initialise_balance_url;
    var callback = balance_initialisation.success_callback;
    this.balance_initialisation.input.val(this.data.balance);
    this.balance_initialisation.date_input.val(this.data.date);
    this.balance_initialisation.submit.click();
    assert.ok(stub.calledOnce);
    assert.deepEqual(stub.firstCall.args, [url, this.data, callback]);
    stub.restore();
});

QUnit.test('Upon successful submission of the form hide/delete the balance_initialisation  div', function(assert){
    assert.ok($('#balance-initialisation').length == 1, "found balance-initialisation div");
    this.server.respondWith("POST",
    			    this.balance_initialisation.initialise_balance_url,
    			    [200, {'Content-Type': 'application/json'}, '{}']
    			   );
    this.balance_initialisation.input.val(4344.40);
    this.balance_initialisation.submit.click();
    this.server.respond();
    assert.ok($('#balance-initialisation').length == 0, "balance-initialisation removed from document");
});

QUnit.test('Upon successful submission of the form call create_balance_chart', function(assert){
    
    this.server.respondWith("POST",
    			    this.balance_initialisation.initialise_balance_url,
    			    [200, { "Content-Type": "application/json" }, JSON.stringify(this.response_data)]
    			   );
    this.balance_initialisation.submit.click();
    this.server.respond();
    assert.ok(this.BalanceChart.calledOnce, 'BalanceChart called');
    assert.ok(this.BalanceChart.calledWith(this.response_data, balance_chart.div_id), 'BalanceChart called with args');

});

QUnit.test('Upon successful submission return a new BalanceChart object', function(assert){
    var data = {'a': 1};
    var chart = balance_initialisation.success_callback(data);
    assert.ok(this.BalanceChart.calledWithNew())
});

QUnit.module('Successful ajax balance initialisation creates a first transaction prompt', {});

QUnit.test('test', function(assert){

    var data = {'a': 1};
    var first_transaction_prompt = sinon.stub(transactions, 'FirstTransactionPrompt');
    var BalanceChart = sinon.stub(balance_chart, 'BalanceChart');

    balance_initialisation.success_callback(data);
    
    assert.ok(first_transaction_prompt.calledOnce, 'FirstTransactionPrompt called');
    assert.ok(BalanceChart.calledBefore(first_transaction_prompt));

    BalanceChart.restore();
    first_transaction_prompt.restore();
});
