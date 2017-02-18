console.log("home.js");

function initialise(){
    console.log('initialise');
    
    console.log(balance_initialisation);
    vf.home.balance_initialisation = new balance_initialisation.BalanceInitialisation();
    
};

vf.home = {
    initialise: initialise
}
