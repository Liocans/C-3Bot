import re


class SentenceSegmenter:

    __pattern = re.compile(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|!)\s')

    @staticmethod
    def segment_sentences(text):
        return SentenceSegmenter.__pattern.split(text)
