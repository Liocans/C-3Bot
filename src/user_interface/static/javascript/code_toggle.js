$(document).ready(function() {

    document.getElementById('code_toggle').addEventListener('click', function() {
        const textarea = document.getElementById('message_text');
        const text = textarea.value;
        const codeQuote = '```';

        if (text.startsWith(codeQuote) && text.endsWith(codeQuote)) {
            // If text is wrapped with ```, remove them
            textarea.value = text.slice(3, text.length - 3).trim();
        } else {
            // If not wrapped, wrap the text with ```
            textarea.value = codeQuote + '\n' + text.trim() + '\n' + codeQuote;
        }
    });
});
