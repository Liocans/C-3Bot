import unittest

from NLP.preprocessing.sentence_segmenter import SentenceSegmenter

class TestSentenceSegmenter(unittest.TestCase):
    def setUp(self):
        self.segmenter = SentenceSegmenter()

    def test_simple_sentences(self):
        input = "This is a sentence. Here is another one."
        expected_output = ["This is a sentence.", "Here is another one."]
        actual_output = self.segmenter.segment_sentences(text=input)
        self.assertEqual(expected_output, actual_output)

    def test_with_question_and_exclamation(self):
        input = "What is your name? I'm John! Nice to meet you."
        expected_output = ["What is your name?", "I'm John!", "Nice to meet you."]
        actual_output = self.segmenter.segment_sentences(text=input)
        self.assertEqual(expected_output, actual_output)

    def test_with_abbreviation(self):
        input = "Dr. Smith is here. Please, call him."
        expected_output = ["Dr. Smith is here.", "Please, call him."]
        actual_output = self.segmenter.segment_sentences(text=input)
        self.assertEqual(expected_output, actual_output)

    def test_with_quotation_marks(self):
        input = '"Is it raining?" she asked. "Yes, it is," he replied.'
        expected_output = ['"Is it raining?" she asked.', '"Yes, it is," he replied.']
        actual_output = self.segmenter.segment_sentences(text=input)
        self.assertEqual(expected_output, actual_output)

    def test_with_no_punctuation(self):
        input = "This is a sentence without an end"
        expected_output = ["This is a sentence without an end"]
        actual_output = self.segmenter.segment_sentences(text=input)
        self.assertEqual(actual_output, expected_output)

    def test_empty_string(self):
        input = ""
        expected_output = [""]
        actual_output = self.segmenter.segment_sentences(text=input)
        self.assertEqual(actual_output, expected_output)

if __name__ == '__main__':
    unittest.main()
