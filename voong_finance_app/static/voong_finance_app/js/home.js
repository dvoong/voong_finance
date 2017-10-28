console.log("home.js");

$('#transaction-form').submit(function(e){
    console.log('submit form');
    e.preventDefault();

    console.log(e);
    console.log(this);
    var args = $(this).serialize();
    console.log(args);
    console.log($(this).serializeArray());
    $.post('create-transaction', $(this).serialize())
	.done(function(data, status, xhr){
	    var transactions_table = d3.select('#transactions-table tbody');
	    var selection = transactions_table.selectAll('tr.transaction')
	    .data([data]);
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

	    console.log('done');
	    console.log(data);
	    console.log(enter);
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
