$(document).ready(function() {
    document.getElementById('code_toggle').addEventListener('click', function() {
        const textarea = document.getElementById('message_text');
        const text = textarea.value;
        const codeQuote = '```';
        const languageRegex = /^```(\w+)?\s*\n[\s\n]*```$/; // Regex to match language and empty content between ```

        // Check if there's a selection
        const start = textarea.selectionStart;
        const end = textarea.selectionEnd;
        const selectedText = text.substring(start, end);

        if (start !== end) {
            if (selectedText.startsWith(codeQuote) && selectedText.endsWith(codeQuote)) {
                // Remove code block if it's just backticks with optional language and whitespace
                if (languageRegex.test(selectedText)) {
                    textarea.value = text.substring(0, start) + selectedText.slice(3, selectedText.lastIndexOf(codeQuote)).trim() + text.substring(end);
                } else {
                    textarea.value = text.substring(0, start) + selectedText.slice(3, selectedText.length - 3).trim() + text.substring(end);
                }
            } else {
                // Wrap the selection with codeQuote
                textarea.value = text.substring(0, start) + codeQuote + '\n' + selectedText.trim() + '\n' + codeQuote + text.substring(end);
            }
        } else {
            textarea.value = text + '\n' + codeQuote + '\n' + codeQuote;
        }
        // Update the cursor position
        textarea.setSelectionRange(start, end);
        textarea.dispatchEvent(new Event("input"));
    });
});
