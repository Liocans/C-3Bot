import os

from safetensors import torch

from modules.chatbot.chatbot_test import test_chatbot
from modules.chatbot.trainer.chat_bot_trainer import ChatBotTrainer
from utilities.path_finder import PathFinder


if __name__ == '__main__':

    ChatBotTrainer(extractor_name="BagOfWords", preprocessor_name="Stemmer", remove_stopwords=False,
                   modeling_name="NeuralNet", model_name="bow_stemmer_ws", num_epochs=50, batch_size=16,
                   learning_rate=0.005, hidden_size=16).start_training()