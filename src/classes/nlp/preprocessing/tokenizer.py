import re
import string
import os

class Tokenizer:
    def __init__(self, language = "english", mode = ""):
        self.language = language
        self.stop_words = self.load_stop_words()
        self.mode = mode

    def tokenize_and_filter_sentence(self, sentence):
        sentence = self.remove_punctuation(sentence)
        tokens = self.tokenize(sentence)
        if self.mode == "S":    
            tokens = self.remove_stop_words(tokens)
        return tokens

    def load_stop_words(self):
        stop_words = set()
        filename = os.path.abspath(f'ressources/stop_words/{self.language}.txt')

        with open(filename, 'r', encoding='utf-8') as file:
            for line in file:
                stop_words.add(line.strip())
        return stop_words

    def tokenize(self, sentence):
        pattern = r'\w+|\$[\d\.]+|\S+'
        tokens = re.findall(pattern, sentence.lower())
        return tokens

    def remove_stop_words(self, tokens):
        filtered_words = [word for word in tokens if word not in self.stop_words]
        return filtered_words

    def remove_punctuation(self, sentence):
        translator = str.maketrans('', '', string.punctuation)
        return sentence.translate(translator)