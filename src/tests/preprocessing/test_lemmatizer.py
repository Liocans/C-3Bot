import unittest

from NLP.preprocessing.lemmatizer import Lemmatizer


class TestLemmatizer(unittest.TestCase):
    
    def setUp(self):
        self.lemmatizer = Lemmatizer()
    
    def test_lemmatize_passage(self):
        # Test case with a simple sentence
        input = ['The', 'cats', 'are', 'chasing', 'mice']
        expected_output = ["The", "cat", "be", "chase", "mouse"]
        actual_output = self.lemmatizer.lemmatize(input)
        self.assertEqual(expected_output, actual_output)

        # Test case with a more complex sentence
        input = ['He', 'is', 'running', 'quickly', 'to', 'catch', 'the', 'fast', 'train']
        expected_output = ["He", "be", "run", "quickly", "to", "catch", "the", "fast", "train"]
        actual_output = self.lemmatizer.lemmatize(input)
        self.assertEqual(expected_output, actual_output)

        # Test case with empty string
        input = ["cats"]
        expected_output = ["cat"]
        actual_output = self.lemmatizer.lemmatize(input)
        self.assertEqual(expected_output, actual_output)
        

if __name__ == '__main__':
    unittest.main()
