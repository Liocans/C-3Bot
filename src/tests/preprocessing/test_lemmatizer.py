import unittest

from classes.preprocessing.lemmatizer import Lemmatizer


class TestLemmatizer(unittest.TestCase):
    
    def setUp(self):
        self.lemmatizer = Lemmatizer()
    
    def test_lemmatize_passage(self):
        # Test case with a simple sentence
        words = ['The', 'cats', 'are', 'chasing', 'mice']
        expected_output = ["The", "cat", "be", "chase", "mouse"]
        self.assertEqual(self.lemmatizer.lemmatize(words), expected_output)

        # Test case with a more complex sentence
        words = ['He', 'is', 'running', 'quickly', 'to', 'catch', 'the', 'fast', 'train']
        expected_output = ["He", "be", "run", "quickly", "to", "catch", "the", "fast", "train"]
        self.assertEqual(self.lemmatizer.lemmatize(words), expected_output)

        # Test case with empty string
        words = ["cats"]
        expected_output = ["cat"]
        self.assertEqual(self.lemmatizer.lemmatize(words), expected_output)
        

if __name__ == '__main__':
    unittest.main()
