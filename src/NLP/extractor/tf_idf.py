import numpy as np
import math
from collections import defaultdict


class TFIDF:
    def __init__(self, documents):
        """
        Initialize the TFIDF class with a list of documents.
        Each document is expected to be a list of tokenized words.
        """
        self.documents = documents
        self.vocab = self._build_vocab(documents)
        self.idf = self._calculate_idf()

    def _build_vocab(self, documents):
        """
        Build and return a set of unique words in the documents.
        """
        vocab = set()
        for doc in documents:
            vocab.update(doc)
        return list(vocab)

    def _calculate_idf(self):
        """
        Calculate and return the inverse document frequency (IDF) for each word in the vocabulary.
        """
        df = defaultdict(int)
        for doc in self.documents:
            seen = set()
            for word in doc:
                if word not in seen:
                    df[word] += 1
                    seen.add(word)

        idf = {}
        total_docs = len(self.documents)
        for word, freq in df.items():
            idf[word] = math.log((total_docs + 1) / (freq + 1)) + 1  # Applying smoothing

        return idf

    def _calculate_tf(self, document):
        """
        Calculate and return the term frequency (TF) for each word in a single document.
        """
        tf = defaultdict(int)
        for word in document:
            tf[word] += 1

        max_tf = max(tf.values())
        for word in tf:
            tf[word] = tf[word] / max_tf  # Normalize TF

        return tf

    def calculate_tfidf(self, new_documents=None):
        """
        Calculate the TF-IDF for the provided documents or the initialized documents if none are provided.
        Returns a TF-IDF matrix where rows are documents and columns are terms in the vocabulary.
        """
        if new_documents is None:
            documents_to_use = self.documents
        else:
            documents_to_use = new_documents

        tfidf_matrix = np.zeros((len(documents_to_use), len(self.vocab)))

        for i, doc in enumerate(documents_to_use):
            tf = self._calculate_tf(doc)
            for j, word in enumerate(self.vocab):
                tfidf_matrix[i, j] = tf.get(word, 0) * self.idf.get(word, 0)

        return tfidf_matrix
