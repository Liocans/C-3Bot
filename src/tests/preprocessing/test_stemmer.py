import unittest

from modules.NLP.preprocessing.stemmer import Stemmer


class TestStemmer(unittest.TestCase):
    
    def setUp(self):
        self.stemmer = Stemmer()

    def test_divide_into_class(self):
        self.assertEqual(self.stemmer._Stemmer__divide_into_class(word="monkey"), ['C', 'V', 'C', 'V', 'C'])
        self.assertEqual(self.stemmer._Stemmer__divide_into_class(word="apparatus"), ['V', 'C', 'V', 'C', 'V', 'C', 'V', 'C'])
        self.assertEqual(self.stemmer._Stemmer__divide_into_class(word="eye"), ['V', 'C', 'V'])
        
        
    def test_determine_m(self):
        self.assertEqual(self.stemmer._Stemmer__determine_m(word="tree"), 0)
        self.assertEqual(self.stemmer._Stemmer__determine_m(word="by"), 0)
        self.assertEqual(self.stemmer._Stemmer__determine_m(word="trouble"), 1)
        self.assertEqual(self.stemmer._Stemmer__determine_m(word="oats"), 1)
        self.assertEqual(self.stemmer._Stemmer__determine_m(word="trees"), 1)
        self.assertEqual(self.stemmer._Stemmer__determine_m(word="ivy"), 1)
        self.assertEqual(self.stemmer._Stemmer__determine_m(word="troubles"), 2)
        self.assertEqual(self.stemmer._Stemmer__determine_m(word="private"), 2)
        self.assertEqual(self.stemmer._Stemmer__determine_m(word="oaten"), 2)

    def test_step_1_a(self):
        self.assertEqual(self.stemmer._Stemmer__step_1_a(word="caresses"), "caress")
        self.assertEqual(self.stemmer._Stemmer__step_1_a(word="ponies"), "poni")
        self.assertEqual(self.stemmer._Stemmer__step_1_a(word="ties"), "ti")

    def test_step_1_b(self):
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="feed"), "feed")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="agreed"), "agree")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="plastered"), "plaster")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="bled"), "bled")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="motoring"), "motor")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="sing"), "sing")

    def test_step_1_2b(self):
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="conflated"), "conflate")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="troubled"), "trouble")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="sized"), "size")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="hopping"), "hop")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="tanned"), "tan")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="falling"), "fall")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="hissing"), "hiss")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="fizzed"), "fizz")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="failing"), "fail")
        self.assertEqual(self.stemmer._Stemmer__step_1_b(word="filing"), "file")

    def test_step_1_c(self):
        self.assertEqual(self.stemmer._Stemmer__step_1_c(word="happy"), "happi")
        self.assertEqual(self.stemmer._Stemmer__step_1_c(word="sky"), "sky")

    def test_step_2(self):
        self.assertEqual(self.stemmer._Stemmer__step_2(word="relational"), "relate")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="conditional"), "condition")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="rational"), "rational")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="valenci"), "valence")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="hesitanci"), "hesitance")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="digitizer"), "digitize")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="conformabli"), "conformable")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="radicalli"), "radical")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="differentli"), "different")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="vileli"), "vile")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="analogousli"), "analogous")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="vietnamization"), "vietnamize")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="predication"), "predicate")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="operator"), "operate")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="feudalism"), "feudal")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="decisiveness"), "decisive")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="hopefulness"), "hopeful")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="callousness"), "callous")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="formaliti"), "formal")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="sensitiviti"), "sensitive")
        self.assertEqual(self.stemmer._Stemmer__step_2(word="sensibiliti"), "sensible")

    def test_step_3(self):
        self.assertEqual(self.stemmer._Stemmer__step_3(word="triplicate"), "triplic")
        self.assertEqual(self.stemmer._Stemmer__step_3(word="formative"), "form")
        self.assertEqual(self.stemmer._Stemmer__step_3(word="formalize"), "formal")
        self.assertEqual(self.stemmer._Stemmer__step_3(word="electriciti"), "electric")
        self.assertEqual(self.stemmer._Stemmer__step_3(word="electrical"), "electric")
        self.assertEqual(self.stemmer._Stemmer__step_3(word="hopeful"), "hope")
        self.assertEqual(self.stemmer._Stemmer__step_3(word="goodness"), "good")

    def test_step_4(self):
        self.assertEqual(self.stemmer._Stemmer__step_4(word="revival"), "reviv")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="allowance"), "allow")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="inference"), "infer")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="airliner"), "airlin")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="gyroscopic"), "gyroscop")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="adjustable"), "adjust")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="defensible"), "defens")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="irritant"), "irrit")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="replacement"), "replac")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="adjustment"), "adjust")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="dependent"), "depend")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="adoption"), "adopt")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="homologou"), "homolog")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="communism"), "commun")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="activate"), "activ")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="angulariti"), "angular")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="homologous"), "homolog")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="effective"), "effect")
        self.assertEqual(self.stemmer._Stemmer__step_4(word="bowdlerize"), "bowdler")

    def test_step_5_a(self):
        self.assertEqual(self.stemmer._Stemmer__step_5_a(word="probate"), "probat")
        self.assertEqual(self.stemmer._Stemmer__step_5_a(word="rate"), "rate")
        self.assertEqual(self.stemmer._Stemmer__step_5_a(word="cease"), "ceas")

    def test_step_5_a(self):
        self.assertEqual(self.stemmer._Stemmer__step_5_b(word="controll"), "control")
        self.assertEqual(self.stemmer._Stemmer__step_5_b(word="roll"), "roll")

if __name__ == '__main__':
    unittest.main()
