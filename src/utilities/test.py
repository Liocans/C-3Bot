import os

from safetensors import torch

from modules.chatbot.chatbot_test import test_chatbot
from modules.chatbot.trainer.chat_bot_trainer import ChatBotTrainer
from utilities.path_finder import PathFinder


if __name__ == '__main__':

    print("Basic path:", PathFinder.get_basic_path())
    print("Complete path:", PathFinder.get_complet_path("ressources"))