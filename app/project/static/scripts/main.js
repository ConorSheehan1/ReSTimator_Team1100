// CHART
console.log('HI STEPHEN');

// Load the Visualization API and the corechart package.
//google.charts.load('current', {'packages':['corechart']});

function test() {
    console.log('hello222');
}

//function drawChart(bikes, stands, date) { // function that draws chart
function drawChart(results) { // function that draws chart
    // date parameter currently unused - might change
//    document.getElementById('response').style.display = "block"; // displays response div on webpage
    
    // Create the data table.
    var data = new google.visualization.DataTable(); // create data object
    data.addColumn('string', 'Time');
    data.addColumn('number', 'Occupancy %');
    for (i = 0; i < results.length; i++) {
        data.addRow([results[i].time, results[i].occupancy]);
    }

    // Set chart options
    var options = {'title':'Average Bikes/Stands per Day of Week',
                   'width':680,
                   'height':300};

    // create instance of chart, in 'graph' div on webpage - this is within 'response' div
    var chart = new google.visualization.LineChart(document.getElementById('chart'));
    chart.draw(data, options); //pass data object and options used for drawing graph
}