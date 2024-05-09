from transformers import BertTokenizer, BertModel
import torch

class BertFeatureExtractor:
    def __init__(self, model_name='bert-base-uncased'):
        # Initializes the tokenizer and model with the specified BERT model.
        self.tokenizer = BertTokenizer.from_pretrained(model_name)
        self.model = BertModel.from_pretrained(model_name)
        self.model.eval()  # Set the model to evaluation mode

    def tokenize(self, text):
        # Tokenizes the text and returns the tensor.
        inputs = self.tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=512)
        return inputs

    def extract_features(self, text):
        # Tokenizes the text and extracts features using the BERT model.
        with torch.no_grad():  # No need to calculate gradients
            inputs = self.tokenize(text)
            outputs = self.model(**inputs)
            return outputs.last_hidden_state

# Usage
bert_extractor = BertFeatureExtractor()

# Example text
text = "Hello, how are you?"
features = bert_extractor.tokenize(text)
print(features)  # Check the shape of the output features
