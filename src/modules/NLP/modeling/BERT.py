import json
import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, Dataset
from tqdm import tqdm

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
    def __init__(self, model_name):
        self.__model_name = model_name
        self.__tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        self.__intents = []
        self.__intent_map = {}
        self.__model = None

    def load_data(self):
        file_path = PathFinder.get_complet_path("ressources/json_files/intents.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        texts = []
        tags = []
        for intent in intents_data["intents"]:
            tag = intent["tag"]
            if tag not in self.__intent_map:
                self.__intent_map[tag] = len(self.__intents)
                self.__intents.append(tag)
            for text in intent["patterns"]:
                texts.append(text)
                tags.append(self.__intent_map[tag])

        return texts, tags

    def prepare_data(self, texts, tags):
        encodings = self.__tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors='pt')
        dataset = IntentDataset(encodings, tags)
        return dataset

    def train(self, epochs=3, learning_rate=0.0005, batch_size=16):
        texts, tags = self.load_data()
        dataset = self.prepare_data(texts, tags)
        train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.__model = BertForSequenceClassification.from_pretrained('bert-base-uncased',
                                                                     num_labels=len(self.__intents))
        self.__model.train()
        optimizer = AdamW(self.__model.parameters(), lr=learning_rate)

        for epoch in range(epochs):
            for batch in tqdm(train_loader, desc=f"Epoch {epoch + 1}"):
                self.__model.zero_grad()
                input_ids = batch['input_ids']
                attention_mask = batch['attention_mask']
                labels = batch['labels']
                outputs = self.__model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()

        self.__save_model(epochs, learning_rate, batch_size)

    def __save_model(self, epochs, learning_rate, batch_size):
        model_path, tokenizer_path = self.__get_necessary_path()

        # Load or update the model config
        config = self.__model.config

        # Add custom training parameters to the configuration
        config.num_epochs = epochs  # Assuming self.epochs is defined
        config.learning_rate = learning_rate  # Assuming self.lr is defined
        config.batch_size = batch_size  # Assuming self.batch_size is defined

        self.__model.save_pretrained(model_path)
        self.__tokenizer.save_pretrained(tokenizer_path)

        print(f"Model saved to {model_path}, Tokenizer saved to {tokenizer_path}")

    def load_model(self):
        model_path, tokenizer_path = self.__get_necessary_path()
        self.__model = BertForSequenceClassification.from_pretrained(model_path)
        self.__tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        print(f"Model loaded from {model_path}, Tokenizer loaded from {tokenizer_path}")

    def __get_necessary_path(self):
        model_path = PathFinder.get_complet_path(f"ressources/models/{self.__model_name}")
        tokenizer_path = PathFinder.get_complet_path(f"ressources/tokenizers/{self.__model_name}_T")
        return model_path, tokenizer_path

    def predict(self, text):
        self.__model.eval()
        with torch.no_grad():
            inputs = self.__tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            outputs = self.__model(**inputs)
            probabilities = torch.softmax(outputs.logits, dim=-1)  # Apply softmax to convert logits to probabilities
            max_prob, prediction = torch.max(probabilities, dim=-1)  # Get the max probability and index
            return self.__intents[prediction.item()] if max_prob >= 0.7 else ""
