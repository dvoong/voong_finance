console.log("home.js");

function initialise(){
    
    $.get(vf.home.getBalanceUrl, {})
	.done(function(){
    	    console.log("done");
    	    vf.createBalanceChart();
	})
	.fail(function(){
	    console.log("failed");
	});
    
};

vf.home.initialise = initialise;

$.ready(vf.home.initialise);
