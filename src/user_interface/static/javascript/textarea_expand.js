$(document).ready(function() {
    const textarea = document.getElementById('message_text');
    const lineHeight = parseInt(window.getComputedStyle(textarea).lineHeight, 10) || 20; // Default line height
    const maxLines = 7;

    function adjustTextareaHeight() {
        // Reset the textarea's rows for recalculation
        textarea.rows = 2; // Start with the minimum number of rows

        // Increase rows until the content fits
        while (textarea.scrollHeight > textarea.clientHeight && textarea.rows < maxLines) {
            textarea.rows += 1;
        }
    }

    // Adjust the textarea height on input
    textarea.addEventListener('input', adjustTextareaHeight);

    // Initial adjustment in case there's content already (e.g., when reloading with form data)
    adjustTextareaHeight();
});
