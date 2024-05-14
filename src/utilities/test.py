import os

from safetensors import torch

from modules.chatbot.chatbot_test import test_chatbot
from modules.chatbot.trainer.chat_bot_trainer import ChatBotTrainer
from utilities.path_finder import PathFinder

# ChatBotTrainer(modeling_name="BERT", model_name="bert", num_epochs=2, batch_size=8,
#                learning_rate=0.005).start_training()
#
# path_file = PathFinder.get_complet_path("ressources/models/bert")
#
# directory = PathFinder.get_complet_path("ressources/models/")  # Change this to your directory path
# files = os.listdir(directory)
# print(files)

if __name__ == '__main__':
    ChatBotTrainer(extractor_name="Word2Vec_CBOW", preprocessor_name="Lemmatizer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="wvc_lemmatizer_ws", num_epochs=1000, batch_size=8,
                   learning_rate=0.005, hidden_size=8, vector_size=100, window=5).start_training()

    test_chatbot("wvc_lemmatizer_ws.pth")