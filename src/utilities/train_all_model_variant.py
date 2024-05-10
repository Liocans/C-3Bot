from modules.chatbot.trainer.chat_bot_trainer import ChatBotTrainer

if __name__ == '__main__':
    ChatBotTrainer(extractor_name="BagOfWords", preprocessor_name="Lemmatizer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="bow_lemmatizer_ws", num_epochs=200, batch_size=8,
                   learning_rate=0.005, hidden_size=8).start_training()

    ChatBotTrainer(extractor_name="BagOfWords", preprocessor_name="Stemmer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="bow_stemmer_ws", num_epochs=200, batch_size=8,
                   learning_rate=0.005, hidden_size=8).start_training()

    ChatBotTrainer(extractor_name="BagOfWords", preprocessor_name="Lemmatizer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="bow_lemmatizer", num_epochs=200, batch_size=8,
                   learning_rate=0.005, hidden_size=8).start_training()

    ChatBotTrainer(extractor_name="BagOfWords", preprocessor_name="Stemmer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="bow_stemmer", num_epochs=200, batch_size=8,
                   learning_rate=0.005, hidden_size=8).start_training()

    ChatBotTrainer(extractor_name="TFIDF", preprocessor_name="Lemmatizer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="tfidf_lemmatizer_ws", num_epochs=200, batch_size=8,
                   learning_rate=0.005, hidden_size=8).start_training()

    ChatBotTrainer(extractor_name="TFIDF", preprocessor_name="Stemmer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="tfidf_stemmer_ws", num_epochs=200, batch_size=8,
                   learning_rate=0.005, hidden_size=8).start_training()

    ChatBotTrainer(extractor_name="TFIDF", preprocessor_name="Lemmatizer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="tfidf_lemmatizer", num_epochs=200, batch_size=8,
                   learning_rate=0.005, hidden_size=8).start_training()

    ChatBotTrainer(extractor_name="TFIDF", preprocessor_name="Stemmer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="tfidf_stemmer", num_epochs=200, batch_size=8,
                   learning_rate=0.005, hidden_size=8).start_training()

    ChatBotTrainer(extractor_name="Word2Vec_CBOW", preprocessor_name="Lemmatizer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="wvc_lemmatizer_ws", num_epochs=1000, batch_size=8,
                   learning_rate=0.005, hidden_size=8, vector_size=100, window=5).start_training()

    ChatBotTrainer(extractor_name="Word2Vec_CBOW", preprocessor_name="Stemmer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="wvc_stemmer_ws", num_epochs=1000, batch_size=8,
                   learning_rate=0.005, hidden_size=8, vector_size=100, window=5).start_training()

    ChatBotTrainer(extractor_name="Word2Vec_GRAM", preprocessor_name="Lemmatizer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="wvg_lemmatizer_ws", num_epochs=1000, batch_size=8,
                   learning_rate=0.005, hidden_size=8, vector_size=100, window=5).start_training()

    ChatBotTrainer(extractor_name="Word2Vec_GRAM", preprocessor_name="Stemmer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="wvg_stemmer_ws", num_epochs=1000, batch_size=8,
                   learning_rate=0.005, hidden_size=8, vector_size=100, window=5).start_training()

    ChatBotTrainer(extractor_name="Word2Vec_CBOW", preprocessor_name="Lemmatizer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="wvc_lemmatizer", num_epochs=1000, batch_size=8,
                   learning_rate=0.005, hidden_size=8, vector_size=100, window=5).start_training()

    ChatBotTrainer(extractor_name="Word2Vec_CBOW", preprocessor_name="Stemmer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="wvc_stemmer", num_epochs=1000, batch_size=8,
                   learning_rate=0.005, hidden_size=8, vector_size=100, window=5).start_training()

    ChatBotTrainer(extractor_name="Word2Vec_GRAM", preprocessor_name="Lemmatizer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="wvg_lemmatizer", num_epochs=1000, batch_size=8,
                   learning_rate=0.005, hidden_size=8, vector_size=100, window=5).start_training()

    ChatBotTrainer(extractor_name="Word2Vec_GRAM", preprocessor_name="Stemmer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="wvg_stemmer", num_epochs=1000, batch_size=8,
                   learning_rate=0.005, hidden_size=8, vector_size=100, window=5).start_training()