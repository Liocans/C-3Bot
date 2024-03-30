import unittest

from parser.language_parser import LanguageParser
from utilities.file_searcher import PathFinder


class TestJavaParser(unittest.TestCase):

    def setUp(self):
        self.language_parser = LanguageParser()

    def test_missings(self):
        filename = PathFinder().get_complet_path('ressources/java_files/code_with_missings.txt')
        expected_output = ({(3, 1), (11, 25), (14, 28)}, {(5, 20, ';')})
        with open(filename, "r") as file:
            actual_output = self.language_parser.find_syntax_problem(file.read(), "java")
        self.assertEqual(expected_output , actual_output)

    def test_errors(self):
        filename = PathFinder().get_complet_path('ressources/java_files/code_with_errors.txt')
        expected_output = (set(), {(37, 2, '}')})
        with open(filename, "r") as file:
            actual_output = self.language_parser.find_syntax_problem(file.read(), "java")
        self.assertEqual(expected_output, actual_output)

    def test_no_errors(self):
        filename = PathFinder().get_complet_path('ressources/java_files/code_without_errors.txt')
        expected_output = (set(), set())
        with open(filename, "r") as file:
            actual_output = self.language_parser.find_syntax_problem(file.read(), "java")
        self.assertEqual(expected_output, actual_output)

if __name__ == '__main__':
    unittest.main()
