import json

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from modules.NLP.features_extractor.extractor import Extractor
from modules.NLP.modeling.modeling import Modeling
from modules.NLP.preprocessing.preprocessor import Preprocessor
from utilities.path_finder import PathFinder


class ChatBotTrainer(Dataset):

    def __init__(self, extractor_name="BagOfWords", preprocessor_name="Lemmatizer", stopwords=False,
                 modeling_name="NeuralNet", model_name="bow_lemmatizer", num_epochs=1000, batch_size=8,
                 learning_rate=0.0005, hidden_size=8, vector_size=None, window=None):

        self.__extractor = Extractor(preprocessor=Preprocessor(preprocessor_name, stopwords), extractor_name=extractor_name,
                                     vector_size=vector_size, window=window)

        self.__modeling_name = modeling_name
        self.__vector_size = vector_size
        self.__window = window
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

    def start_training(self):
        train_loader = DataLoader(dataset=self,
                                  batch_size=self.__batch_size,
                                  shuffle=True,
                                  num_workers=0)

        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

        model = Modeling().select_model(model_name=self.__modeling_name, input_size=self.__input_size,
                                        hidden_size=self.__hidden_size, num_classes=self.__output_size, device=device)

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
            "vocab": self.__extractor.vocab,
            "tags": self.__extractor.tags,
            "docs": self.__extractor.docs,
            "extractor": self.__extractor.extractor_name,
            "preprocessor": self.__extractor.preprocessor.preprocessor_name,
            "remove_stopwords": self.__extractor.preprocessor.remove_stopwords,
            "modeling_name": self.__modeling_name,
            "num_epochs": self.__num_epochs,
            "batch_size": self.__batch_size,
            "learning_rate": self.__learning_rate,
            "vector_size": self.__vector_size,
            "window": self.__window,
        }

        file_path = PathFinder.get_complet_path(f"ressources/models/{self.__model_name}.pth")
        torch.save(data, file_path)

        print(f'training complete. file saved to {file_path}')

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
