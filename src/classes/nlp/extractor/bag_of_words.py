from sklearn.feature_extraction.text import CountVectorizer

# create the vocabulary
vectorizer = CountVectorizer()

# fit the vocabulary to the text data
vectorizer.fit(text_data)

# create the bag-of-words model
bow_model = vectorizer.transform(text_data)

# print the bag-of-words model
print(bow_model)