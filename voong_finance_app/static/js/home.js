console.log("home.js");

function initialise(){
    console.log("initialise");
    $.get(url, {
	csrfmiddlewaretoken: token
    });
};

var vf = {
    home: {
	initialise: initialise
    }
};

$.ready(vf.home.initialise);
