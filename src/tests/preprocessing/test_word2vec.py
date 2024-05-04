import unittest

from modules.NLP.features_extractor.word2vec import Word2Vec
from modules.NLP.preprocessing.preprocessor import Preprocessor


class TestWord2Vec(unittest.TestCase):

    def setUp(self):
        # Create a mock preprocessor that just lowercases and tokenizes on spaces
        self.preprocessor = Preprocessor()
        # Create a Word2Vec instance with the mocked preprocessor
        self.vocab = ['the', 'premiere', 'outside', 'i', 'go', 'not', 'watch', 'it', 'season', 'today', 'be', 'to',
                      'rain']
        # Simulating preprocessed documents
        self.docs = [
            self.preprocessor.preprocess_text('It is going to rain today'),
            self.preprocessor.preprocess_text('Today I am not going outside'),
            self.preprocessor.preprocess_text('I am going to watch the season premiere')
        ]

        self.word2vec = Word2Vec(self.preprocessor, vocab=self.vocab, docs=self.docs)

    def test_extract_features_single_known_word(self):
        sentence = "rain"
        expected_vector = [1.0, 2.0]
        result_vector = self.word2vec.extract_features(sentence)
        self.assertEqual(result_vector, expected_vector)

    def test_extract_features_multiple_known_words(self):
        sentence = "It is raining"
        expected_vector = [2.0, 3.0]
        result_vector = self.word2vec.extract_features(sentence)
        self.assertEqual(result_vector, expected_vector)

    def test_extract_features_no_known_words(self):
        sentence = "goodbye"
        expected_vector = [0.0, 0.0]  # No known words results in a zero vector
        result_vector = self.word2vec.extract_features(sentence)
        self.assertEqual(result_vector, expected_vector)

    def test_extract_features_empty_sentence(self):
        sentence = ""
        expected_vector = [0.0, 0.0]  # Empty sentence should also result in a zero vector
        result_vector = self.word2vec.extract_features(sentence)
        self.assertEqual(result_vector, expected_vector)


if __name__ == '__main__':
    unittest.main()
