QUnit.module("Balance Initialisation Tests", {
    beforeEach: function(){
	this.balance_initialisation = new balance_initialisation.BalanceInitialisation();
	this.xhr = sinon.useFakeXMLHttpRequest();
	this.requests = [];
	this.xhr.onCreate = function(request) { this.requests.push(request); };
	this.server = sinon.fakeServer.create();
    },
    afterEach: function(){
	this.xhr.restore();
    }
});

QUnit.test('Submission of the form makes an ajax call to the initialise_balance api', function(assert){
    var stub = sinon.stub(jQuery, 'post');
    var url = balance_initialisation.initialise_balance_url;
    var data = {balance: 4344.40}
    var callback = balance_initialisation.success_callback;
    this.balance_initialisation.input.val(data.balance);
    this.balance_initialisation.submit.click();
    assert.ok(stub.calledOnce);
    assert.ok(stub.calledWith(url, data, callback));
});

QUnit.test('Upon successful submission of the form hide/delete the balance_initialisation  div', function(assert){
    // mock a ajax response
    assert.ok($('#balance-initialisation').length == 1, "found balance-initialisation div");
    this.server.respondWith("POST",
			    this.balance_initialisation.initialise_balance_url,
			    [200, {}, '']
			   );
    this.balance_initialisation.input.val(4344.40);
    this.balance_initialisation.submit.click();
    this.server.respond();
    assert.ok($('#balance-initialisation').length == 0, "balance-initialisation removed from document");
});

QUnit.test('Upon successful submission of the form call create_balance_chart', function(assert){

    var spy = sinon.spy(balance_chart, 'BalanceChart');
    console.log(spy)
    var data = {date: ['2017-01-24', '2017-01-25'], balance: [10, 10]}
    this.server.respondWith("POST",
			    this.balance_initialisation.initialise_balance_url,
			    [200, { "Content-Type": "application/json" }, JSON.stringify(data)]
			   );
    this.balance_initialisation.submit.click();
    this.server.respond();
    console.log(spy.callCount);
    assert.ok(spy.calledOnce, 'BalanceChart not called');
    assert.ok(spy.calledWith(balance_chart.div_id, data), 'BalanceChart not called with args');
});
