import unittest

from classes.preprocessing.tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):

    def setUp(self):
        # Initialize the tokenizer
        self.tokenizer = Tokenizer(mode="S")

    def test_remove_punctuation(self):
        # Test punctuation removal
        text = "Hello, world! How are you?"
        expected_text = "Hello world How are you"
        processed_text = self.tokenizer.remove_punctuation(text)
        self.assertEqual(processed_text, expected_text)

    def test_tokenize(self):
        # Test tokenization
        text = "Hello world. How are you?"
        expected_tokens = ["hello", "world", ".", "how", "are", "you", "?"]
        tokens = self.tokenizer.tokenize(text)
        self.assertEqual(tokens, expected_tokens)

    def test_remove_stop_words(self):
        # Test stop word removal
        tokens = ["hello", "world", "how", "are", "you"]
        expected_tokens = ["hello", "world"]
        filtered_tokens = self.tokenizer.remove_stop_words(tokens)
        self.assertEqual(filtered_tokens, expected_tokens)

    def test_tokenize_sentence(self):
        # Test full tokenization process
        sentence = "Hello, world! How are you?"
        expected_tokens = ["hello", "world"]
        tokens = self.tokenizer.tokenize_and_filter_sentence(sentence)
        self.assertEqual(tokens, expected_tokens)
        
if __name__ == '__main__':
    unittest.main()