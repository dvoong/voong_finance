console.log("home.js");

function initialise(){
    
    // $.get(vf.getBalanceUrl, {})
    // 	.done(function(data){
    // 	    vf.createBalanceChart(data);
    // 	})
    // 	.fail(function(){
    // 	    console.log("failed");
    // 	});

    vf.home.balance_initialisation = new BalanceInitialisation();
    
};

vf.home = {
    initialise: initialise
}
