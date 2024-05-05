import unittest
import numpy as np

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
        expected_vector = np.array([2, 1, 0])  # Corresponding counts in the vocab
        np.testing.assert_array_almost_equal(self.bow.extract_features(sentence), expected_vector)

        # Test with non-vocab words
        sentence = "random words here"
        expected_vector = np.array([0, 0, 0])
        np.testing.assert_array_almost_equal(self.bow.extract_features(sentence), expected_vector)

        # Test with empty string
        sentence = ""
        expected_vector = np.array([0, 0, 0])
        np.testing.assert_array_almost_equal(self.bow.extract_features(sentence), expected_vector)


if __name__ == '__main__':
    unittest.main()
