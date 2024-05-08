$(document).ready(function() {
    var input = document.querySelector("#phone_no");
    var iti = window.intlTelInput(input, {
        utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
        initialCountry: "auto",
        separateDialCode: true,
        preferredCountries: ["us", "gb", "ca"],
        formatOnDisplay: true,
        nationalMode: false,
        autoPlaceholder: "polite",
        placeholderNumberType: "MOBILE",
        geoIpLookup: function(callback) {
            $.get("https://ipinfo.io", function() {}, "jsonp").always(function(resp) {
                var countryCode = (resp && resp.country) ? resp.country : "";
                callback(countryCode);
            });
        }
    });

    $('#customerCreateForm').on('submit', function(event) {
        event.preventDefault();

        if (!iti.isValidNumber()) {
            $('#error-msg').text('Please enter a valid phone number.');
            $('#valid-msg').text('');
            return;
        }

        $('#error-msg').text('');
        $('#valid-msg').text('Phone number is valid.');

        // Directly get the phone number in E.164 format, which includes the country code
        var phoneNumber = iti.getNumber(intlTelInputUtils.numberFormat.E164);
        console.log('Final phone number being sent:', phoneNumber);


        // Submit form data using AJAX
        $.ajax({
            url: '/customer-create',
            method: 'POST',
            data: {
                full_name: $('#full_name').val(),
                email: $('#email').val(),
                phone_no: phoneNumber // No need to manually prepend the country code
            },
            success: function(data) {
                if (data.success) {
                    alert(data.message);
                    window.location.href = '/customers_list';
                } else {
                    $('#error-message').text(data.message);
                }
            },
            error: function(xhr, status, error) {
                console.error('XHR Status:', status);
                console.error('Error:', error);
                var errorMessage = xhr.responseJSON && xhr.responseJSON.message ? xhr.responseJSON.message : 'An error occurred. Please try again.';
                $('#error-message').text(errorMessage);
            }
        });
        
    });
});


function filterCustomers() {
    var input = document.getElementById("customerSearch");
    var filter = input.value.toUpperCase();
    var ul = document.getElementById("customerList");
    var li = ul.getElementsByTagName("li");
    var isVisible = false;

    for (var i = 0; i < li.length; i++) {
        var txtValue = li[i].textContent || li[i].innerText;
        if (txtValue.toUpperCase().indexOf(filter) > -1) {
            li[i].style.display = "";
            isVisible = true;
        } else {
            li[i].style.display = "none";
        }
    }

    // Only display the list if there are matching results or if there's text in the input
    ul.style.display = isVisible && input.value ? "block" : "none";
}

function selectCustomer(item) {
    var customerId = item.getAttribute("data-customer-id");
    document.getElementById("selectedCustomerId").value = customerId;
    document.getElementById("customerSearch").value = item.textContent.trim().split(" - ")[0]; // Display only the name
    document.getElementById("customerList").style.display = "none";
}
// Function to close the customer creation modal
function closeCustomerModal() {
    $('#customerCreateModal').modal('hide'); // Hide the modal
    $('#customerCreateModelForm')[0].reset(); // Reset the form fields
}

// Function to select the newly created customer in the dropdown
function selectNewCustomer(customerId, customerName) {
    $('#customer_id').append($('<option>', {
        value: customerId,
        text: customerName,
        selected: true // Automatically select the newly created customer
    }));
}

$(document).ready(function() {
    // Initialize the phone validation
    var input = document.querySelector("#phone_no");
    var iti = window.intlTelInput(input, {
        utilsScript: "https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.8/js/utils.js",
        initialCountry: "auto",
        separateDialCode: true,
        preferredCountries: ["us", "gb", "ca"],
        formatOnDisplay: true,
        nationalMode: false,
        autoPlaceholder: "polite",
        placeholderNumberType: "MOBILE",
        geoIpLookup: function(callback) {
            $.get("https://ipinfo.io", function() {}, "jsonp").always(function(resp) {
                var countryCode = (resp && resp.country) ? resp.country : "";
                callback(countryCode);
            });
        }
    });

    $('#customerCreateModelForm').submit(function(event) {
        event.preventDefault(); // Prevent default form submission

        if (!iti.isValidNumber()) {
            $('#error-msg').text('Please enter a valid phone number.');
            $('#valid-msg').text('');
            return;
        }

        $('#error-msg').text('');
        $('#valid-msg').text('Phone number is valid.');

        var phoneNumber = iti.getNumber(intlTelInputUtils.numberFormat.E164); // Get the phone number in E.164 format

        // Update the phone number input with the E.164 formatted number
        $('#phone_no').val(phoneNumber);

        // Serialize the form data including the updated phone number
        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: $(this).attr('action'),
            data: formData,
            success: function(response) {
                if (response.success) {
                    closeCustomerModal(); // Close the modal on success
                    var customerId = response.customer_id;
                    var customerName = response.customer_name;
                    
                    // Select the newly created customer in the customer search box
                    $('#customerSearch').val(customerName);
                    $('#selectedCustomerId').val(customerId);
                    
                    alert('Customer created successfully.');
                } else {
                    alert('Failed to create customer: ' + (response.message || 'Please try again.'));
                }
            },
            error: function(xhr, status, error) {
                console.error('XHR Status:', status);
                console.error('Error:', error);
                var errorMessage = xhr.responseJSON && xhr.responseJSON.message ? xhr.responseJSON.message : 'An error occurred. Please try again.';
                $('#error-message').text(errorMessage);
                alert('Error: ' + errorMessage);
            }
        });
    });
});





