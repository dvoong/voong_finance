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
	    console.log('done');
	    console.log(data);
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
