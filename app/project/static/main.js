// CHART
console.log('HELLO STEPHEN');

// Load the Visualization API and the corechart package.
//google.charts.load('current', {'packages':['corechart']});

function test() {
    console.log('hello555');
}

function drawChart(results) { // function that draws chart
    
    // Create the data table.
    var data = new google.visualization.DataTable(); // create data object
    data.addColumn('string', 'Time');
    data.addColumn('number', 'Occupancy %');
    for (i = 0; i < results.length; i++) {
        data.addRow([results[i].time, results[i].occupancy]);
    }

    // Set chart options
    var options = {'title':'Estimated Occupancy per Hour',
                   'width':680,
                   'height':300};

    // create instance of chart in 'chart' div on webpage
    var chart = new google.visualization.LineChart(document.getElementById('chart'));
    chart.draw(data, options); //pass data object and options used for drawing graph
}