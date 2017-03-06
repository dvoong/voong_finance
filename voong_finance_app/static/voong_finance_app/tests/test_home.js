var xhr, requests;
QUnit.module("initialisation tests", {
    beforeEach: function(){
	this.original_vf = jQuery.extend(true, {}, vf);
	xhr = sinon.useFakeXMLHttpRequest();
	this.requests = [];
	xhr.onCreate = function(request) { requests.push(request); };
    },
    afterEach: function(){
	vf = this.original_vf;
	xhr.restore();
    }
});

QUnit.test("Initialisation creates a balance_initialisation object", function(assert){
    assert.ok(vf.home.balance_initialisation === undefined);
    vf.home.initialise();
    assert.ok(vf.home.balance_initialisation !== undefined);
});
