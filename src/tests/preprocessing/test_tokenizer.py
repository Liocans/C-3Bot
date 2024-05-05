import unittest

from modules.NLP.preprocessing.tokenizer import Tokenizer


class TestTokenizer(unittest.TestCase):

    def setUp(self):
        # Initialize the tokenizer_without_stopwords
        self.tokenizer_without_stopwords = Tokenizer()
        self.tokenizer_with_stopwords = Tokenizer(remove_stopwords=False)

    def test_remove_punctuation(self):
        # Test punctuation removal
        input = "Hello, world! How are you?"
        expected_output = "Hello world How are you"
        actual_output = self.tokenizer_without_stopwords._Tokenizer__remove_punctuation(sentence=input)
        self.assertEqual(actual_output, expected_output)

    def test_tokenize(self):
        # Test tokenization
        input = "Hello"
        expected_output = ["hello"]
        actual_output = self.tokenizer_without_stopwords._Tokenizer__tokenize(sentence=input)
        self.assertEqual(actual_output, expected_output)

    def test_remove_stop_words(self):
        # Test stop word removal
        input = ["hello", "world", "how", "are", "you"]
        expected_output = ['hello', 'world', 'how', 'you']
        actual_output = self.tokenizer_without_stopwords._Tokenizer__remove_stop_words(tokens=input)
        self.assertEqual(actual_output, expected_output)

    def test_tokenize_sentence_without_stop_words(self):
        # Test full tokenization process
        input = "Hello, world! How are you?"
        expected_output = ['hello', 'world', 'how', 'you']
        actual_output = self.tokenizer_without_stopwords.tokenize_and_filter_sentence(sentence=input)
        self.assertEqual(actual_output, expected_output)

    def test_tokenize_sentence_with_stop_words(self):
        # Test full tokenization process
        input = "Hello, world! How are you?"
        expected_output = ['hello', 'world', 'how', 'are', 'you']
        actual_output = self.tokenizer_with_stopwords.tokenize_and_filter_sentence(sentence=input)
        self.assertEqual(actual_output, expected_output)

        
if __name__ == '__main__':
    unittest.main()