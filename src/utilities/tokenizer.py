import re
import string
import os

def tokenizer(sentence):
    
    sentence = remove_punctuation(sentence)
    
    tokens = tokenize(sentence)
    
    tokens = remove_stop_words(tokens)
    
    return tokens

def load_stop_words(language):
    
    stop_words = set()  # Initialize an empty set to store stop words
    
    dirname = os.path.dirname(__file__)
    
    filename = os.path.join(dirname, f'../ressources/stop_words/{language}.txt')

    # Open the stop words file and read each line
    with open(filename, 'r', encoding='utf-8') as file:
        for line in file:
            stop_words.add(line.strip())  # Add each word to the set of stop words
    
    return stop_words

def tokenize(sentence):
    
    # Using regular expression to get rid of the multiple white space, \n,... 
    pattern = r'\w+|\$[\d\.]+|\S+'

    tokens = re.findall(pattern, sentence.lower())
    
    return tokens

def remove_stop_words(tokens):
    
    stop_words = load_stop_words('english') # Set of English stopwords
    
    filtered_words = [word for word in tokens if word.lower() not in stop_words]  # Remove stopwords
    
    return filtered_words 

def remove_punctuation(sentence):
    
    # Remove punctuation using string.punctuation
    
    translator = str.maketrans('', '', string.punctuation)
    
    return sentence.translate(translator)


# Example usage:
text = "This is a sample sentence. This is a sample sentence. It contains some numbers like 123 and $4.50."
tokens = tokenize(text)
print("Without punctuation: ", remove_punctuation(text))
print("When tokenize :", tokens)
print("Whitout Stop word: ", remove_stop_words(tokens))
print("Full tokenization: ", tokenizer(text))