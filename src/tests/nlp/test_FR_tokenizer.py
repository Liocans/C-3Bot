import unittest
import sys
import os
sys.path.append(os.path.abspath('classes/nlp'))

from tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):
    def setUp(self):
        # Initialize the tokenizer
        self.tokenizer = Tokenizer(language='french')

    def test_remove_punctuation(self):
        # Test punctuation removal
        text = "Bonjour, tout le monde! Comment ça va?"
        expected_text = "Bonjour tout le monde Comment ça va"
        processed_text = self.tokenizer.remove_punctuation(text)
        self.assertEqual(processed_text, expected_text)

    def test_tokenize(self):
        # Test tokenization
        text = "Bonjour tout le monde. Comment ça va?"
        expected_tokens = ["bonjour", "tout", "le", "monde", ".", "comment", "ça", "va", "?"]
        tokens = self.tokenizer.tokenize(text)
        self.assertEqual(tokens, expected_tokens)

    def test_remove_stop_words(self):
        # Test stop word removal
        tokens = ["bonjour", "tout", "le", "monde", "comment", "ça", "va"]
        expected_tokens = ["bonjour", "tout", "monde", "comment", "ça", "va"]
        filtered_tokens = self.tokenizer.remove_stop_words(tokens)
        self.assertEqual(filtered_tokens, expected_tokens)

    def test_tokenize_sentence(self):
        # Test full tokenization process
        sentence = "Bonjour, tout le monde! Comment ça va?"
        expected_tokens = ["bonjour", "tout", "monde", "comment", "ça", "va"]
        tokens = self.tokenizer.tokenize_sentence(sentence)
        self.assertEqual(tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()
