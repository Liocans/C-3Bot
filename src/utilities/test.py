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
    def __init__(self, model_name='bert-base-uncased'):
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.intents = []
        self.intent_map = {}
        self.model = None

    def load_data(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            intents_data = json.load(file)

        texts = []
        tags = []
        for intent in intents_data["intents"]:
            tag = intent["tag"]
            if tag not in self.intent_map:
                self.intent_map[tag] = len(self.intents)
                self.intents.append(tag)
            for text in intent["patterns"]:
                texts.append(text)
                tags.append(self.intent_map[tag])

        return texts, tags

    def prepare_data(self, texts, tags):
        encodings = self.tokenizer(texts, truncation=True, padding=True, max_length=512, return_tensors='pt')
        dataset = IntentDataset(encodings, tags)
        return dataset

    def train(self, file_path, epochs=3, learning_rate=5e-5, batch_size=16):
        texts, tags = self.load_data(file_path)
        dataset = self.prepare_data(texts, tags)
        train_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        self.model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(self.intents))
        self.model.train()
        optimizer = AdamW(self.model.parameters(), lr=learning_rate)

        for epoch in range(epochs):
            for batch in tqdm(train_loader, desc=f"Epoch {epoch + 1}"):
                self.model.zero_grad()
                input_ids = batch['input_ids']
                attention_mask = batch['attention_mask']
                labels = batch['labels']
                outputs = self.model(input_ids, attention_mask=attention_mask, labels=labels)
                loss = outputs.loss
                loss.backward()
                optimizer.step()

    def save_model(self, file_path):
        model_path = file_path + "_model"
        tokenizer_path = file_path + "_tokenizer"
        self.model.save_pretrained(model_path)
        self.tokenizer.save_pretrained(tokenizer_path)
        print(f"Model saved to {model_path}, Tokenizer saved to {tokenizer_path}")

    def load_model(self, file_path):
        model_path = file_path + "_model"
        tokenizer_path = file_path + "_tokenizer"
        self.model = BertForSequenceClassification.from_pretrained(model_path)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_path)
        print(f"Model loaded from {model_path}, Tokenizer loaded from {tokenizer_path}")

    def predict(self, text):
        self.model.eval()
        with torch.no_grad():
            inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
            outputs = self.model(**inputs)
            prediction = torch.argmax(outputs.logits, dim=-1)
            return self.intents[prediction.item()]


file_path = PathFinder.get_complet_path('ressources/json_files/intents.json')
# Example usage
classifier = BertIntentClassifier()
classifier.train(file_path)
prediction = classifier.predict("Hello mate, how are you doing ?")
print("Predicted Intent:", prediction)
