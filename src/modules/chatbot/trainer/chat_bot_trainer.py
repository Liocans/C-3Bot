import json

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

from modules.NLP.modeling.BERT import BertIntentClassifier
from modules.NLP.modeling.modeling import Modeling
from modules.NLP.features_extractor.extractor import Extractor
from modules.NLP.preprocessing.preprocessor import Preprocessor
from utilities.path_finder import PathFinder


class ChatBotTrainer:
    def __init__(self, extractor_name=None, preprocessor_name=None, remove_stopwords=None,
                 modeling_name=None, model_name=None, num_epochs=None, batch_size=None,
                 learning_rate=None, hidden_size=None, vector_size=None, window=None):

        self.__device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.__modeling_name = modeling_name
        self.__num_epochs = num_epochs
        self.__batch_size = batch_size
        self.__learning_rate = learning_rate
        self.__hidden_size = hidden_size
        self.__model_name = model_name
        self.__vector_size = vector_size
        self.__window = window
        self.__model = None

        if (modeling_name != "BERT"):
            self.preprocessor = Preprocessor(preprocessor_name, remove_stopwords)
            self.extractor = Extractor(preprocessor=self.preprocessor, extractor_name=extractor_name,
                                       vector_size=self.__vector_size, window=self.__window,
                                       model_name=self.__model_name,
                                       is_training=True)

            self.dataset = IntentDataset(extractor=self.extractor)

    def start_training(self):

        if (self.__modeling_name == "BERT"):
            BertIntentClassifier(model_name=self.__model_name).train(epochs=self.__num_epochs, learning_rate=self.__learning_rate,
                                 batch_size=self.__batch_size)

        else:
            input_size = len(self.dataset[0][0])
            output_size = len(self.extractor.tags)

            self.__model = Modeling().select_model(modeling_name=self.__modeling_name, input_size=input_size,
                                                   hidden_size=self.__hidden_size, num_classes=output_size,
                                                   device=self.__device)

            train_loader = DataLoader(dataset=self.dataset, batch_size=self.__batch_size, shuffle=True, num_workers=0)

            criterion = nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(self.__model.parameters(), lr=self.__learning_rate)

            for epoch in range(self.__num_epochs):
                for words, labels in train_loader:
                    words = words.to(dtype=torch.float).to(self.__device)
                    labels = labels.to(dtype=torch.long).to(self.__device)

                    outputs = self.__model(words)
                    loss = criterion(outputs, labels)

                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                if (epoch + 1) % 100 == 0:
                    print(f'Epoch [{epoch + 1}/{self.__num_epochs}], Loss: {loss.item():.4f}')

            self.save_model(loss)

    def save_model(self, final_loss):
        data = {
            "model_state": self.__model.state_dict(),
            "input_size": len(self.dataset[0][0]),
            "hidden_size": self.__hidden_size,
            "output_size": len(self.extractor.tags),
            "vocab": self.extractor.vocab,
            "tags": self.extractor.tags,
            "docs": self.extractor.docs,
            "extractor": self.extractor.extractor_name,
            "preprocessor": self.extractor.preprocessor.preprocessor_name,
            "remove_stopwords": self.extractor.preprocessor.remove_stopwords,
            "modeling_name": self.__modeling_name,
            "num_epochs": self.__num_epochs,
            "batch_size": self.__batch_size,
            "learning_rate": self.__learning_rate,
            "vector_size": self.__vector_size,
            "window": self.__window,
        }

        file_path = PathFinder.get_complet_path(f"ressources/models/{self.__model_name}.pth")
        torch.save(data, file_path)
        print(f'training complete. final loss: {final_loss.item():.4f}, file saved to {file_path}')


class IntentDataset(Dataset):
    def __init__(self, extractor):
        self.extractor = extractor
        self.x_train = []
        self.y_train = []
        self.load_data()

    def load_data(self):
        file_path = PathFinder().get_complet_path('ressources/json_files/intents.json')
        with open(file_path, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        for intent in intents_data["intents"]:
            for pattern in intent["patterns"]:
                features = self.extractor.extract_features(pattern)
                self.x_train.append(features)
                self.y_train.append(self.extractor.tags.index(intent["tag"]))

        self.x_train = np.array(self.x_train)
        self.y_train = np.array(self.y_train)

    def __getitem__(self, index):
        return self.x_train[index], self.y_train[index]

    def __len__(self):
        return len(self.x_train)
