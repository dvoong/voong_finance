console.log("home.js");

function initialise(){
    
    $.get(vf.getBalanceUrl, {})
	.done(function(data){
    	    console.log("done");
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
