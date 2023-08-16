// Get the DOM elements for the start and destination select inputs, and all rows of the flight table

var startSelect = document.querySelector(".start");
var destinationSelect = document.querySelector(".destination");
var tableRows = document.querySelectorAll(".flight-table-body tr");

// Define a function that filters the rows of the flight table based on the selected start and destination airports
function filterRows() {
// Get the selected start and destination airport values and convert to lowercase for case-insensitive matching
var selectedStart = startSelect.value.toLowerCase();
var selectedDestination = destinationSelect.value.toLowerCase();

// Loop through each row of the flight table
for (var i = 0; i < tableRows.length; i++) {
    var row = tableRows[i];
    
    // Get the start and destination airport values for the current row and convert to lowercase for case-insensitive matching
    var start = row.getAttribute("data-start").toLowerCase();
    var destination = row.getAttribute("data-destination").toLowerCase();
    
    // If the current row matches the selected start and destination airports, show the row, otherwise hide the row
    if ((selectedStart === "" || start.includes(selectedStart)) &&
        (selectedDestination === "" || destination.includes(selectedDestination))) {
    row.style.display = "";
    } else {
    row.style.display = "none";
    }
}

// Call the stripeRows function to alternate row colors of visible rows
stripeRows();
}

// Define a function that alternates the background color of visible rows in the flight table
function stripeRows() {
// Get all visible rows in the flight table
var visibleRows = document.querySelectorAll(".flight-table-body tr:not([style*='display: none'])");

// Loop through each visible row and apply a background color class based on row index
for (var i = 0; i < visibleRows.length; i++) {
    if (i % 2 === 0) {
    visibleRows[i].classList.add("bg-light");
    } else {
    visibleRows[i].classList.remove("bg-light");
    }
}
}

// Add event listeners to the start and destination select inputs to trigger the filterRows function when changed, and call the filterRows function on page load
startSelect.addEventListener("change", filterRows);
destinationSelect.addEventListener("change", filterRows);
document.addEventListener("DOMContentLoaded", function() {
filterRows();
});