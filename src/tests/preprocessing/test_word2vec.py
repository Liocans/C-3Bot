import unittest
import numpy as np

from modules.NLP.features_extractor.word2vec import Word2Vec
from modules.NLP.preprocessing.preprocessor import Preprocessor


class TestWord2Vec(unittest.TestCase):

    def setUp(self):

        self.preprocessor = Preprocessor()
        self.docs = [
            self.preprocessor.preprocess_text('It is going to rain today'),
            self.preprocessor.preprocess_text('Today I am not going outside'),
            self.preprocessor.preprocess_text('I am going to watch the season premiere')
        ]

        self.word2vec = Word2Vec(self.preprocessor, docs=self.docs, vector_size=2)

    def test_extract_features_single_known_word(self):
        sentence = "rain"
        expected_vector = np.array([0.337885, 0.038143])
        result_vector = self.word2vec.extract_features(sentence)
        np.testing.assert_array_almost_equal(result_vector, expected_vector)

    def test_extract_features_multiple_known_words(self):
        sentence = "It is raining"
        expected_vector = np.array([0.303532, 0.106113])
        result_vector = self.word2vec.extract_features(sentence)
        np.testing.assert_array_almost_equal(result_vector, expected_vector)

    def test_extract_features_no_known_words(self):
        sentence = "goodbye"
        expected_vector = np.array([0.0, 0.0])
        result_vector = self.word2vec.extract_features(sentence)
        np.testing.assert_array_almost_equal(result_vector, expected_vector)

    def test_extract_features_empty_sentence(self):
        sentence = ""
        expected_vector = np.array([0.0, 0.0])
        result_vector = self.word2vec.extract_features(sentence)
        np.testing.assert_array_almost_equal(result_vector, expected_vector)


if __name__ == '__main__':
    unittest.main()
