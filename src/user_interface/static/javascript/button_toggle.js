$(document).ready(function() {
    // Function to programmatically check a radio button and update the active class
    function checkRadioButton(radioName, valueToCheck) {
        // Find all radio buttons with the specified name
        $('input[type="radio"][name="' + radioName + '"]').each(function() {
            if ($(this).val() === valueToCheck) {
                // Check this radio button and add the active class to its label
                $(this).prop('checked', true);
                $(this).closest('label').addClass('active');
            } else {
                // Ensure other radio buttons are unchecked and their labels are not active
                $(this).prop('checked', false);
                $(this).closest('label').removeClass('active');
            }
        });
    }

    // Listen for changes on any radio buttons with the name 'stopwords'
    $('input[type="radio"][name="stopwords"]').change(function() {
        // Remove 'active' class from all labels within the same button group
        $(this).closest('.btn-group-toggle').find('.btn').removeClass('active');

        // Add 'active' class back to the label that contains the newly checked radio button
        $(this).closest('label').addClass('active');
    });

    // Example usage:
    // To select "Without Stop Words", you would now use "True" as the value to check.
    checkRadioButton('stopwords', 'False');

    // Similarly, to select "With Stop Words", you would use "False".
    // checkRadioButton('stopwords', 'False');
});