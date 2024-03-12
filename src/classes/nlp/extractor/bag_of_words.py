import sys
import os
import json
import numpy as np
sys.path.append(os.path.abspath('classes/nlp/preprocessing'))

from lemmatizer import Lemmatizer
from stemmer import Stemmer
from tokenizer import Tokenizer

class BagOfWords:
    def __init__(self, mode="L"):
        self.stemmer = Stemmer()
        self.lemmatizer = Lemmatizer()
        self.tokenizer = Tokenizer()
        self.mode = mode
        self.vocab = []
        self.bow_representation = None
        self.load_corpus()
        
    def load_corpus(self):
        filename = os.path.abspath(f'ressources/intents/intents.json')
        # Load intents data from JSON file
        intents_data = None
        with open(filename, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)
            
        for intent in intents_data["intents"]:
            for text in intent["texts"]:
                for word in self.preprocess_text(text):                            
                    if word not in self.vocab:
                        self.vocab.append(word)
        print(self.vocab)
                            
    def generate_bow(self, sentence):
        self.bow_representation = np.zeros(len(self.vocab))
        for word in self.preprocess_text(sentence):
            if word in self.vocab:
                index = self.vocab.index(word)
                self.bow_representation[index] += 1
        return self.bow_representation
        
    def preprocess_text(self, text):
        tokens = self.tokenizer.tokenize_and_filter_sentence(text)  # Tokenize and convert to lowercase
        return self.lemmatizer.lemmatize(tokens) if self.mode == "L" else self.stemmer.stem_words(tokens)
    
if __name__ == "__main__":
    # Initialize BagOfWords instance
    bow = BagOfWords(mode="L")  # Use lemmatization mode

    # Define a sample sentence
    sentence = "How are you doing today?"

    # Generate Bag of Words representation for the sample sentence
    bow_representation = bow.generate_bow(sentence)

    # Print the generated Bag of Words representation
    print("Bag of Words representation:")
    print(bow_representation)
