#https://tartarus.org/martin/PorterStemmer/index.html

class Stemmer():
    
    def __init__(self, language = "english"):
        self.language = language
        self.vowels = [*"aeiou"]
        self.consonants = [*"bcdfghjklmnpqrstwxz"]
        self.is_step_1_2b = False
        self.step1a_suffixes = [('sses', 'ss'), ('ies', 'i'), ('ss', 'ss'), ('s', '')]
        self.step1b_suffixes = [('eed', 'ee'), ('ed', ''), ('ing', '')]
        self.step1_2b_suffixes = [('at', 'ate'), ('bl','ble'), ('iz', 'ize')]
        self.step1c_suffixes = [('y','i')]
        self.step2_suffixes = [
            ('ational', 'ate'), ('tional', 'tion'), ('enci', 'ence'), ('anci', 'ance'),
            ('izer', 'ize'), ('bli', 'ble'), ('alli', 'al'), ('entli', 'ent'), ('eli', 'e'),
            ('ousli', 'ous'), ('ization', 'ize'), ('ation', 'ate'), ('ator', 'ate'), ('alism', 'al'),
            ('iveness', 'ive'), ('fulness', 'ful'), ('ousness', 'ous'), ('aliti', 'al'), ('iviti', 'ive'),
            ('biliti', 'ble'), ('logi', 'log')
        ]
        self.step3_suffixes = [
            ('icate', 'ic'), ('ative', ''), ('alize', 'al'), ('iciti', 'ic'), ('ical', 'ic'),
            ('ful', ''), ('ness', '')
        ]
        self.step4_suffixes = [
            ('al', ''), ('ance', ''), ('ence', ''), ('er', ''), ('ic', ''), ('able', ''),
            ('ible', ''), ('ant', ''), ('ement', ''), ('ment', ''), ('ent', ''), ('ou', ''), 
            ('tion','t'), ('sion', 's'), ('ism', ''), ('ate', ''), ('iti', ''), ('ous', ''), 
            ('ive', ''), ('ize', '') 
        ]
        
        self.step5a_suffixes = [('e','')]
        
        self.step5b_suffixes = [('l','')]
    
    def stem_words(self, tokens):
        stem_sentence = []
        for word in tokens:
            stem_sentence.append(self.stem_word(word))
        return stem_sentence
    
    def stem_word(self, word):
        stem = self.step_1(word)
        stem = self.step_2(stem)
        stem = self.step_3(stem)
        stem = self.step_4(stem)
        stem = self.step_5(stem)
        return stem
    
    def determine_class(self, char):
        if(char in self.vowels):
            return "V"
        return "C"
    
    def divide_into_class(self, word):
        classes = []
        for char in word:
            classfication = self.determine_class(char)
            if len(classes) == 0 or classes[-1] != classfication:
                classes.append(classfication)
        return classes
    
    def determine_m(self, word):
        classes = self.divide_into_class(word)
        if len(classes) < 2:
            return 0
        if classes[0] == 'C':
            classes = classes[1:]
        if classes[-1] == 'V':
            classes = classes[:len(classes)-1]
        m = len(classes)//2 if (len(classes)/2) >= 1 else 0
        return m
    
    #stem ends with S (or other letters, such as L, T…)
    def _chk_s(self, word, lt):
        for letter in lt:
            if word.endswith(letter):
                return True
        return False
    
    #stem contains a vowel.
    def contains_vowel(self, word):
        if(len(word) > 1):
            for letter in word[1:-1]:
                if letter in self.vowels:
                    return True
            return False

    #stem ends with a double consonant of any type.
    def end_with_double_consonant(self, word):
        if len(word) >= 2 and word[-1] in self.consonants and word[-2] in self.consonants:
            return True
        return False
    
    #stem ends with cvc (consonant followed by vowel followed by consonant) 
    #where second consonant is not W, X or Y (see, weird y again!)
    def end_with_cvc(self, word):
        if (len(word) >= 3 and word[-3] in self.consonants) and (word[-2] in self.vowels) and (word[-1] in self.consonants) and (word[-1] not in "wxy"):
            return True
        else:
            return False
    
    
    # Deal with Plurals and Past Participles
    def step_1(self, word):
        stem = self.step_1_a(word)
        stem = self.step_1_b(stem)
        stem = self.step_1_c(stem)
        return stem
    
    def step_1_a(self, word):
        for suffix in self.step1a_suffixes:
            if word.endswith(suffix[0]):
                return word[:-len(suffix[0])] + suffix[1]
        return word
    
    def step_1_b(self, word):

        if(word.endswith(self.step1b_suffixes[0][0]) and self.determine_m(word[:-len(self.step1b_suffixes[0][0])]) > 0):
            return word[:-len(self.step1b_suffixes[0][0])] + self.step1b_suffixes[0][1]
            
        if (word.endswith(self.step1b_suffixes[1][0]) and self.contains_vowel(word[:-len(self.step1b_suffixes[1][0])])):
            return self.step_1_2b(word[:-len(self.step1b_suffixes[1][0])] + self.step1b_suffixes[1][1])
             
        if (word.endswith(self.step1b_suffixes[2][0]) and self.contains_vowel(word[:-len(self.step1b_suffixes[2][0])])):
            return self.step_1_2b(word[:-len(self.step1b_suffixes[2][0])] + self.step1b_suffixes[2][1])
            
        return word
    
    def step_1_2b(self, word):
        
        for suffix in self.step1_2b_suffixes:
            if word.endswith(suffix[0]):
                return word[:-len(suffix[0])] + suffix[1]
            
        if(not word.endswith('s') and not word.endswith('z') and not word.endswith('l') and self.end_with_double_consonant(word)):
            return word[:-1]
        
        if(self.determine_m(word) == 1 and self.end_with_cvc(word)):
            return word + "e"
        
        return word
    
    def step_1_c(self, word):
        for suffix in self.step1c_suffixes:
            if (word.endswith(suffix[0]) and self.contains_vowel(word[:-len(suffix[0])])):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def step_2(self, word):
        for suffix in self.step2_suffixes:
            if (word.endswith(suffix[0]) and self.determine_m(word[:-len(suffix[0])]) > 0):
                return word[:-len(suffix[0])] + suffix[1]
        return word
    
    def step_3(self, word):
        for suffix in self.step3_suffixes:
            if (word.endswith(suffix[0]) and self.determine_m(word[:-len(suffix[0])]) > 0 ):
                return word[:-len(suffix[0])] + suffix[1]
        return word
    
    def step_4(self, word):
        for suffix in self.step4_suffixes:
            if (word.endswith(suffix[0]) and self.determine_m(word[:-len(suffix[0])]) > 1):
                return word[:-len(suffix[0])] + suffix[1]
        return word
    
    def step_5(self, word):
        stem = self.step_5_a(word)
        stem = self.step_5_b(stem)
        return stem
        
    def step_5_a(self, word):
        for suffix in self.step5a_suffixes:
            if self.determine_m(word[:-len(suffix[0])]) > 1 and word.endswith(suffix[0]):
                return word[:-len(suffix[0])] + suffix[1]
                
        for suffix in self.step5a_suffixes:
            if (word.endswith(suffix[0]) and self.determine_m(word[:-len(suffix[0])]) == 1 and not self.end_with_cvc(word[:-len(suffix[0])])):
                return word[:-len(suffix[0])] + suffix[1]
            
        return word
        
    def step_5_b(self, word):
        for suffix in self.step5b_suffixes:
            if (word.endswith(suffix[0]) and self.determine_m(word) > 1 and self.end_with_double_consonant(word)):
                return word[:-len(suffix[0])] + suffix[1]
        return word