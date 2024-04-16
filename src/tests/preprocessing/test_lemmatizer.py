import unittest

from modules.NLP.preprocessing.lemmatizer import Lemmatizer


class TestLemmatizer(unittest.TestCase):
    """
    A test suite for testing the Lemmatizer class functionality.

    This class includes setup procedures and multiple test cases to ensure the
    Lemmatizer class correctly lemmatizes input tokens into their base or dictionary form.
    """

    def setUp(self):
        """
        Setup method to initialize a Lemmatizer instance before each test method.

        This method is called before every individual test function, ensuring that
        each test is run with a fresh instance of the Lemmatizer.
        """
        self.lemmatizer = Lemmatizer()
    
    def test_lemmatize_passage(self):
        """
        Tests the lemmatization functionality of the Lemmatizer with various inputs.

        This test includes three cases:
        - A simple sentence to verify basic lemmatization.
        - A more complex sentence to test lemmatization with different parts of speech.
        - A single word to test lemmatization functionality on individual tokens.

        Each case verifies that the actual output from the Lemmatizer matches the expected output.
        """

        # Test case with a simple sentence
        input = ['The', 'cats', 'are', 'chasing', 'mice']
        expected_output = ["The", "cat", "be", "chase", "mouse"]
        actual_output = self.lemmatizer.preprocess_text(tokens=input)
        self.assertEqual(expected_output, actual_output)

        # Test case with a more complex sentence
        input = ['He', 'is', 'running', 'quickly', 'to', 'catch', 'the', 'fast', 'train']
        expected_output = ["He", "be", "run", "quickly", "to", "catch", "the", "fast", "train"]
        actual_output = self.lemmatizer.preprocess_text(tokens=input)
        self.assertEqual(expected_output, actual_output)

        # Test case with empty string
        input = ["cats"]
        expected_output = ["cat"]
        actual_output = self.lemmatizer.preprocess_text(tokens=input)
        self.assertEqual(expected_output, actual_output)
        

if __name__ == '__main__':
    unittest.main()
