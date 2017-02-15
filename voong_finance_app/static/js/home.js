console.log("home.js");

function initialise(){
    
    $.get(vf.getBalanceUrl, {})
	.done(function(data){
    	    vf.createBalanceChart(data);
	})
	.fail(function(){
	    console.log("failed");
	});
    
};

vf.home = {
    initialise: initialise
}

$.ready(vf.home.initialise);

var balance_initialisation = new function(){
    this.div = $('#balance-initialisation');
    this.input = $('#input');
    this.submit_button = this.div.find('#submit-button');
    this.submit_button.click(function(){
	console.log('submit_button clicked');
    });
}

console.log(balance_initialisation);
