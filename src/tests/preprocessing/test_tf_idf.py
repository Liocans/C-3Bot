import math
import unittest

import numpy as np

from modules.NLP.features_extractor.tf_idf import TFIDF
from modules.NLP.preprocessing.preprocessor import Preprocessor

class TestTFIDF(unittest.TestCase):
    def setUp(self):
        # Mock preprocessor setup
        self.preprocessor = Preprocessor()
        self.vocab = ['the', 'premiere', 'outside', 'i', 'go', 'not', 'watch', 'it', 'season', 'today', 'be', 'to', 'rain']
        # Simulating preprocessed documents
        self.docs = [
            self.preprocessor.preprocess_text('It is going to rain today'),
            self.preprocessor.preprocess_text('Today I am not going outside'),
            self.preprocessor.preprocess_text('I am going to watch the season premiere')
        ]
        self.tfidf = TFIDF(self.preprocessor, self.vocab, self.docs)

    def test_feature_extraction(self):
        sentence = "It is going to rain today"
        expected_vector = np.zeros(len(self.vocab)).tolist()
        # Compute expected TF-IDF values manually here for 'sample', 'test', 'tfidf'
        # Example calculation (these will need to be accurate based on actual preprocessing)
        expected_vector[0] = 0  # TF * IDF for 'the'
        expected_vector[1] = 0  # TF * IDF for 'premiere'
        expected_vector[2] = 0  # TF * IDF for 'outside'
        expected_vector[3] = 0  # TF * IDF for 'i'
        expected_vector[4] = (1 / 6) * math.log(3 / (1 + 3))  # TF * IDF for 'go'
        expected_vector[5] = 0  # TF * IDF for 'not'
        expected_vector[6] = 0  # TF * IDF for 'watch'
        expected_vector[7] = (1 / 6) * math.log(3 / (1 + 1))  # TF * IDF for 'it'
        expected_vector[8] = 0  # TF * IDF for 'season'
        expected_vector[9] = (1 / 6) * math.log(3 / (1 + 2))  # TF * IDF for 'today'
        expected_vector[10] = (1 / 6) * math.log(3 / (1 + 3))  # TF * IDF for 'be'
        expected_vector[11] = (1 / 6) * math.log(3 / (1 + 2))  # TF * IDF for 'to'
        expected_vector[12] = (1 / 6) * math.log(3 / (1 + 1))  # TF * IDF for 'rain'
        np.testing.assert_array_almost_equal(self.tfidf.extract_features(sentence), expected_vector)


if __name__ == '__main__':
    unittest.main()
