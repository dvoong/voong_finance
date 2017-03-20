QUnit.module('initialisation', {
    
    stub: function(object, func){
	var stub = sinon.stub(object, func);
	this.stubs.push(stub);
	return stub;
    },
    
    beforeEach: function(){
	this.stubs = [];
	this.get_balances = this.stub(balance_chart, 'get_balances');
	this.create_balance_chart = this.stub(vf.home, 'create_balance_chart');
    },
    
    afterEach: function(){
	for(var i=0; i<this.stubs.length; i++){
	    this.stubs[i].restore();
	}
    }
    
});

QUnit.test('calls get_balances', function(assert){

    vf.home.initialise();

    assert.deepEqual(this.get_balances.firstCall.args, [this.create_balance_chart]);
});

QUnit.module('create_balance_chart', {
    stub: function(object, func){
	var stub = sinon.stub(object, func);
	this.stubs.push(stub);
	return stub;
    },
    
    beforeEach: function(){
	this.stubs = [];
	this.balance_chart = {};
	this.BalanceChart = this.stub(balance_chart, 'BalanceChart').returns(this.balance_chart);
	this.data = {};
    },
    
    afterEach: function(){
	for(var i=0; i<this.stubs.length; i++){
	    this.stubs[i].restore();
	}
    }
});

QUnit.test('', function(assert){

    vf.home.create_balance_chart(this.data);

    assert.deepEqual(this.BalanceChart.firstCall.args, [this.data]);
    assert.ok(this.BalanceChart.calledWithNew);
    assert.equal(_chart, this.balance_chart);
});

// var xhr, requests;
// QUnit.module("initialisation tests", {
//     beforeEach: function(){
// 	this.original_vf = jQuery.extend(true, {}, vf);
// 	xhr = sinon.useFakeXMLHttpRequest();
// 	this.requests = [];
// 	xhr.onCreate = function(request) { requests.push(request); };
//     },
//     afterEach: function(){
// 	vf = this.original_vf;
// 	xhr.restore();
//     }
// });

// QUnit.test("Initialisation creates a balance_initialisation object", function(assert){
//     assert.ok(vf.home.balance_initialisation === undefined);
//     vf.home.initialise();
//     assert.ok(vf.home.balance_initialisation !== undefined);
// });

QUnit.module('create_transaction_form', {});

QUnit.test('test', function(assert){

    vf.home.create_transaction_form()

    assert.ok(true);
});
