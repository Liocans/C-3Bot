from modules.chatbot.trainer.chat_bot_trainer import ChatBotTrainer

if __name__ == '__main__':
    ChatBotTrainer(extractor_name="BagOfWords", preprocessor_name="Lemmatizer", remove_stopwords=True,
                   modeling_name="NeuralNet", model_name="bow_lemmatizer", num_epochs=200, batch_size=8,
                   learning_rate=0.005, hidden_size=8).start_training()