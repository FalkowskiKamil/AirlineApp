// Get references to the start and destination dropdown menus and table rows
var startSelect = document.getElementById("start2");
var destinationSelect = document.getElementById("destination2");
var tableRows = document.querySelectorAll("#route_table1 > tbody > tr");

// Define a function to filter the table rows based on the start and destination values
function filterRows2() {
// Convert the selected values to lowercase
var selectedStart = startSelect.value.toLowerCase();
var selectedDestination = destinationSelect.value.toLowerCase();

// Loop through all table rows and check if they match the selected values
for (var i = 0; i < tableRows.length; i++) {
    var row = tableRows[i];
    var start = row.getAttribute("data-start2").toLowerCase();
    var destination = row.getAttribute("data-destination2").toLowerCase();
    row.style.display = "none"
    if ((selectedStart == "" || start.includes(selectedStart)) &&
    (selectedDestination == "" || destination.includes(selectedDestination))) {
    row.style.display = "table-row";
    } else {
    row.style.display = "none";
    }
}

// Apply row striping to the visible rows
stripeRows();
}
// Define a function to apply row striping to the visible rows
function stripeRows() {
// Get all visible rows in the flight table
var visibleRows = document.querySelectorAll("#route-table-body > tr:not([style*='display: none'])");

// Loop through each visible row and apply a background color class based on row index
for (var i = 0; i < visibleRows.length; i++) {
    if (i % 2 === 0) {
    visibleRows[i].classList.add("bg-light");
    } else {
    visibleRows[i].classList.remove("bg-light");
    }
}
}

// Attach the filterRows() function to the change event of startSelect and destinationSelect
startSelect.addEventListener("change", filterRows2);
destinationSelect.addEventListener("change", filterRows2);

// Attach the filterRows() function to the DOMContentLoaded event of the document
document.addEventListener("DOMContentLoaded", function () {
filterRows2();
});


// Get references to the search input field, country list, and country items
const searchInput = document.getElementById("search-input");
const countryList = document.getElementById("country-list");
const countries = countryList.querySelectorAll("li");

// Define an event listener for the input event of the searchInput field
searchInput.addEventListener("input", function () {
// Convert the search term to lowercase
const searchTerm = searchInput.value.toLowerCase();

// Loop through all country items and hide those that don"t match the search term
for (let i = 0; i < countries.length; i++) {
    const country = countries[i];
    const name = country.textContent.toLowerCase();

    if (name.includes(searchTerm)) {
    country.style.display = "block";
    } else {
    country.style.display = "none";
    }
}
});