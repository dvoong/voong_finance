console.log('transactions');

var transactions = new function(){
    this.FirstTransactionPrompt = function(){
	d3.select('body')
	    .append('div')
	    .attr('id', 'first-entry-prompt');

	console.log('get transaction-form');
	$.get('/api/transaction-form', transactions.append_form);
    };

    this.append_form = function(html_form){
	console.log('append_form: ' + html_form);
	d3.select('#first-entry-prompt')
	    .html(html_form);
    };
};

console.log(transactions);
