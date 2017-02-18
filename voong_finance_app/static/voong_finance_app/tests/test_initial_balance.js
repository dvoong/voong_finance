QUnit.module("Balance Initialisation Tests", {
    beforeEach: function(){
	this.balance_initialisation = new BalanceInitialisation();
	this.xhr = sinon.useFakeXMLHttpRequest();
	this.requests = [];
	this.xhr.onCreate = function(request) { this.requests.push(request); };
	this.server = sinon.fakeServer.create();
    },
    afterEach: function(){
	this.xhr.restore();
    }
});

// QUnit.test("Submitting initial balance removes/hides the initial balance div", function(assert) {
//     this.balance_initialisation.input.val(4344.40);
//     this.balance_initialisation.submit.click();
//     assert.equal(true, false, "TODO");
// });

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
