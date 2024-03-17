import unittest

from NLP.preprocessing.stemmer import Stemmer


class TestStemmer(unittest.TestCase):
    
    def setUp(self):
        self.stemmer = Stemmer()

    def test_divide_into_class(self):
        self.assertEqual(self.stemmer.divide_into_class("monkey"), ['C', 'V', 'C', 'V', 'C'])
        self.assertEqual(self.stemmer.divide_into_class("apparatus"), ['V', 'C', 'V', 'C', 'V', 'C', 'V', 'C'])
        self.assertEqual(self.stemmer.divide_into_class("eye"), ['V', 'C', 'V'])
        
        
    def test_determine_m(self):
        self.assertEqual(self.stemmer.determine_m("tree"), 0)
        self.assertEqual(self.stemmer.determine_m("by"), 0)
        self.assertEqual(self.stemmer.determine_m("trouble"), 1)
        self.assertEqual(self.stemmer.determine_m("oats"), 1)
        self.assertEqual(self.stemmer.determine_m("trees"), 1)
        self.assertEqual(self.stemmer.determine_m("ivy"), 1)
        self.assertEqual(self.stemmer.determine_m("troubles"), 2)
        self.assertEqual(self.stemmer.determine_m("private"), 2)
        self.assertEqual(self.stemmer.determine_m("oaten"), 2)
    
    def test_step_1_a(self):
        self.assertEqual(self.stemmer.step_1_a("caresses"), "caress")
        self.assertEqual(self.stemmer.step_1_a("ponies"), "poni")
        self.assertEqual(self.stemmer.step_1_a("ties"), "ti")
        
    def test_step_1_b(self):
        self.assertEqual(self.stemmer.step_1_b("feed"), "feed")
        self.assertEqual(self.stemmer.step_1_b("agreed"), "agree")
        self.assertEqual(self.stemmer.step_1_b("plastered"), "plaster")
        self.assertEqual(self.stemmer.step_1_b("bled"), "bled")
        self.assertEqual(self.stemmer.step_1_b("motoring"), "motor")
        self.assertEqual(self.stemmer.step_1_b("sing"), "sing")
        
    def test_step_1_2b(self):
        self.assertEqual(self.stemmer.step_1_b("conflated"), "conflate")
        self.assertEqual(self.stemmer.step_1_b("troubled"), "trouble")
        self.assertEqual(self.stemmer.step_1_b("sized"), "size")
        self.assertEqual(self.stemmer.step_1_b("hopping"), "hop")
        self.assertEqual(self.stemmer.step_1_b("tanned"), "tan")
        self.assertEqual(self.stemmer.step_1_b("falling"), "fall")
        self.assertEqual(self.stemmer.step_1_b("hissing"), "hiss")
        self.assertEqual(self.stemmer.step_1_b("fizzed"), "fizz")
        self.assertEqual(self.stemmer.step_1_b("failing"), "fail")
        self.assertEqual(self.stemmer.step_1_b("filing"), "file")
        
    def test_step_1_c(self):
        self.assertEqual(self.stemmer.step_1_c("happy"), "happi")
        self.assertEqual(self.stemmer.step_1_c("sky"), "sky")
    
    def test_step_2(self):
        self.assertEqual(self.stemmer.step_2("relational"), "relate")
        self.assertEqual(self.stemmer.step_2("conditional"), "condition")
        self.assertEqual(self.stemmer.step_2("rational"), "rational")
        self.assertEqual(self.stemmer.step_2("valenci"), "valence")
        self.assertEqual(self.stemmer.step_2("hesitanci"), "hesitance")
        self.assertEqual(self.stemmer.step_2("digitizer"), "digitize")
        self.assertEqual(self.stemmer.step_2("conformabli"), "conformable")
        self.assertEqual(self.stemmer.step_2("radicalli"), "radical")
        self.assertEqual(self.stemmer.step_2("differentli"), "different")
        self.assertEqual(self.stemmer.step_2("vileli"), "vile")
        self.assertEqual(self.stemmer.step_2("analogousli"), "analogous")
        self.assertEqual(self.stemmer.step_2("vietnamization"), "vietnamize")
        self.assertEqual(self.stemmer.step_2("predication"), "predicate")
        self.assertEqual(self.stemmer.step_2("operator"), "operate")
        self.assertEqual(self.stemmer.step_2("feudalism"), "feudal")
        self.assertEqual(self.stemmer.step_2("decisiveness"), "decisive")
        self.assertEqual(self.stemmer.step_2("hopefulness"), "hopeful")
        self.assertEqual(self.stemmer.step_2("callousness"), "callous")
        self.assertEqual(self.stemmer.step_2("formaliti"), "formal")
        self.assertEqual(self.stemmer.step_2("sensitiviti"), "sensitive")
        self.assertEqual(self.stemmer.step_2("sensibiliti"), "sensible")
    
    def test_step_3(self):
        self.assertEqual(self.stemmer.step_3("triplicate"), "triplic")
        self.assertEqual(self.stemmer.step_3("formative"), "form")
        self.assertEqual(self.stemmer.step_3("formalize"), "formal")
        self.assertEqual(self.stemmer.step_3("electriciti"), "electric")
        self.assertEqual(self.stemmer.step_3("electrical"), "electric")
        self.assertEqual(self.stemmer.step_3("hopeful"), "hope")
        self.assertEqual(self.stemmer.step_3("goodness"), "good")
        
    def test_step_4(self):
        self.assertEqual(self.stemmer.step_4("revival"), "reviv")
        self.assertEqual(self.stemmer.step_4("allowance"), "allow")
        self.assertEqual(self.stemmer.step_4("inference"), "infer")
        self.assertEqual(self.stemmer.step_4("airliner"), "airlin")
        self.assertEqual(self.stemmer.step_4("gyroscopic"), "gyroscop")
        self.assertEqual(self.stemmer.step_4("adjustable"), "adjust")
        self.assertEqual(self.stemmer.step_4("defensible"), "defens")
        self.assertEqual(self.stemmer.step_4("irritant"), "irrit")
        self.assertEqual(self.stemmer.step_4("replacement"), "replac")
        self.assertEqual(self.stemmer.step_4("adjustment"), "adjust")
        self.assertEqual(self.stemmer.step_4("dependent"), "depend")
        self.assertEqual(self.stemmer.step_4("adoption"), "adopt")
        self.assertEqual(self.stemmer.step_4("homologou"), "homolog")
        self.assertEqual(self.stemmer.step_4("communism"), "commun")
        self.assertEqual(self.stemmer.step_4("activate"), "activ")
        self.assertEqual(self.stemmer.step_4("angulariti"), "angular")
        self.assertEqual(self.stemmer.step_4("homologous"), "homolog")
        self.assertEqual(self.stemmer.step_4("effective"), "effect")
        self.assertEqual(self.stemmer.step_4("bowdlerize"), "bowdler")
        
    def test_step_5_a(self):
        self.assertEqual(self.stemmer.step_5_a("probate"), "probat")
        self.assertEqual(self.stemmer.step_5_a("rate"), "rate")
        self.assertEqual(self.stemmer.step_5_a("cease"), "ceas")
        
    def test_step_5_a(self):
        self.assertEqual(self.stemmer.step_5_b("controll"), "control")
        self.assertEqual(self.stemmer.step_5_b("roll"), "roll")
        
if __name__ == '__main__':
    unittest.main()
