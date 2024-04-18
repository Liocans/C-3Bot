# https://tartarus.org/martin/PorterStemmer/index.html

class Stemmer:
    """
    Implements the Porter Stemming algorithm which is a process for removing the commoner morphological and 
    inflexional endings from words in English. Its main use is as part of a term normalisation process that is 
    usually done when setting up Information Retrieval systems.

    Attributes:
        __vowels (list): A list of vowel characters.
        __consonants (list): A list of consonant characters.
        __step1a_suffixes (list of tuples): Suffix rules for step 1a of the Porter Stemmer algorithm.
        __step1b_suffixes (list of tuples): Suffix rules for step 1b of the Porter Stemmer algorithm.
        __step1_2b_suffixes (list of tuples): Suffix rules for special cases in step 1b of the Porter Stemmer algorithm.
        __step1c_suffixes (list of tuples): Suffix rules for step 1c of the Porter Stemmer algorithm.
        __step2_suffixes (list of tuples): Suffix rules for step 2 of the Porter Stemmer algorithm.
        __step3_suffixes (list of tuples): Suffix rules for step 3 of the Porter Stemmer algorithm.
        __step4_suffixes (list of tuples): Suffix rules for step 4 of the Porter Stemmer algorithm.
        __step5a_suffixes (list of tuples): Suffix rules for step 5a of the Porter Stemmer algorithm.
        __step5b_suffixes (list of tuples): Suffix rules for step 5b of the Porter Stemmer algorithm.

    Methods:
        preprocess_text(tokens): Processes a list of word tokens and applies stemming to each token.
    """
    def __init__(self):
        """
        Initializes the Stemmer with predefined rules and character sets used in the Porter Stemming Algorithm.
        """
        self.__vowels = [*"aeiou"]
        self.__consonants = [*"bcdfghjklmnpqrstwxz"]
        self.__step1a_suffixes = [("sses", "ss"), ("ies", "i"), ("ss", "ss"), ("s", "")]
        self.__step1b_suffixes = [("eed", "ee"), ("ed", ""), ("ing", "")]
        self.__step1_2b_suffixes = [("at", "ate"), ("bl", "ble"), ("iz", "ize")]
        self.__step1c_suffixes = [("y", "i")]
        self.__step2_suffixes = [
            ("ational", "ate"), ("tional", "tion"), ("enci", "ence"), ("anci", "ance"),
            ("izer", "ize"), ("bli", "ble"), ("alli", "al"), ("entli", "ent"), ("eli", "e"),
            ("ousli", "ous"), ("ization", "ize"), ("ation", "ate"), ("ator", "ate"), ("alism", "al"),
            ("iveness", "ive"), ("fulness", "ful"), ("ousness", "ous"), ("aliti", "al"), ("iviti", "ive"),
            ("biliti", "ble"), ("logi", "log")
        ]
        self.__step3_suffixes = [
            ("icate", "ic"), ("ative", ""), ("alize", "al"), ("iciti", "ic"), ("ical", "ic"),
            ("ful", ""), ("ness", "")
        ]
        self.__step4_suffixes = [
            ("al", ""), ("ance", ""), ("ence", ""), ("er", ""), ("ic", ""), ("able", ""),
            ("ible", ""), ("ant", ""), ("ement", ""), ("ment", ""), ("ent", ""), ("ou", ""),
            ("tion", "t"), ("sion", "s"), ("ism", ""), ("ate", ""), ("iti", ""), ("ous", ""),
            ("ive", ""), ("ize", "")
        ]

        self.__step5a_suffixes = [("e", "")]

        self.__step5b_suffixes = [("l", "")]

    def preprocess_text(self, tokens: list) -> list:
        """
        Applies stemming to a list of word tokens based on the defined rules of the Porter Stemmer algorithm.

        Parameters:
            tokens (list): A list of word tokens to be stemmed.

        Returns:
            list: A list of stemmed word tokens.
        """
        stem_sentence = []
        for word in tokens:
            stem_sentence.append(self.__stem_word(word=word))
        return stem_sentence

    def __stem_word(self, word: str) -> str:
        """
        Stem a single word through sequential application of stemming rules from steps 1 to 5.

        Parameters:
            word (str): The word to be stemmed.

        Returns:
            str: The stemmed word.
        """
        stem = self.__step_1(word=word)
        stem = self.__step_2(word=stem)
        stem = self.__step_3(word=stem)
        stem = self.__step_4(word=stem)
        stem = self.__step_5(word=stem)
        return stem

    def __determine_class(self, char: str) -> str:
        """
        Determines if a character is a vowel or a consonant.

        Parameters:
            char (str): A single character.

        Returns:
            str: 'V' if the character is a vowel, 'C' otherwise.
        """
        if (char in self.__vowels):
            return "V"
        return "C"

    def __divide_into_class(self, word: str) -> list:
        """
        Divides a word into segments of vowels ('V') and consonants ('C').

        Parameters:
            word (str): The word to be divided.

        Returns:
            list: A list representing the sequence of character classes in the word.
        """
        classes = []
        for char in word:
            classfication = self.__determine_class(char=char)
            if len(classes) == 0 or classes[-1] != classfication:
                classes.append(classfication)
        return classes

    def __determine_m(self, word: str) -> int:
        """
        Calculates the 'm' value for a word, which is a key component in determining how many consonant sequences
        follow the first non-consonant (if any). This value is used in the Porter Algorithm to apply various
        stemming rules.

        Parameters:
            word (str): The word for which the 'm' value is calculated.

        Returns:
            int: The 'm' value, representing the count of 'VC' sequences in the word.
        """
        classes = self.__divide_into_class(word=word)
        if len(classes) < 2:
            return 0
        if classes[0] == "C":
            classes = classes[1:]
        if classes[-1] == "V":
            classes = classes[:len(classes) - 1]
        m = len(classes) // 2 if (len(classes) / 2) >= 1 else 0
        return m

    # stem contains a vowel.
    def __contains_vowel(self, word: str) -> bool:
        if (len(word) > 1):
            for letter in word[1:-1]:
                if letter in self.__vowels:
                    return True
            return False

    # stem ends with a double consonant of any type.
    def __end_with_double_consonant(self, word: str) -> bool:
        if len(word) >= 2 and word[-1] in self.__consonants and word[-2] in self.__consonants:
            return True
        return False

    # stem ends with cvc (consonant followed by vowel followed by consonant)
    # where second consonant is not W, X or Y (see, weird y again!)
    def __end_with_cvc(self, word: str) -> bool:
        if (len(word) >= 3 and word[-3] in self.__consonants) and (word[-2] in self.__vowels) and (
                word[-1] in self.__consonants) and (word[-1] not in "wxy"):
            return True
        else:
            return False

    # Deal with Plurals and Past Participles
    def __step_1(self, word: str) -> str:
        """
        Processes the first step of the Porter Stemming Algorithm, applying various suffix rules
        related to plurals and past participles.

        Parameters:
            word (str): The word to be processed.

        Returns:
            str: The modified word after applying step 1 rules.
        """
        stem = self.__step_1_a(word=word)
        stem = self.__step_1_b(word=stem)
        stem = self.__step_1_c(word=stem)
        return stem

    def __step_1_a(self, word: str) -> str:
        """
        Applies step 1a of the Porter Stemming Algorithm to remove common plural suffixes from a word.

        Parameters:
            word (str): The word to process.

        Returns:
            str: The word after removing plural suffixes.
        """
        for suffix in self.__step1a_suffixes:
            if word.endswith(suffix[0]):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def __step_1_b(self, word: str) -> str:
        """
        Applies step 1b of the Porter Stemming Algorithm, focusing on removing past tense and gerund forms.

        Parameters:
            word (str): The word to process.

        Returns:
            str: The word after processing past tense and gerund suffixes.
        """
        if (word.endswith(self.__step1b_suffixes[0][0]) and self.__determine_m(
                word=word[:-len(self.__step1b_suffixes[0][0])]) > 0):
            return word[:-len(self.__step1b_suffixes[0][0])] + self.__step1b_suffixes[0][1]

        if (word.endswith(self.__step1b_suffixes[1][0]) and self.__contains_vowel(
                word=word[:-len(self.__step1b_suffixes[1][0])])):
            return self.__step_1_2b(word[:-len(self.__step1b_suffixes[1][0])] + self.__step1b_suffixes[1][1])

        if (word.endswith(self.__step1b_suffixes[2][0]) and self.__contains_vowel(
                word=word[:-len(self.__step1b_suffixes[2][0])])):
            return self.__step_1_2b(word[:-len(self.__step1b_suffixes[2][0])] + self.__step1b_suffixes[2][1])

        return word

    def __step_1_2b(self, word: str) -> str:
        """
        Handles additional rules in step 1b, including replacing or removing certain suffixes after
        removing 'ed' or 'ing'.

        Parameters:
            word (str): The word to process.

        Returns:
            str: The word after applying additional step 1b suffix transformations.
        """
        for suffix in self.__step1_2b_suffixes:
            if word.endswith(suffix[0]):
                return word[:-len(suffix[0])] + suffix[1]

        if (not word.endswith("s") and not word.endswith("z") and not word.endswith(
                "l") and self.__end_with_double_consonant(word=word)):
            return word[:-1]

        if (self.__determine_m(word=word) == 1 and self.__end_with_cvc(word=word)):
            return word + "e"

        return word

    def __step_1_c(self, word: str) -> str:
        """
        Applies step 1c of the Porter Stemming Algorithm, changing 'y' to 'i' if there is another vowel in the word.

        Parameters:
            word (str): The word to process.

        Returns:
            str: The word after possibly changing 'y' to 'i'.
        """
        for suffix in self.__step1c_suffixes:
            if (word.endswith(suffix[0]) and self.__contains_vowel(word=word[:-len(suffix[0])])):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def __step_2(self, word: str) -> str:
        """
        Applies step 2 of the Porter Stemming Algorithm, which focuses on substituting suffixes to simplify
        the word's morphological structure.

        Parameters:
            word (str): The word to process.

        Returns:
            str: The word after applying step 2 suffix transformations.
        """
        for suffix in self.__step2_suffixes:
            if (word.endswith(suffix[0]) and self.__determine_m(word=word[:-len(suffix[0])]) > 0):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def __step_3(self, word: str) -> str:
        """
        Step 3 deals with words ending in "y", "ic", and various other suffixes by simplifying these to their
        root forms if certain conditions regarding the measure of the word (m) are met.

        Parameters:
            word (str): The word to process.

        Returns:
            str: The word after applying step 3 suffix transformations.
        """
        for suffix in self.__step3_suffixes:
            if (word.endswith(suffix[0]) and self.__determine_m(word=word[:-len(suffix[0])]) > 0):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def __step_4(self, word: str) -> str:
        """
        Step 4 of the Porter Stemming Algorithm removes some of the most common suffixes if the word is long enough
        (measure m > 1). This step helps further reduce the word closer to its root form.

        Parameters:
            word (str): The word to process.

        Returns:
            str: The word after applying step 4 suffix transformations.
        """
        for suffix in self.__step4_suffixes:
            if (word.endswith(suffix[0]) and self.__determine_m(word=word[:-len(suffix[0])]) > 1):
                return word[:-len(suffix[0])] + suffix[1]
        return word

    def __step_5(self, word: str) -> str:
        """
        Step 5 focuses on cleaning up the ends of words following the other stemming steps, particularly dealing with
        terminal 'e's and doubling consonants.

        Parameters:
            word (str): The word to process.

        Returns:
            str: The word after applying step 5 suffix transformations.
        """
        stem = self.__step_5_a(word=word)
        stem = self.__step_5_b(word=stem)
        return stem

    def __step_5_a(self, word: str) -> str:
        """
        Step 5a of the Porter Stemming Algorithm removes a terminal 'e' if there are at least two VC sequences
        in the word (m > 1), or if m = 1 and there is no cvc structure at the end of the word.

        Parameters:
            word (str): The word to process.

        Returns:
            str: The word after potentially removing a terminal 'e'.
        """
        for suffix in self.__step5a_suffixes:
            if self.__determine_m(word=word[:-len(suffix[0])]) > 1 and word.endswith(suffix[0]):
                return word[:-len(suffix[0])] + suffix[1]

        for suffix in self.__step5a_suffixes:
            if (word.endswith(suffix[0]) and self.__determine_m(
                    word=word[:-len(suffix[0])]) == 1 and not self.__end_with_cvc(word=word[:-len(suffix[0])])):
                return word[:-len(suffix[0])] + suffix[1]

        return word

    def __step_5_b(self, word: str) -> str:
        """
        Step 5b of the Porter Stemming Algorithm deals with words ending in double consonants. If the word ends
        with a double consonant and has a measure greater than 1, the last consonant is removed.

        Parameters:
            word (str): The word to process.

        Returns:
            str: The word after potentially removing the last consonant if it's a double consonant.
        """
        for suffix in self.__step5b_suffixes:
            if (word.endswith(suffix[0]) and self.__determine_m(word=word) > 1 and self.__end_with_double_consonant(word=word)):
                return word[:-len(suffix[0])] + suffix[1]
        return word
