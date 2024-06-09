import json
from typing import Tuple

import torch
from matplotlib import pyplot as plt
from transformers import BertTokenizer, BertForSequenceClassification, TrainingArguments, Trainer
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

    def __init__(self, model_name: str, num_epochs: int = None, learning_rate: float = None, batch_size: int = None):
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
        self.__num_epochs = num_epochs
        self.__learning_rate = learning_rate
        self.__batch_size = batch_size
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

    def train(self) -> None:
        """
        Trains the BERT model for intent classification using the specified hyperparameters.
        """

        dataset = self.prepare_data()

        self.__model = BertForSequenceClassification.from_pretrained('bert-base-uncased',
                                                                     num_labels=len(self.__intents)).to(self.__device)

        training_args = TrainingArguments(
            output_dir=PathFinder.get_complet_path(f"ressources/results/"),
            num_train_epochs=self.__num_epochs,
            per_device_train_batch_size=self.__batch_size,
            per_device_eval_batch_size=self.__batch_size,
            learning_rate=self.__learning_rate,
            warmup_steps=500,
            weight_decay=0.01,
            logging_dir=PathFinder.get_complet_path(f"ressources/logs/"),
            logging_steps=10  # Log metrics and loss every 10 steps
        )

        trainer = Trainer(
            model=self.__model,
            args=training_args,
            train_dataset=dataset,
        )

        train_result = trainer.train()

        last_loss = trainer.state.log_history[-2]["loss"] # Capture the last training loss

        time_taken = train_result.metrics["train_runtime"]

        # Extract loss data from Trainer logs
        loss_data = [entry for entry in trainer.state.log_history if 'loss' in entry]

        # Prepare data for plotting
        epochs_reported = [i for i in range(len(loss_data))]
        losses = [entry['loss'] for entry in loss_data]

        self.__save_chart(epochs_reported, losses)

        self.__save_model(time_taken, last_loss)

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

    def __save_model(self, total_time: float, last_loss: float) -> None:
        """
        Saves the trained BERT model and tokenizer to the specified file paths. Updates the model configuration with the training parameters.

        Parameters:
            total_time (float): The total time taken for the training in seconds.
            last_loss (float): The loss value of the last training batch.

        This method also prints out a summary of the training results including the time taken and final loss.
        """

        model_path, tokenizer_path = self.__get_necessary_path()

        # Load or update the model config
        config = self.__model.config

        # Add custom training parameters to the configuration
        config.num_epochs = self.__num_epochs  # Assuming self.epochs is defined
        config.learning_rate = self.__learning_rate  # Assuming self.lr is defined
        config.batch_size = self.__batch_size  # Assuming self.batch_size is defined

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
        inputs = self.__tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
        with torch.no_grad():
            outputs = self.__model(**inputs)
        prediction = torch.argmax(outputs.logits, dim=1)
        return self.__intents[prediction.item()]
