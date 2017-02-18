var xhr, requests;
QUnit.module("initialisation tests", {
    beforeEach: function(){
	this.original_vf = jQuery.extend(true, {}, vf);
	xhr = sinon.useFakeXMLHttpRequest();
	requests = [];
	xhr.onCreate = function(request) { requests.push(request); };
    },
    afterEach: function(){
	vf = this.original_vf;
	xhr.restore();
    }
});

QUnit.test("initialise makes an ajax call to get the balance data", function(assert) {
    initialise();
    assert.equal(requests.length, 1, 'check ajax request');
    assert.equal(requests[0].method, 'GET', 'check http method');
    assert.equal(requests[0].url, vf.getBalanceUrl, 'check url');
});

QUnit.test("On unsuccessful response create balance chart", function(assert) {
    var mock_vf = sinon.mock(vf);
    var exp = mock_vf.expects("createBalanceChart").never()
    var server = sinon.fakeServer.create();
    server.respondWith([403, {}, "unauthorised"]);

    vf.home.initialise();

    assert.equal(exp.verify(), true);
    mock_vf.restore();
});

QUnit.test("On successful response create balance chart", function(assert) {
    var mock_vf = sinon.mock(vf);
    var exp = mock_vf.expects("createBalanceChart").once();
    var data = [{ "id": 12, "comment": "Hey there" }]
    var server = sinon.fakeServer.create();
    server.respondWith("GET", vf.getBalanceUrl, [200, { "Content-Type": "application/json" }, JSON.stringify(data)]);

    vf.home.initialise();
    server.respond();
    
    assert.equal(exp.verify(), true);
    mock_vf.restore();
});

QUnit.test("Initialisation creates a balance_initialisation object", function(assert){
    assert.ok(vf.home.balance_initialisation === undefined);
    vf.home.initialise();
    assert.ok(vf.home.balance_initialisation !== undefined);
});
