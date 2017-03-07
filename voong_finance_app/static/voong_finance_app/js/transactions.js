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
};
