$(document).ready(function() {
    $('#model').change(function() {
        var selectedFile = $(this).val(); // Get the selected file name
        $.ajax({
            type: "POST",
            url: "/load_model",
            data: {
                filename: selectedFile
            },
        })
    });
});

