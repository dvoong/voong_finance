console.log('balance_initialisation');

var balance_initialisation = {
    
    BalanceInitialisation: function (){
	var that = this;
	that.div = $('#balance-initialisation');
	that.input = that.div.find('#input');
	that.date_input = that.div.find('#date');
	that.submit = that.div.find('#submit-button');
	that.submit.click(function(){
	    var data = {balance: parseFloat(that.input.val()), date: that.date_input.val()};
	    var csrftoken = getCookie('csrftoken');
	    $.ajaxSetup({
		beforeSend: function(xhr, settings) {
		    if (!vf.csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		    }
		}
	    });
	    $.post(balance_initialisation.initialise_balance_url, data, balance_initialisation.success_callback);
	    that.div.remove();
	})
    },

    initialise_balance_url: '/api/initialise-balance',

    success_callback: function(data){
	var date = data['date'];
	var balance = data['balance'];
	var data = {columns: ['date', 'balance'], values: [[date, balance]]}; // change format
	var start = new Date(new Date(date) - 1 * 24 * 60 * 60 * 1000);
	var end = new Date(date);
	end.setDate(end.getDate() + 27);
	var data = balance_chart.pad_dates(data, start, end) // with padded dates
	new balance_chart.BalanceChart(data, balance_chart.div_id);
	var first_transaction_prompt = new transactions.FirstTransactionPrompt();
    }
    
}
