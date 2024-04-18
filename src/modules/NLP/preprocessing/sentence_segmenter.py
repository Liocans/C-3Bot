import re

def segment_sentences(user_input: str) -> dict:
    """
    Segments a string of user input into sentences, considering typical end-of-sentence punctuation,
    and also extracts any embedded code block and its language from the input.

    This function uses regex to identify sentence boundaries and then delegates to an internal
    function to extract any embedded code snippets and their respective programming language.

    Parameters:
        user_input (str): The user's input string potentially containing natural language text and
                          an embedded code block.

    Returns:
        dict: A dictionary containing the following keys:
              - 'language': The programming language of the embedded code block (if any).
              - 'code': The code block extracted from the input (if any).
              - 'user_input': A list of sentences segmented from the input, excluding the code block.
    """
    pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s')
    segmented_sentences = __extract_language_and_code(user_input=user_input)
    segmented_sentences["user_input"] = pattern.split(string=segmented_sentences["user_input"])
    segmented_sentences["user_input"] = [segment for segment in segmented_sentences["user_input"] if segment != '']
    return segmented_sentences

def __extract_language_and_code(user_input: str) -> dict:
    """
    Extracts the programming language and any enclosed code from a string based on markdown code block syntax.
    The function searches for text enclosed within triple backticks, captures the programming language if specified,
    and extracts the code, cleaning up the user input by removing the code block.

    Parameters:
        user_input (str): The complete string input potentially containing a markdown-like code block.

    Returns:
        dict: A dictionary containing:
              - 'language': A string representing the programming language specified in the code block (or None).
              - 'code': The string of the code extracted from the input (or None).
              - 'user_input': The modified input string after removing the code block.
    """
    pattern = r"```(.*?)\n(.*?)```"
    match = re.search(pattern, user_input, re.DOTALL)
    code = None
    language = None
    if match:
        language = match.group(1).strip()
        code = match.group(2).strip()
        start, end = match.span()
        # Extract text before and after the code block
        user_input = user_input[:start].strip()

    return {
        'language': language,
        'code': code,
        'user_input': user_input,
    }
