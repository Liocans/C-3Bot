import re

def segment_sentences(user_input: str) -> dict:
    pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s')
    segmented_sentences = __extract_language_and_code(user_input=user_input)
    segmented_sentences["user_input"] = pattern.split(string=segmented_sentences["user_input"])
    return segmented_sentences

def __extract_language_and_code(user_input: str) -> dict:
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
