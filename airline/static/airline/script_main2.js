// Get references to the start and destination dropdown menus and table rows
var startSelect1 = document.getElementById("start1");
var destinationSelect1 = document.getElementById("destination1");
var tableRows1 = document.querySelectorAll("#route-table2 > tbody > tr");

// Define a function to filter the table rows based on the start and destination values
function filterRows1() {
// Convert the selected values to lowercase
var selectedStart1 = startSelect1.value.toLowerCase();
var selectedDestination1 = destinationSelect1.value.toLowerCase();

// Loop through all table rows and check if they match the selected values
for (var i = 0; i < tableRows1.length; i++) {
    var row1 = tableRows1[i];
    var start1 = row1.getAttribute("data-start1").toLowerCase();
    var destination1 = row1.getAttribute("data-destination1").toLowerCase();
    row1.style.display = "none"
    if ((selectedStart1 == "" || start1.includes(selectedStart1)) &&
    (selectedDestination1 == "" || destination1.includes(selectedDestination1))) {
    row1.style.display = "table-row";
    } else {
    row1.style.display = "none";
    }
}

// Apply row striping to the visible rows
stripeRows1();
}

// Define a function to apply row striping to the visible rows
function stripeRows1() {
// Get all visible rows in the flight table
var visibleRows1 = document.querySelectorAll("#route-table-body1 > tr:not([style*='display: none'])");

// Loop through each visible row and apply a background color class based on row index
for (var i = 0; i < visibleRows1.length; i++) {
    if (i % 2 === 0) {
    visibleRows1[i].classList.add("bg-light");
    } else {
    visibleRows1[i].classList.remove("bg-light");
    }
}
}

// Attach the filterRows() function to the change event of startSelect and destinationSelect
startSelect1.addEventListener("change", filterRows1);
destinationSelect1.addEventListener("change", filterRows1);

// Attach the filterRows() function to the DOMContentLoaded event of the document
document.addEventListener("DOMContentLoaded", function () {
filterRows1();
});

// Get references to the search input field, country list, and country items
const searchInput1 = document.getElementById("search-input-2");
const countryList1 = document.getElementById("country-list-2");
const countries1 = countryList1.querySelectorAll("li");

// Define an event listener for the input event of the searchInput field
searchInput1.addEventListener("input", function () {
// Convert the search term to lowercase
const searchTerm1 = searchInput1.value.toLowerCase();

// Loop through all country items and hide those that don"t match the search term
for (let i = 0; i < countries.length; i++) {
    const country1 = countries1[i];
    const name1 = country1.textContent.toLowerCase();

    if (name.includes(searchTerm)) {
    country1.style.display = "block";
    } else {
    country1.style.display = "none";
    }
}
});