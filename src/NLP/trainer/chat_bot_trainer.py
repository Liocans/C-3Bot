import json

import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from NLP.features_extractor.bag_of_words import BagOfWords
from NLP.modeling.neural_net import NeuralNet
from NLP.preprocessing.preprocessor import Preprocessor
from utilities.file_searcher import PathFinder
from utilities.json_utilities import add_model


class ChatBotTrainer(Dataset):

    def __init__(self, extractor, modeling, model_name, num_epochs=1000, batch_size=8, learning_rate=0.001,
                 hidden_size=8, model_canvas=None):
        self.__extractor = extractor
        self.__modeling = modeling
        self.__num_epochs = num_epochs
        self.__model_name = model_name
        self.__batch_size = batch_size
        self.__learning_rate = learning_rate
        self.__hidden_size = hidden_size
        self.__n_samples = 0
        self.__x_train = []
        self.__y_train = []
        self.__input_size = 0
        self.__output_size = 0
        self.__create_train_set()
        self.__input_size = len(self.__x_train[0])
        self.__output_size = len(self.__extractor.tags)
        self.__n_samples = len(self.__x_train)
        self.__model_canvas = model_canvas

    def start_training(self):
        train_loader = DataLoader(dataset=self,
                                  batch_size=self.__batch_size,
                                  shuffle=True,
                                  num_workers=0)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        model = NeuralNet(self.__input_size, self.__hidden_size, self.__output_size).to(device)

        # Loss and optimizer
        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(model.parameters(), lr=self.__learning_rate)

        # Train the modeling
        for epoch in range(self.__num_epochs):
            for (words, labels) in train_loader:
                words = words.to(dtype=torch.float).to(device)
                labels = labels.to(dtype=torch.long).to(device)

                # Forward pass
                outputs = model(words)
                # if y would be one-hot, we must apply
                # labels = torch.max(labels, 1)[1]
                loss = criterion(outputs, labels)

                # Backward and optimize
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()

            if (epoch + 1) % 100 == 0:
                print(f'Epoch [{epoch + 1}/{self.__num_epochs}], Loss: {loss.item():.4f}')

        print(f'final loss: {loss.item():.4f}')

        data = {
            "model_state": model.state_dict(),
            "input_size": self.__input_size,
            "hidden_size": self.__hidden_size,
            "output_size": self.__output_size,
            "all_words": self.__extractor.vocab,
            "tags": self.__extractor.tags
        }

        file_path = PathFinder.get_complet_path(f"ressources/model/{self.__model_name}.pth")
        torch.save(data, file_path)

        print(f'training complete. file saved to {file_path}')
        add_model(new_model_data=self.__model_canvas)

    def __create_train_set(self):
        file_path = PathFinder.get_complet_path('ressources/json_files/intents.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        for intent in intents_data["intents"]:
            for text in intent["patterns"]:
                representation = self.__extractor.extract_features(text)
                self.__x_train.append(representation)
                # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
                label = self.__extractor.tags.index(intent["tag"])
                self.__y_train.append(label)

        self.__x_train = np.array(self.__x_train)
        self.__y_train = np.array(self.__y_train)

        self.__input_size = len(self.__x_train[0])
        self.__output_size = len(self.__extractor.tags)
        self.__n_samples = len(self.__x_train)

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.__x_train[index], self.__y_train[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.__n_samples
