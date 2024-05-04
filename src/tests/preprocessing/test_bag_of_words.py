import unittest

from modules.NLP.features_extractor.bag_of_words import BagOfWords
from modules.NLP.preprocessing.preprocessor import Preprocessor


class TestBagOfWords(unittest.TestCase):
    def setUp(self):
        # Mock preprocessor setup
        self.preprocessor = Preprocessor()
        self.vocab = ['hello', 'world', 'test']
        self.bow = BagOfWords(self.preprocessor, self.vocab)

    def test_feature_extraction(self):
        sentence = "hello hello world"
        expected_vector = [2, 1, 0]  # Corresponding counts in the vocab
        self.assertEqual(self.bow.extract_features(sentence), expected_vector)

        # Test with non-vocab words
        sentence = "random words here"
        expected_vector = [0, 0, 0]
        self.assertEqual(self.bow.extract_features(sentence), expected_vector)

        # Test with empty string
        sentence = ""
        expected_vector = [0, 0, 0]
        self.assertEqual(self.bow.extract_features(sentence), expected_vector)


if __name__ == '__main__':
    unittest.main()
