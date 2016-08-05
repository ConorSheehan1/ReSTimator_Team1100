function test() {
    console.log('Testing function call external JS');
}

// CHART
function drawChart(results) { // function that draws chart
    
    // Create the data table.
    var data = new google.visualization.DataTable(); // create data object
    data.addColumn('string', 'Time');
    data.addColumn('number', 'Predicted');
    data.addColumn('number', 'Occupancy');
    for (i = 0; i < results.length; i++) {
        data.addRow([results[i].time, results[i].predicted, results[i].occupancy_number]);
    }

    // Set chart options
    var options = {title:'Estimated Occupancy per Hour',
                   width:650,
                   height:300,
                   vAxis: {title: "Number of Students"},
                   hAxis: {title: "Time"},
                   animation:{
                       duration: 1000,
                       easing: 'inAndOut',
                       startup: true
                   }
                  };

    // create instance of chart in 'chart' div on webpage
    var chart = new google.visualization.LineChart(document.getElementById('chart'));
    chart.draw(data, options); //pass data object and options used for drawing graph
}