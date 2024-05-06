import torch
from transformers import BertTokenizer, BertForSequenceClassification, AdamW
from torch.utils.data import DataLoader, Dataset
import json

class IntentDataset(Dataset):
    def __init__(self, intents, tokenizer, max_len=512):
        self.examples = []
        self.tokenizer = tokenizer
        self.max_len = max_len

        for intent in intents:
            tag = intent['tag']
            for pattern in intent['patterns']:
                self.examples.append((pattern, tag))

        self.labels = {tag: idx for idx, tag in enumerate(set(tag for _, tag in self.examples))}

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, idx):
        text, tag = self.examples[idx]
        label = self.labels[tag]
        encoding = self.tokenizer.encode_plus(
            text,
            add_special_tokens=True,
            max_length=self.max_len,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

class BertClassifier:
    def __init__(self, model_name, data_file):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        with open(data_file, 'r') as file:
            data = json.load(file)
        self.num_labels = len(set(intent['tag'] for intent in data))
        self.model = BertForSequenceClassification.from_pretrained(model_name, num_labels=self.num_labels)
        self.model.to(self.device)
        self.dataset = IntentDataset(data, self.tokenizer)

    def train(self, epochs=3, batch_size=16, learning_rate=5e-5):
        data_loader = DataLoader(self.dataset, batch_size=batch_size, shuffle=True)
        optimizer = AdamW(self.model.parameters(), lr=learning_rate)

        for epoch in range(epochs):
            print(f"Epoch {epoch + 1}/{epochs}")
            self.model.train()
            for batch in data_loader:
                batch = {k: v.to(self.device) for k, v in batch.items()}
                outputs = self.model(**batch)
                loss = outputs.loss
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
                print(f"Training loss: {loss.item()}")

    def predict(self, text):
        self.model.eval()
        encoded_input = self.tokenizer.encode_plus(
            text,
            return_tensors="pt",
            max_length=512,
            padding='max_length',
            truncation=True
        ).to(self.device)

        with torch.no_grad():
            outputs = self.model(**encoded_input)
            _, preds = torch.max(outputs.logits, dim=1)

        label_map = {v: k for k, v in self.dataset.labels.items()}
        return label_map[preds.cpu().numpy()[0]]

# Example usage:
# classifier = IntentClassifier('bert-base-uncased', 'path_to_your_data.json')
# classifier.train()
