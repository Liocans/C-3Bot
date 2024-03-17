import nltk
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag

nltk.download('punkt', quiet=True)
nltk.download('wordnet', quiet=True)


class Lemmatizer:

    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()

    def get_wordnet_pos(self, tag):
        if tag.startswith('J'):
            return wordnet.ADJ
        elif tag.startswith('V'):
            return wordnet.VERB
        elif tag.startswith('N'):
            return wordnet.NOUN
        elif tag.startswith('R'):
            return wordnet.ADV
        else:
            return wordnet.NOUN

    def lemmatize(self, tokens):
        pos_tags = pos_tag(tokens)
        lemmatized_words = [self.lemmatizer.lemmatize(word, self.get_wordnet_pos(tag)) for word, tag in pos_tags]
        return lemmatized_words
