console.log("home.js");

function initialise(){
    var balances = balance_chart.get_balances(vf.home.create_balance_chart)
};

function create_balance_chart(data){
    _chart = new balance_chart.BalanceChart(data);
    return _chart;
};

vf.home = {
    initialise: initialise,
    create_balance_chart: create_balance_chart
}
