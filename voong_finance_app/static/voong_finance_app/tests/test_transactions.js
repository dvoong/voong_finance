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
		      transactions.append_form]
		    );

    get.restore();
});

QUnit.test('append_form tests', function(assert){
    var first_transaction_div = {html: sinon.stub()};
    var select = sinon.stub(d3, 'select').returns(first_transaction_div);
    var html_response = 'some html';

    transactions.append_form(html_response);

    assert.equal(select.firstCall.args, '#first-entry-prompt');
    assert.deepEqual(first_transaction_div.html.firstCall.args, [html_response])

    select.restore();
});

QUnit.module('submit_form', {
    beforeEach: function(){
	this.form_data = {};
	this.get_form_data = sinon.stub(transactions, 'get_form_data').returns(this.form_data);
	this.success = sinon.stub(transactions, 'on_successful_submission')
	this.post = sinon.stub($, 'post');
    },

    afterEach: function(){
	this.get_form_data.restore();
	this.success.restore();
	this.post.restore();
    }
});

QUnit.test('makes ajax post call', function(assert){
    
    transactions.submit_form();

    assert.deepEqual(this.post.firstCall.args, ['/api/transaction-form', this.form_data, this.success])

});

QUnit.test('form returns false, i.e. it overrides default form submission', function(assert){
    var response = transactions.submit_form();
    assert.equal(response, false);
});

// QUnit.test('on successful submit, call the success callback', 

QUnit.module('get_form_data', {
    beforeEach: function(){
	this.form = {serializeArray: function(){}};
	this.form_data = [{name: 'foo', value: 'bar'},
			  {name: 'cheese', value: 'camembert'}
			 ]
	this.jquery = sinon.stub(jQuery, 'call').returns(this.form);
	this.serializeArray = sinon.stub(this.form, 'serializeArray')
	    .returns(this.form_data);;
	
    },

    afterEach: function(){
	this.jquery.restore();
    }
});
// TODO: Find out how to mock jquery selections
// QUnit.test('selects form by its id', function(assert){

//     transactions.get_form_data();

//     assert.deepEqual(this.jquery.firstCall.args, ['#transaction-form']);

// });

// QUnit.test('calls serializeArray on the form selection', function(assert){

//     transactions.get_form_data();

//     assert.equal(this.serializeArray.callCount, 1);
//     assert.deepEqual(this.serializeArray.firstCall.args, []);

// });

// QUnit.test('returns object of ', function(assert){

//     var form_data = transactions.get_form_data();

//     assert.deepEqual(form_data, {foo: 'bar', cheese: 'camembert'});

// });

QUnit.module('on_successful_submission', {
    beforeEach: function(){
	this.response = {'columns': ['date', 'balance'], 'values': [['2017-03-01', 10], ['2017-03-02', 20]]};
	this.update_data = sinon.spy(balance_chart, 'update_data');
    },

    afterEach: function(){
	this.update_data.restore();
    }
});

QUnit.test('hide/remove the form', function(assert){

    transactions.on_successful_submission(this.response);

    assert.equal($('#transaction-form').length, 0);
});

QUnit.test('test calls BalanceChart.update_data with success data', function(assert){

    transactions.on_successful_submission(this.response);

    assert.deepEqual(this.update_data.firstCall.args, [this.response]);
});

// QUnit.module('update_data', {});

// Qunit.test('test', function(assert){
//     assert.ok(false, 'TODO');
// });
