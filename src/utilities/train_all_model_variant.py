from modules.chatbot.chatbot_test import test_chatbot
from modules.chatbot.trainer.chat_bot_trainer import ChatBotTrainer

if __name__ == '__main__':

    ChatBotTrainer(extractor_name="BagOfWords", preprocessor_name="Lemmatizer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="bow_lemmatizer_ws", num_epochs=50, batch_size=16,
                   learning_rate=0.005, hidden_size=16).start_training()

    test_chatbot("bow_lemmatizer_ws.pth")

    ChatBotTrainer(extractor_name="BagOfWords", preprocessor_name="Stemmer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="bow_stemmer_ws", num_epochs=50, batch_size=16,
                   learning_rate=0.005, hidden_size=16).start_training()

    test_chatbot("bow_stemmer_ws.pth")

    ChatBotTrainer(extractor_name="BagOfWords", preprocessor_name="Lemmatizer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="bow_lemmatizer", num_epochs=50, batch_size=16,
                   learning_rate=0.005, hidden_size=16).start_training()

    test_chatbot("bow_lemmatizer.pth")

    ChatBotTrainer(extractor_name="BagOfWords", preprocessor_name="Stemmer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="bow_stemmer", num_epochs=50, batch_size=16,
                   learning_rate=0.005, hidden_size=16).start_training()

    test_chatbot("bow_stemmer.pth")

    ChatBotTrainer(extractor_name="TFIDF", preprocessor_name="Lemmatizer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="tfidf_lemmatizer_ws", num_epochs=50, batch_size=16,
                   learning_rate=0.005, hidden_size=16).start_training()

    test_chatbot("tfidf_lemmatizer_ws.pth")

    ChatBotTrainer(extractor_name="TFIDF", preprocessor_name="Stemmer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="tfidf_stemmer_ws", num_epochs=50, batch_size=16,
                   learning_rate=0.005, hidden_size=16).start_training()

    test_chatbot("tfidf_stemmer_ws.pth")

    ChatBotTrainer(extractor_name="TFIDF", preprocessor_name="Lemmatizer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="tfidf_lemmatizer", num_epochs=50, batch_size=16,
                   learning_rate=0.005, hidden_size=16).start_training()

    test_chatbot("tfidf_lemmatizer.pth")

    ChatBotTrainer(extractor_name="TFIDF", preprocessor_name="Stemmer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="tfidf_stemmer", num_epochs=50, batch_size=16,
                   learning_rate=0.005, hidden_size=16).start_training()

    test_chatbot("tfidf_stemmer.pth")

    ChatBotTrainer(extractor_name="Word2Vec_CBOW", preprocessor_name="Lemmatizer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="wvc_lemmatizer_ws", num_epochs=1000, batch_size=16,
                   learning_rate=0.003, hidden_size=16, vector_size=100, window=5).start_training()

    test_chatbot("wvc_lemmatizer_ws.pth")

    ChatBotTrainer(extractor_name="Word2Vec_CBOW", preprocessor_name="Stemmer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="wvc_stemmer_ws", num_epochs=1000, batch_size=16,
                   learning_rate=0.003, hidden_size=16, vector_size=100, window=5).start_training()

    test_chatbot("wvc_stemmer_ws.pth")

    ChatBotTrainer(extractor_name="Word2Vec_GRAM", preprocessor_name="Lemmatizer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="wvg_lemmatizer_ws", num_epochs=1000, batch_size=16,
                   learning_rate=0.003, hidden_size=16, vector_size=100, window=5).start_training()

    test_chatbot("wvg_lemmatizer_ws.pth")

    ChatBotTrainer(extractor_name="Word2Vec_GRAM", preprocessor_name="Stemmer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="wvg_stemmer_ws", num_epochs=1000, batch_size=16,
                   learning_rate=0.003, hidden_size=16, vector_size=100, window=5).start_training()

    test_chatbot("wvg_stemmer_ws.pth")

    ChatBotTrainer(extractor_name="Word2Vec_CBOW", preprocessor_name="Lemmatizer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="wvc_lemmatizer", num_epochs=1000, batch_size=16,
                   learning_rate=0.003, hidden_size=16, vector_size=100, window=5).start_training()

    test_chatbot("wvc_lemmatizer.pth")

    ChatBotTrainer(extractor_name="Word2Vec_CBOW", preprocessor_name="Stemmer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="wvc_stemmer", num_epochs=1000, batch_size=16,
                   learning_rate=0.003, hidden_size=16, vector_size=100, window=5).start_training()

    test_chatbot("wvc_stemmer.pth")

    ChatBotTrainer(extractor_name="Word2Vec_GRAM", preprocessor_name="Lemmatizer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="wvg_lemmatizer", num_epochs=1000, batch_size=16,
                   learning_rate=0.003, hidden_size=16, vector_size=100, window=5).start_training()

    test_chatbot("wvg_lemmatizer.pth")

    ChatBotTrainer(extractor_name="Word2Vec_GRAM", preprocessor_name="Stemmer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="wvg_stemmer", num_epochs=1000, batch_size=16,
                   learning_rate=0.003, hidden_size=16, vector_size=100, window=5).start_training()

    test_chatbot("wvg_stemmer.pth")

    ChatBotTrainer(modeling_name="BERT", model_name="bert_intent_classificator", num_epochs=40, batch_size=16,
                   learning_rate=0.00004).start_training()

    test_chatbot("bert_intent_classificator")