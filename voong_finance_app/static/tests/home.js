console.log("home.js");

function initialise(){
    console.log("initialise");
};

var vf = {
    home: {
	initialise: initialise
    }
};

$.ready(vf.home.initialise);
