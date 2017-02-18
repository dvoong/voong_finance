function BalanceInitialisation(){
    var that = this;
    that.div = $('#balance-initialisation');
    that.input = that.div.find('#input');
    that.submit = that.div.find('#submit-button');
    that.submit.click(function(){
	console.log('clicked');
	that.div.remove();
    });
}
