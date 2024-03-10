import nltk
from nltk.stem import WordNetLemmatizer
nltk.download('averaged_perceptron_tagger')
from nltk.corpus import wordnet

class Lemmatizer():
    
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
    
    def lemmatize_words(self, tokens):
        lemmatized_sentence = []
        for word, tag in self.get_correct_tagger(tokens):
            if tag is None:
                lemmatized_sentence.append(word)
            else:        
                lemmatized_sentence.append(self.lemmatizer.lemmatize(word, tag))
        return lemmatized_sentence
    
    def lemmatize_word(self, token):
        tag = self.get_correct_tagger(token)
    
    
    def get_correct_tagger(self, tokens):
        return list(map(lambda x: (x[0], self.pos_tagged(x[1])), self.pos_tag(tokens)))
        
    def pos_tag(self, tokens):
        return nltk.pos_tag(tokens)
    
    def pos_tagger(nltk_tag):
        if nltk_tag.startswith('J'):
            return wordnet.ADJ
        elif nltk_tag.startswith('V'):
            return wordnet.VERB
        elif nltk_tag.startswith('N'):
            return wordnet.NOUN
        elif nltk_tag.startswith('R'):
            return wordnet.ADV
        else:          
            return None