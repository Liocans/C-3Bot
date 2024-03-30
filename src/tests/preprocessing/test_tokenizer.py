import unittest

from NLP.preprocessing.tokenizer import Tokenizer

class TestTokenizer(unittest.TestCase):

    def setUp(self):
        # Initialize the tokenizer
        self.tokenizer = Tokenizer()

    def test_remove_punctuation(self):
        # Test punctuation removal
        input = "Hello, world! How are you?"
        expected_output = "Hello world How are you"
        actual_output = self.tokenizer._Tokenizer__remove_punctuation(sentence=input)
        self.assertEqual(expected_output, actual_output)

    def test_tokenize(self):
        # Test tokenization
        input = "Hello world. How are you?"
        expected_output = ["hello", "world", ".", "how", "are", "you", "?"]
        actual_output = self.tokenizer._Tokenizer__tokenize(sentence=input)
        self.assertEqual(expected_output, actual_output)

    def test_remove_stop_words(self):
        # Test stop word removal
        input = ["hello", "world", "how", "are", "you"]
        expected_output = ['hello', 'world', 'how', 'you']
        actual_output = self.tokenizer._Tokenizer__remove_stop_words(tokens=input)
        self.assertEqual(expected_output, actual_output)

    def test_tokenize_sentence_without_stop_words(self):
        # Test full tokenization process
        input = "Hello, world! How are you?"
        expected_output = ['hello', 'world', 'how', 'are', 'you']
        actual_output = self.tokenizer.tokenize_and_filter_sentence(sentence=input)
        self.assertEqual(expected_output, actual_output)

    def test_tokenize_sentence_with_stop_words(self):
        # Test full tokenization process
        input = "Hello, world! How are you?"
        expected_output = ['hello', 'world', 'how', 'you']
        actual_output = self.tokenizer.tokenize_and_filter_sentence(sentence=input, exclude_stopwords=False)
        self.assertEqual(expected_output, actual_output)
        
if __name__ == '__main__':
    unittest.main()