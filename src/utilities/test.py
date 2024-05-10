import os

from safetensors import torch

from modules.chatbot.trainer.chat_bot_trainer import ChatBotTrainer
from utilities.path_finder import PathFinder

ChatBotTrainer(modeling_name="BERT", model_name="bert", num_epochs=2, batch_size=8,
               learning_rate=0.005).start_training()

path_file = PathFinder.get_complet_path("ressources/models/bert")

directory = PathFinder.get_complet_path("ressources/models/")  # Change this to your directory path
files = os.listdir(directory)
print(files)