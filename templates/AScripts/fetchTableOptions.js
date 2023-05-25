function fetchTableOptions() {
    // Make a request to fetch the table options from the backend
    Plotly.d3.json('/tables', function(error, data) {
        if (error) {
            console.log(error);
            return;
        }

        var tableOptions = data.tables; // Assuming the response contains an array of table names

        // Populate the fieldA and fieldB select elements with the table options
        var fieldASelect = document.getElementById('fieldA');
        var fieldBSelect = document.getElementById('fieldB');

        tableOptions.forEach(function(option) {
            var optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.text = option;
            fieldASelect.appendChild(optionElement);

            optionElement = document.createElement('option');
            optionElement.value = option;
            optionElement.text = option;
            fieldBSelect.appendChild(optionElement);
        });
    });
}

fetchTableOptions(); // Call the function to populate the select elements on page load
