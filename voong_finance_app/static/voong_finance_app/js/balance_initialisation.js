console.log('balance_initialisation');

var balance_initialisation = {
    
    BalanceInitialisation: function (){
	var that = this;
	that.div = $('#balance-initialisation');
	that.input = that.div.find('#input');
	that.submit = that.div.find('#submit-button');
	that.submit.click(function(){
	    console.log('clicked');
	    var data = {balance: parseFloat(that.input.val())};
	    $.post(balance_initialisation.initialise_balance_url, data, balance_initialisation.success_callback);
	    that.div.remove();
	})
    },

    initialise_balance_url: '/api/initialise-balance',

    success_callback: function(data){
	return balance_chart.BalanceChart(balance_chart.div_id, data);
    }
    
}
