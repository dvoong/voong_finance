console.log("home.js");

function initialise(){
    console.log("initialise");
    $.get(vf.home.getBalanceUrl, {
	csrfmiddlewaretoken: token
    });
};

vf.home.initialise = initialise

$.ready(vf.home.initialise);
