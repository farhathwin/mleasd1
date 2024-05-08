// Function to capitalize each word in a string
function capitalizeWords(str) {
    return str.replace(/\b\w/g, function (char) {
        return char.toUpperCase();
    });
}

// Attach keyup event to the input fields
$(document).ready(function () {
    // Initialize the International Telephone Input library
    var input = document.querySelector("#businhessPone");  // Replace with the actual ID of your phone input field
    var iti = window.intlTelInput(input, {
        separateDialCode: true,  // Enable separate country and dial code in the dropdown
        utilsScript: "https://cdn.jsdelivr.net/npm/intl-tel-input@17.0.13/build/js/utils.js",  // Add utilsScript for formatting and validation
    });

    // Attach keyup event to capitalize text input fields
    $('input[type="text"]').on('input', function () {
        // Get the input value
        var inputValue = $(this).val();

        // Exclude email and website fields from capitalization
        if ($(this).attr('name') !== 'business_email' && $(this).attr('name') !== 'website') {
            // Capitalize each word in the input value
            var capitalizedValue = capitalizeWords(inputValue);

            // Update the input value with the capitalized text
            $(this).val(capitalizedValue);
        }
    });

    $('#updateProfileBtn').on('click', function (e) {
        e.preventDefault();

        // Get the selected country data
        var countryData = iti.getSelectedCountryData();
        var countryCode = countryData.dialCode;

        // Get the phone number without the dial code and leading zeros
        var phoneWithoutCode = iti.getNumber(intlTelInputUtils.numberFormat.INTERNATIONAL)
            .replace("+" + countryCode, "")
            .replace(/^0+/, "")
            .trim();

        // Get the full international phone number including the country code
        var fullPhoneNumber = "+" + countryCode + " " + phoneWithoutCode;

        // Set the ITI value to the hidden input before serializing the form data
        $('#businhessPone').val(fullPhoneNumber);

        // Serialize the form data
        var formData = new FormData($('#agentProfileForm')[0]);

        // Log the form data to the console
        console.log("Form Data:", formData);

        // Send a POST request to the server
        $.ajax({
            url: '/agentprofile',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (data, textStatus, jqXHR) {
                // Check the HTTP status code for success (2xx range)
                if (jqXHR.status >= 200 && jqXHR.status < 300) {
                    $('#uploadStatus').html('<span style="color: green;">&#10003; Successfully updated</span>');
                    location.reload();  // Refresh the page
                } else {
                    $('#uploadStatus').html('<span style="color: red;">X Update failed</span>');
                }
            },
            error: function () {
                // Handle the error
                $('#uploadStatus').html('<span style="color: red;">X Update failed</span>');
            }
        });
    });

    // Add AJAX for /agentsubuserprofile route
    $('#updateProfileBtnSubuser').on('click', function (e) {
        e.preventDefault();

        // Get the selected country data
        var countryData = iti.getSelectedCountryData();
        var countryCode = countryData.dialCode;

        // Get the phone number without the dial code and leading zeros
        var phoneWithoutCode = iti.getNumber(intlTelInputUtils.numberFormat.INTERNATIONAL)
            .replace("+" + countryCode, "")
            .replace(/^0+/, "")
            .trim();

        // Get the full international phone number including the country code
        var fullPhoneNumber = "+" + countryCode + " " + phoneWithoutCode;

        // Set the ITI value to the hidden input before serializing the form data
        $('#businhessPone').val(fullPhoneNumber);

        // Serialize the form data
        var formData = new FormData($('#agentsubuserprofile')[0]);

        // Log the form data to the console
        console.log("Form Data (Subuser):", formData);

        // Send a POST request to the server
        $.ajax({
            url: '/agentsubuserprofile',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (data, textStatus, jqXHR) {
                // Check the HTTP status code for success (2xx range)
                if (jqXHR.status >= 200 && jqXHR.status < 300) {
                    $('#uploadStatus').html('<span style="color: green;">&#10003; Successfully updated</span>');
                    location.reload();  // Refresh the page
                } else {
                    $('#uploadStatus').html('<span style="color: red;">X Update failed</span>');
                }
            },
            error: function () {
                // Handle the error
                $('#uploadStatus').html('<span style="color: red;">X Update failed</span>');
            }
        });
    });

    $('#updateProfileBtnuser').on('click', function (e) {
        e.preventDefault();
        
        // Get the selected country data
        var countryData = iti.getSelectedCountryData();
        var countryCode = countryData.dialCode;
    
        // Get the phone number without the dial code and leading zeros
        var phoneWithoutCode = iti.getNumber(intlTelInputUtils.numberFormat.INTERNATIONAL)
            .replace("+" + countryCode, "")
            .replace(/^0+/, "")
            .trim();
    
        // Get the full international phone number including the country code
        var fullPhoneNumber = "+" + countryCode + " " + phoneWithoutCode;
    
        // Set the ITI value to the hidden input before serializing the form data
        $('#businhessPone').val(fullPhoneNumber);
    
        // Log the phone number to the console (for debugging)
        console.log("Full Phone Number:", fullPhoneNumber);
    
        // Serialize the form data
        var formData = new FormData($('#userProfileForm')[0]);  // Ensure the form ID is correct
    
        // Log the form data to the console
        console.log("Form Data (User):", formData);
    
        // Send a POST request to the server
        $.ajax({
            url: '/userprofile',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (data, textStatus, jqXHR) {
                // Check the HTTP status code for success (2xx range)
                if (jqXHR.status >= 200 && jqXHR.status < 300) {
                    $('#uploadStatus').html('<span style="color: green;">&#10003; Successfully updated</span>');
                    location.reload();  // Refresh the page
                } else {
                    $('#uploadStatus').html('<span style="color: red;">X Update failed</span>');
                }
            },
            error: function () {
                // Handle the error
                $('#uploadStatus').html('<span style="color: red;">X Update failed</span>');
            }
        });
    });

    $('#updateProfileBtnmastersubuser').on('click', function (e) {
        e.preventDefault();
        
        // Get the selected country data
        var countryData = iti.getSelectedCountryData();
        var countryCode = countryData.dialCode;
    
        // Get the phone number without the dial code and leading zeros
        var phoneWithoutCode = iti.getNumber(intlTelInputUtils.numberFormat.INTERNATIONAL)
            .replace("+" + countryCode, "")
            .replace(/^0+/, "")
            .trim();
    
        // Get the full international phone number including the country code
        var fullPhoneNumber = "+" + countryCode + " " + phoneWithoutCode;
    
        // Set the ITI value to the hidden input before serializing the form data
        $('#businhessPone').val(fullPhoneNumber);
    
        // Log the phone number to the console (for debugging)
        console.log("Full Phone Number:", fullPhoneNumber);
    
        // Serialize the form data
        var formData = new FormData($('#mastersubuserprofile')[0]);  // Ensure the form ID is correct
    
        // Log the form data to the console
        console.log("Form Data (User):", formData);
    
        // Send a POST request to the server
        $.ajax({
            url: '/mastersubuserprofile',
            type: 'POST',
            data: formData,
            contentType: false,
            processData: false,
            success: function (data, textStatus, jqXHR) {
                // Check the HTTP status code for success (2xx range)
                if (jqXHR.status >= 200 && jqXHR.status < 300) {
                    $('#uploadStatus').html('<span style="color: green;">&#10003; Successfully updated</span>');
                    location.reload();  // Refresh the page
                } else {
                    $('#uploadStatus').html('<span style="color: red;">X Update failed</span>');
                }
            },
            error: function () {
                // Handle the error
                $('#uploadStatus').html('<span style="color: red;">X Update failed</span>');
            }
        });
    });
});
