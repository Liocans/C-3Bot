import unittest
from NLP.preprocessing.sentence_segmenter import SentenceSegmenter


class TestSentenceSegmenter(unittest.TestCase):
    def setUp(self):
        self.segmenter = SentenceSegmenter()

    def test_simple_sentences(self):
        text = "This is a sentence. Here is another one."
        expected = ["This is a sentence.", "Here is another one."]
        self.assertEqual(self.segmenter.segment_sentences(text), expected)

    def test_with_question_and_exclamation(self):
        text = "What is your name? I'm John! Nice to meet you."
        expected = ["What is your name?", "I'm John!", "Nice to meet you."]
        self.assertEqual(self.segmenter.segment_sentences(text), expected)

    def test_with_abbreviation(self):
        text = "Dr. Smith is here. Please, call him."
        expected = ["Dr. Smith is here.", "Please, call him."]
        self.assertEqual(self.segmenter.segment_sentences(text), expected)

    def test_with_quotation_marks(self):
        text = '"Is it raining?" she asked. "Yes, it is," he replied.'
        expected = ['"Is it raining?" she asked.', '"Yes, it is," he replied.']
        self.assertEqual(self.segmenter.segment_sentences(text), expected)

    def test_with_no_punctuation(self):
        text = "This is a sentence without an end"
        expected = ["This is a sentence without an end"]
        self.assertEqual(self.segmenter.segment_sentences(text), expected)

    def test_empty_string(self):
        text = ""
        expected = [""]
        self.assertEqual(self.segmenter.segment_sentences(text), expected)

if __name__ == '__main__':
    unittest.main()
