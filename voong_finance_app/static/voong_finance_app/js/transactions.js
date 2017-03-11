console.log('transactions');

var transactions = new function(){
    this.FirstTransactionPrompt = function(){
	d3.select('body')
	    .append('div')
	    .attr('id', 'first-entry-prompt');

	$.get('/api/transaction-form', transactions.append_form);
    };

    this.append_form = function(html_form){
	d3.select('#first-entry-prompt')
	    .html(html_form);
    };

    this.get_form_data = function(){
	var form_data = $('#transaction-form')
	    .serializeArray()
	    .reduce(function(obj, item) {
	     	obj[item.name] = item.value;
	     	return obj;
	    }, {})
	return form_data;
    };
    

    this.on_successful_submission = function(){
	$('#transaction-form').remove();
	$('#first-entry-prompt').remove();
    };

    this.submit_form = function(){
	var csrftoken = vf.getCookie('csrftoken');
	$.ajaxSetup({
	    beforeSend: function(xhr, settings) {
		if (!vf.csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader("X-CSRFToken", csrftoken);
		}
	    }
	});
	$.post('/api/transaction-form',
	       transactions.get_form_data(),
	       transactions.on_successful_submission);
	return false;
    };
};
