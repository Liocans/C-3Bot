import re

def stem(word):
    # Define a regular expression to match a vowel
    vowel_pattern = re.compile(r'[aeiou]')

    # Define the Porter stemming rules
    step1a_suffixes = [('sses', 'ss'), ('ies', 'i'), ('ss', 'ss'), ('s', '')]
    
    step1b_suffixes = [('eed', 'ee'), ('ed', ''), ('ing', '')]
    
    step2_suffixes = [
        ('ational', 'ate'), ('tional', 'tion'), ('enci', 'ence'), ('anci', 'ance'),
        ('izer', 'ize'), ('bli', 'ble'), ('alli', 'al'), ('entli', 'ent'), ('eli', 'e'),
        ('ousli', 'ous'), ('ization', 'ize'), ('ation', 'ate'), ('ator', 'ate'), ('alism', 'al'),
        ('iveness', 'ive'), ('fulness', 'ful'), ('ousness', 'ous'), ('aliti', 'al'), ('iviti', 'ive'),
        ('biliti', 'ble'), ('logi', 'log')
    ]
    step3_suffixes = [
        ('icate', 'ic'), ('ative', ''), ('alize', 'al'), ('iciti', 'ic'), ('ical', 'ic'),
        ('ful', ''), ('ness', '')
    ]
    step4_suffixes = [
        ('al', ''), ('ance', ''), ('ence', ''), ('er', ''), ('ic', ''), ('able', ''),
        ('ible', ''), ('ant', ''), ('ement', ''), ('ment', ''), ('ent', ''), ('ou', ''),
        ('ism', ''), ('ate', ''), ('iti', ''), ('ous', ''), ('ive', ''), ('ize', '')
    ]

    # Apply the Porter stemming algorithm
    # Step 1a
    for suffix in step1a_suffixes:
        if word.endswith(suffix):
            return word[:-len(suffix)]
    
    # Step 1b
    for suffix, replacement in step1b_suffixes:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if vowel_pattern.search(stem):
                return stem + replacement
    
    # Step 2
    for suffix, replacement in step2_suffixes:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if measure(stem) > 0:
                return stem + replacement
    
    # Step 3
    for suffix, replacement in step3_suffixes:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if measure(stem) > 0:
                return stem + replacement
    
    # Step 4
    for suffix, replacement in step4_suffixes:
        if word.endswith(suffix):
            stem = word[:-len(suffix)]
            if measure(stem) > 1:
                return stem + replacement
    
    return word

def measure(word):
    # Compute the "measure" of a word (the number of consonant sequences)
    consonant_pattern = re.compile(r'[^aeiou]')
    word = re.sub(r'^[^aeiou]+', '', word)
    word = re.sub(r'[^aeiou]+$', '', word)
    return len(consonant_pattern.findall(word))

# Example usage:
word = "relational"
print(measure(word))
stemmed_word = stem(word)
print("Original word:", word)
print("Stemmed word:", stemmed_word)
