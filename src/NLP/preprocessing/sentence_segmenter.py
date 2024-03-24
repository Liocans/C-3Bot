import re


class SentenceSegmenter:
    def __init__(self):
        self.pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s')

    def segment_sentences(self, text):
        return self.pattern.split(text)
