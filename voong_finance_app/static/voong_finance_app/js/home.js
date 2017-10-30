console.log("home.js");

$('#transaction-form').submit(function(e){
    console.log('submit form');
    e.preventDefault();

    var that = this;

    var args = $(this).serialize();
    $.post('create-transaction', $(this).serialize())
	.done(function(data, status, xhr){

	    console.log(data);
	    
	    var transactions_table = d3.select('#transactions-table tbody');
	    var selection = transactions_table.selectAll('tr.transaction');
	    
	    var transactions = selection.data();
	    transactions.push(data);
	    transactions.sort(function(a, b){
		if(a.date < b.date){
		    return -1
		} else if (a.date == b.date){
		    return a.ordinal < b.ordinal ? -1 : 1;		    
		}
		
		return 1
	    })

	    selection.remove();

	    var selection = transactions_table.selectAll('tr.transaction');
	    var selection = selection.data(transactions);
	    var enter = selection.enter();

	    var transaction = enter.append('tr')
	    .attr('class', 'transaction')

	    transaction.append('td')
		.attr('id', 'transaction-date')
		.html(function(d){
		    return d.date;
		});

	    transaction.append('td')
		.attr('id', 'transaction-type')
		.html(function(d){
		    return d.transaction_type;
		});

	    transaction.append('td')
		.attr('id', 'transaction-description')
		.html(function(d){
		    return d.description;
		});

	    transaction.append('td')
		.attr('id', 'transaction-size')
		.html(function(d){
		    return d.transaction_size;
		});

	    transaction.append('td')
		.attr('id', 'balance')
		.html(function(d){
		    return d.balance;
		});

	    $(that).find('#description-input').val('');
	    $(that).find('#size-input').val('');
	});
})

// function initialise(){
//     var balances = balance_chart.get_balances(vf.home.create_balance_chart);
//     $('#create-transaction-btn').click(function(){
// 	$.get('/api/transaction-form', function(response){
// 	    $('#balance-chart').append(response);
// 	});
//     });
// };

// function create_balance_chart(data){
//     _chart = new balance_chart.BalanceChart(data);
//     return _chart;
// };

// vf.home = {
//     initialise: initialise,
//     create_balance_chart: create_balance_chart,
// }
