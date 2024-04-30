import unittest

from modules.NLP.preprocessing.sentence_segmenter import segment_sentences
from utilities.path_finder import PathFinder


class TestSentenceSegmenter(unittest.TestCase):
    def setUp(self):
        pass

    def test_simple_sentences(self):
        input = "This is a sentence. Here is another one."
        expected_output = ["This is a sentence.", "Here is another one."]
        actual_output = segment_sentences(user_input=input)
        self.assertEqual(expected_output, actual_output["user_input"])

    def test_with_question_and_exclamation(self):
        input = "What is your name? I'm John! Nice to meet you."
        expected_output = ["What is your name?", "I'm John!", "Nice to meet you."]
        actual_output = segment_sentences(user_input=input)
        self.assertEqual(expected_output, actual_output["user_input"])

    def test_with_abbreviation(self):
        input = "Dr. Smith is here. Please, call him."
        expected_output = ["Dr. Smith is here.", "Please, call him."]
        actual_output = segment_sentences(user_input=input)
        self.assertEqual(expected_output, actual_output["user_input"])

    def test_with_quotation_marks(self):
        input = '"Is it raining?" she asked. "Yes, it is," he replied.'
        expected_output = ['"Is it raining?"', 'she asked.', '"Yes, it is," he replied.']
        actual_output = segment_sentences(user_input=input)
        self.assertEqual(expected_output, actual_output["user_input"])

    def test_with_no_punctuation(self):
        input = "This is a sentence without an end"
        expected_output = ["This is a sentence without an end"]
        actual_output = segment_sentences(user_input=input)
        self.assertEqual(expected_output, actual_output["user_input"])

    def test_with_newline(self):
        input = "This is a sentence\n without an end"
        expected_output = ["This is a sentence", "without an end"]
        actual_output = segment_sentences(user_input=input)
        self.assertEqual(expected_output, actual_output["user_input"])

    def test_empty_string(self):
        input = ""
        expected_output = []
        actual_output = segment_sentences(user_input=input)
        self.assertEqual(expected_output, actual_output["user_input"])

    def test_with_code(self):
        expected_output = "python"
        filename = PathFinder().get_complet_path(path_to_file='ressources/dialog_files/dialog_with_code.txt')
        with open(filename, "r") as file:
            actual_output = segment_sentences(user_input=file.read())
            self.assertEqual(expected_output, actual_output["language"])

    def test_with_code_without_language(self):
        expected_output = ""
        filename = PathFinder().get_complet_path(path_to_file='ressources/dialog_files/dialog_with_code_without_language.txt')
        with open(filename, "r") as file:
            actual_output = segment_sentences(user_input=file.read())
            self.assertEqual(expected_output, actual_output["language"])

if __name__ == '__main__':
    unittest.main()
