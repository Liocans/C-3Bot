import json
from typing import Tuple

import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm
import time

from utilities.path_finder import PathFinder


class IntentDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)


class BertIntentClassifier:
    """
    A classifier for intent recognition in text using the BERT (Bidirectional Encoder Representations from Transformers) model.
    This class handles the entire process from loading and preprocessing data to training the model and making predictions.

    Attributes:
        __model_name (str): The name of the model for saving and loading purposes.
        __tokenizer (BertTokenizer): Tokenizer for converting text into tokens that BERT can understand.
        __intents (list): List of unique intent labels.
        __intent_map (dict): Mapping of intent labels to their corresponding indices.
        __model (BertForSequenceClassification): The BERT model for sequence classification.
        __texts (list): Collection of text data for training.
        __tags (list): Corresponding intent labels for the text data.
        __device (torch.device): Device (CPU or GPU) on which the model will run.

    Methods:
        load_data(): Loads training data from a JSON file and preprocesses it into a suitable format.
        prepare_data(): Prepares the data for training by encoding texts and converting labels into tensors.
        train(epochs, learning_rate, batch_size): Trains the BERT model using the specified hyperparameters.
        predict(text): Predicts the intent of a given text using the trained model.
        load_model(): Loads a trained BERT model and tokenizer from files.
    """

    def __init__(self, model_name: str):
        """
        Initializes the BertIntentClassifier with a specific model name.

        Parameters:
            model_name (str): The name used to save or load the model.
        """

        self.__model_name = model_name
        self.__tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.__intents = []
        self.__intent_map = {}
        self.__model = None
        self.__texts = []
        self.__tags = []
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.load_data()

    def load_data(self):
        """
        Loads intent data from a JSON file and processes it to prepare for training.
        This includes populating the texts and tags needed for creating the dataset.
        """

        file_path = PathFinder.get_complet_path("ressources/json_files/intents.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        for intent in intents_data["intents"]:
            tag = intent["tag"]
            if tag not in self.__intent_map:
                self.__intent_map[tag] = len(self.__intents)
                self.__intents.append(tag)
            for text in intent["patterns"]:
                self.__texts.append(text)
                self.__tags.append(self.__intent_map[tag])

    def prepare_data(self) -> IntentDataset:
        """
        Encodes text data and converts labels into tensors, preparing them as a dataset for training.

        Returns:
            IntentDataset: A dataset containing encoded texts and labels ready for training.
        """

        encodings = self.__tokenizer(self.__texts, truncation=True, padding=True, max_length=512, return_tensors='pt')
        dataset = IntentDataset(encodings, self.__tags)
        return dataset

    def train(self, epochs: int = 3, learning_rate: float = 0.0005, batch_size: int = 16) -> None:
        """
        Trains the BERT model for intent classification using the specified hyperparameters.

        Parameters:
            epochs (int): Number of training epochs.
            learning_rate (float): Learning rate for the optimizer.
            batch_size (int): Number of samples per batch.
        """

        start = time.time()
        dataset = self.prepare_data()
        train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.__model = BertForSequenceClassification.from_pretrained('bert-base-uncased',
                                                                     num_labels=len(self.__intents))

        self.__model.to(self.__device)  # Send model to device
        self.__model.train()
        optimizer = AdamW(self.__model.parameters(), lr=learning_rate)
        running_loss = 0.0

        for epoch in range(epochs):
            running_loss = 0.0
            # Create tqdm progress bar
            progress_bar = tqdm(train_loader, desc=f"Epoch {epoch + 1}")
            for i, batch in enumerate(progress_bar):
                self.__model.zero_grad()
                input_ids = batch['input_ids']
                attention_mask = batch['attention_mask']
                labels = batch['labels']
                outputs = self.__model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()

                running_loss = loss.item()
                # Update progress bar description with current loss
                progress_bar.set_description(f"Epoch {epoch + 1} Loss: {loss.item():.4f}")

        end = time.time()

        self.__save_model(epochs, learning_rate, batch_size, end - start, running_loss)

    def __save_model(self, epochs: int, learning_rate: float, batch_size: int, total_time: float,
                     last_loss: float) -> None:
        """
        Saves the trained BERT model and tokenizer to the specified file paths. Updates the model configuration with the training parameters.

        Parameters:
            epochs (int): The total number of epochs trained.
            learning_rate (float): The learning rate used in training.
            batch_size (int): The batch size used in training.
            total_time (float): The total time taken for the training in seconds.
            last_loss (float): The loss value of the last training batch.

        This method also prints out a summary of the training results including the time taken and final loss.
        """

        model_path, tokenizer_path = self.__get_necessary_path()

        # Load or update the model config
        config = self.__model.config

        # Add custom training parameters to the configuration
        config.num_epochs = epochs  # Assuming self.epochs is defined
        config.learning_rate = learning_rate  # Assuming self.lr is defined
        config.batch_size = batch_size  # Assuming self.batch_size is defined

        self.__model.save_pretrained(model_path)
        self.__tokenizer.save_pretrained(tokenizer_path)

        print(f'training complete in {total_time:.2f} sec. final loss: {last_loss:.4f}, file saved to {model_path}')

    def load_model(self) -> None:
        """
        Loads a trained BERT model and tokenizer from files, preparing the classifier for making predictions.
        """

        model_path, tokenizer_path = self.__get_necessary_path()
        self.__model = BertForSequenceClassification.from_pretrained(model_path)
        self.__tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        print(f"Model loaded from {model_path}, Tokenizer loaded from {tokenizer_path}")

    def __get_necessary_path(self) -> tuple[str, str]:
        """
        Determines the file paths for saving the BERT model and tokenizer based on the model name.

        Returns:
            tuple[str, str]: A tuple containing the file paths for the model and the tokenizer.
        """

        model_path = PathFinder.get_complet_path(f"ressources/models/{self.__model_name}")
        tokenizer_path = PathFinder.get_complet_path(f"ressources/tokenizers/{self.__model_name}_T")
        return model_path, tokenizer_path

    def predict(self, text) -> str:
        """
        Predicts the intent of a given text using the trained BERT model.

        Parameters:
            text (str): The text for which the intent is to be predicted.

        Returns:
            str: The predicted intent label.
        """

        self.__model.eval()
        with torch.no_grad():
            inputs = self.__tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            outputs = self.__model(**inputs)
            prediction = torch.argmax(outputs.logits, dim=1)
            return self.__intents[prediction.item()]
