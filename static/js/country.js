// Function to update the hidden input field with the ISO code of the selected country
function updateCountryISOCode() {
    var selectedCountry = $("#country").val();
    $("#country_iso_code").val(selectedCountry);
}

// Function to map the API data in select format
const mapper = (data) => {
    return data.map((item) => {
        return {
            id: item.id,
            text: `${item.name} (${item.iso2})`
        };
    });
};

// Declare global variables to store country and state mappings
let countryMapping = {};
let stateMapping = {};

// Function to fetch country and state data from the API and populate mappings
const fetchCountryAndStateData = () => {
    const base = "https://api.countrystatecity.in/v1";
    const apiKey = "eWVpM3Zwd3RmN3pMMlUzdWtOejBrZ0s1ZVlqa1dvUlpXcUFTMHdPdw=="; // Replace with your actual API key

    // Fetch countries
    $.ajax({
        url: `${base}/countries`,
        method: 'GET',
        headers: {
            "X-CSCAPI-KEY": apiKey
        },
        success: function (countries) {
            // Map countries to your countryMapping object
            countryMapping = Object.fromEntries(countries.map(country => [country.id, country.name]));

            // Fetch states for each country
            countries.forEach(country => {
                $.ajax({
                    url: `${base}/countries/${country.id}/states`,
                    method: 'GET',
                    headers: {
                        "X-CSCAPI-KEY": apiKey
                    },
                    success: function (states) {
                        // Map states to your stateMapping object for the specific country
                        stateMapping[country.id] = Object.fromEntries(states.map(state => [state.id, state.name]));
                    },
                    error: function (error) {
                        console.error("Error fetching states:", error);
                    }
                });
            });
        },
        error: function (error) {
            console.error("Error fetching countries:", error);
        }
    });
};

// Call the fetchCountryAndStateData function to populate mappings
fetchCountryAndStateData();

// Function to initialize Select2 for a given element
const initializeSelect2 = (element, placeholder, data) => {
    element.empty(); // Clear existing options
    element.val(null).trigger('change'); // Clear selected value
    element.select2({
        placeholder: placeholder,
        data: mapper(data),
        // Add this line to configure select2 to use the text field
        id: function (item) {
            return item.text;
        },
    });
};

// Function to send data to the server
const sendDataToServer = () => {
    const selectedCountryId = $('#country').select2('data')[0].id; // Use id to get the country code
    const selectedStateId = $('#state').select2('data')[0].id; // Use id to get the state code

    // Map country and state codes to names
    const selectedCountryName = countryMapping[selectedCountryId] || 'Unknown Country';
    const selectedStateName = stateMapping[selectedCountryId] ? stateMapping[selectedCountryId][selectedStateId] || 'Unknown State' : 'Unknown State';

    // Modify this data structure to include the country name and state name
    const data = {
        trading_name: $('input[name="trading_name"]').val(),
        street_1: $('input[name="street_1"]').val(),
        street_2: $('input[name="street_2"]').val(),
        town_city: $('input[name="town_city"]').val(),
        state_province: selectedStateName,
        country: selectedCountryName,
        // Include other data you're sending to the server
    };

    // Your AJAX request
    $.ajax({
        url: '/agentprofile',
        method: 'POST',
        data: data,
        // other settings...
        success: function (response) {
            // Handle success
        },
        error: function (error) {
            // Handle error
        }
    });
};

// Assuming there is a form submission event where you call sendDataToServer
$('#agentProfileForm').on('submit', function (event) {
    event.preventDefault();
    sendDataToServer();
});

// Wrap the code in a document ready function
$(document).ready(function () {
    // Load Select2 library
    $.getScript("https://cdnjs.cloudflare.com/ajax/libs/select2/4.0.12/js/select2.min.js", function () {
        // Ensure the script is loaded before proceeding

        const base = "https://api.countrystatecity.in/v1";
        const apiKey = "eWVpM3Zwd3RmN3pMMlUzdWtOejBrZ0s1ZVlqa1dvUlpXcUFTMHdPdw=="; // Replace with your actual API key

        // Initialize country and state select dropdowns.
        const countrySelect = $('#country');
        const stateSelect = $('#state');
        const citySelect = $('#city'); // Add city dropdown

        initializeSelect2(countrySelect, "Select a country", []);

        // Handle change event of the country dropdown
        countrySelect.on('change', function () {
            const selectedCountry = $(this).val();

            // Check if a country is selected
            if (selectedCountry) {
                // Fetch a list of States within the selected country
                $.ajax({
                    url: `${base}/countries/${selectedCountry}/states`,
                    method: 'GET',
                    headers: {
                        "X-CSCAPI-KEY": apiKey
                    },
                    success: function (statesData) {
                        console.log(`States in ${selectedCountry}:`, statesData);

                        // Initialize state select dropdown.
                        initializeSelect2(stateSelect, "Select a state/province", statesData);
                    },
                    error: function (error) {
                        console.error("Error fetching states:", error);
                        alert('Error fetching states. Please try again later.');
                    }
                });
            } else {
                // Clear the state dropdown if no country is selected
                initializeSelect2(stateSelect, "Select a state/province", []);
            }
        });

        // Handle change event of the state dropdown
        stateSelect.on('change', function () {
            const selectedCountry = countrySelect.val();
            const selectedState = $(this).val();

            // Check if a country and state are selected
            if (selectedCountry && selectedState) {
                // Fetch a list of Cities within the selected country and state
                $.ajax({
                    url: `${base}/countries/${selectedCountry}/states/${selectedState}/cities`,
                    method: 'GET',
                    headers: {
                        "X-CSCAPI-KEY": apiKey
                    },
                    success: function (citiesData) {
                        console.log(`Cities in ${selectedCountry}, ${selectedState}:`, citiesData);

                        // Update city dropdown options
                        initializeSelect2(citySelect, "Select a city", citiesData);
                    },
                    error: function (error) {
                        console.error("Error fetching cities:", error);
                        alert('Error fetching cities. Please try again later.');
                    }
                });
            } else {
                // Clear the city dropdown if no country or state is selected
                initializeSelect2(citySelect, "Select a city", []);
            }
        });

        // Get a list of Countries
        $.ajax({
            url: `${base}/countries`,
            method: 'GET',
            headers: {
                "X-CSCAPI-KEY": apiKey
            },
            success: function (data) {
                console.log("Countries:", data);

                // Update country dropdown options
                initializeSelect2(countrySelect, "Select a country", data);
            },
            error: function (error) {
                console.error("Error fetching countries:", error);
                alert('Error fetching countries. Please try again later.');
            }

            
        });

    });
});
