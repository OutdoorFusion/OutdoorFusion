function generatePlot() {
    var fieldA = document.getElementById('fieldA').value;
    var fieldB = document.getElementById('fieldB').value;

    Plotly.d3.json('/plot?field_a=' + fieldA + '&field_b=' + fieldB, function(error, data) {
        if (error) {
            console.log(error);
        }
        Plotly.newPlot('plot', data.data, data.layout);
    });
}



function generateVisualization() {
    var chartType = document.getElementById('chart-type').value;

    if (chartType === 'generatePlot') {
        generatePlot();
        return;
    }

    // Make a request to the appropriate route based on the selected chart type
    var url = '/chart?type=' + chartType;
    if (chartType === 'scatter') {
        var fieldA = document.getElementById('fieldA').value;
        var fieldB = document.getElementById('fieldB').value;
        url += '&field_a=' + fieldA + '&field_b=' + fieldB;
    } else if (chartType === 'pie') {
        var fieldA = document.getElementById('fieldA').value;
        url += '&field_a=' + fieldA;
    } else if (chartType === 'bar') {
        var fieldA = document.getElementById('fieldA').value;
        url += '&field_a=' + fieldA;
    }

    Plotly.d3.json(url, function(error, data) {
        if (error) {
            console.log(error);
        }

        if (chartType === 'scatter') {
            Plotly.newPlot('plot', data.data, data.layout);
        } else if (chartType === 'pie')
        {
            var pieData = [{
                values: data.data[0].values,
                labels: data.data[0].labels,
                type: 'pie'
            }];
            var pieLayout = {
                title: ''
            };
            Plotly.newPlot('plot', pieData, pieLayout);
        } else if (chartType === 'bar') {
            var barData = [{
                x: data.data[0].x,
                y: data.data[0].y,
                type: 'bar'
            }];
            var barLayout = {
                title: ' '
            };
            Plotly.newPlot('plot', barData, barLayout);
        }
    });
}


document.getElementById('generate-btn').addEventListener('click', generateVisualization);
