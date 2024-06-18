import json

import time
import numpy as np
import torch
import torch.nn as nn
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader, Dataset

from modules.NLP.modeling.BERT import BertIntentClassifier
from modules.NLP.modeling.modeling import Modeling
from modules.NLP.features_extractor.extractor import Extractor
from modules.NLP.preprocessing.preprocessor import Preprocessor
from utilities.path_finder import PathFinder


class ChatBotTrainer:
    """
    A class responsible for training a chatbot using specified models and configurations. This trainer supports both BERT-based and custom model training setups.

    Attributes:
        __device (torch.device): The computing device (CPU or GPU) where the model operations are executed.
        __modeling_name (str): The name of the modeling technique to be used (e.g., 'BERT').
        __num_epochs (int): The number of training epochs.
        __batch_size (int): The number of samples per training batch.
        __learning_rate (float): The learning rate for the optimizer.
        __hidden_size (int): The size of the hidden layers in the neural network.
        __model_name (str): The name used to save or load the model.
        __vector_size (int): The dimensionality of the word vectors.
        __window (int): The context window size for the word vector model.
        __model (torch.nn.Module): The neural network model used for training.

    """

    def __init__(self, extractor_name: str = None, preprocessor_name: str = None, remove_stopwords: bool = None,
                 modeling_name: str = None, model_name: str = None, num_epochs: int = None, batch_size: int = None,
                 learning_rate: float = None, hidden_size: int = None, vector_size: int = None, window: int = None):
        """
        Initializes the ChatBotTrainer with the specified configuration and sets up the model based on the provided model name.

        Parameters:
            extractor_name (str): The name of the feature extractor to use.
            preprocessor_name (str): The name of the preprocessor to apply to the text data.
            remove_stopwords (bool): Whether to remove stopwords during preprocessing.
            modeling_name (str): The type of model to train ('BERT' for using BERT; others for custom models).
            model_name (str): The identifier for the model, used for saving and loading.
            num_epochs (int): The number of epochs to train the model.
            batch_size (int): The batch size for training.
            learning_rate (float): The optimizer's learning rate.
            hidden_size (int): The number of units in the hidden layers of a custom model.
            vector_size (int): The size of the embedding vectors.
            window (int): The window size in terms of the number of words around the target word for feature extraction.
        """

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

    def start_training(self) -> None:
        """
        Starts the training process for the chatbot. Depending on the configuration, it either trains a BERT model or a custom model.
        Tracks and prints training progress and loss at regular intervals.
        """

        if (self.__modeling_name == "BERT"):
            BertIntentClassifier(model_name=self.__model_name, num_epochs=self.__num_epochs,
                                 learning_rate=self.__learning_rate,batch_size=self.__batch_size).train()

        else:
            start = time.time()
            input_size = len(self.dataset[0][0])
            output_size = len(self.extractor.tags)

            self.__model = Modeling().select_model(modeling_name=self.__modeling_name, input_size=input_size,
                                                   hidden_size=self.__hidden_size, num_classes=output_size,
                                                   device=self.__device)

            train_loader = DataLoader(dataset=self.dataset, batch_size=self.__batch_size, shuffle=True, num_workers=0)

            criterion = nn.CrossEntropyLoss()
            optimizer = torch.optim.Adam(self.__model.parameters(), lr=self.__learning_rate)

            report_frequency = max(1, self.__num_epochs // 10)

            total_loss = 0
            num_batches = 0
            average_loss = 0
            losses = []
            epochs_reported = []
            for epoch in range(self.__num_epochs):
                for words, labels in train_loader:
                    words = words.to(dtype=torch.float).to(self.__device)
                    labels = labels.to(dtype=torch.long).to(self.__device)

                    outputs = self.__model(words)
                    loss = criterion(outputs, labels)

                    optimizer.zero_grad()
                    loss.backward()
                    optimizer.step()

                    total_loss += loss.item()
                    num_batches += 1

                    # Check if it's time to report
                if (epoch + 1) % report_frequency == 0 or epoch == 0:
                    average_loss = total_loss / num_batches
                    losses.append(average_loss)
                    epochs_reported.append(epoch + 1)
                    print(f'Epoch [{epoch + 1}/{self.__num_epochs}], Average Loss: {average_loss:.4f}')
                    total_loss = 0  # Reset total loss after reporting
                    num_batches = 0  # Reset batch count after reporting

            end = time.time()
            # self.__save_chart(epochs_reported=epochs_reported, losses=losses)
            self.__save_model(final_loss=average_loss, total_time=end - start)

    def __save_chart(self, epochs_reported, losses):
        # Plotting the loss curve
        plt.figure(figsize=(10, 5))
        plt.plot(epochs_reported, losses, marker='o', linestyle='-')
        plt.title(f'Loss Curve for {self.__model_name} - Learning Rate {self.__learning_rate}')
        plt.xlabel('Epoch')
        plt.ylabel('Average Loss')
        plt.grid(True)
        plt.savefig(PathFinder.get_complet_path(f"ressources/models_training_chart/{self.__model_name} - Epoch {self.__num_epochs} - Learning Rate {self.__learning_rate}.png"))
        plt.close()

    def __save_model(self, final_loss: float, total_time: float) -> None:
        """
        Saves the trained model and configuration to a file. Additionally, prints the training summary including the final loss and total training time.

        Parameters:
            final_loss (torch.Tensor): The loss value of the last training batch.
            total_time (float): The total time taken for the training process in seconds.
        """

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
        print(
            f'training complete in {total_time:.2f} sec. final loss: {final_loss:.4f}, file saved to {file_path}')


class IntentDataset(Dataset):
    """
    A PyTorch Dataset for loading and transforming text data for intent classification.

    Attributes:
        extractor (Extractor): An instance of the Extractor class used to convert text data into features.
        x_train (numpy.array): The features extracted from the training data.
        y_train (numpy.array): The intent labels corresponding to each feature set in x_train.

    """

    def __init__(self, extractor: Extractor):
        """
        Initializes the dataset with a feature extractor.

        Parameters:
            extractor (Extractor): The feature extractor that will be used to process text data.
        """

        self.extractor = extractor
        self.x_train = []
        self.y_train = []
        self.load_data()

    def load_data(self) -> None:
        """
        Loads intent data from a JSON file and processes it using the feature extractor to populate x_train and y_train.
        """

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
        """
        Retrieves a single item from the dataset.

        Parameters:
            index (int): The index of the item to retrieve.

        Returns:
            tuple: A tuple containing the features and the label of the requested item.
        """

        return self.x_train[index], self.y_train[index]

    def __len__(self):
        """
        Returns the total number of items in the dataset.

        Returns:
            int: The size of the dataset.
        """

        return len(self.x_train)
