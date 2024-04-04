import numpy as np
import torch
import torch.nn as nn
from NLP.features_extractor.bag_of_words import BagOfWords
from NLP.modeling.neural_net import NeuralNet
import json

from NLP.preprocessing.sentence_segmenter import segment_sentences
from NLP.preprocessing.text_preprocessor import TextPreprocessor
from utilities.file_searcher import PathFinder


class ChatBot:
    def __init__(self, model_file):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model, self.bag_of_words, self.all_words, self.tags = self.load_model(model_file)
        self.model.eval()
        self.intents_data = dict()
        self.__load_intents()


    def __load_intents(self):
        filename = PathFinder().get_complet_path('ressources/intents/intents.json')
        # Load intents data from JSON file
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for intent in data.get('intents'):
                self.intents_data[intent['tag']] = {
                    'responses': intent['responses'],
                    'function': intent['function']
                }

    def load_model(self, model_file):
        data = torch.load(model_file, map_location=self.device)
        input_size = data["input_size"]
        hidden_size = data["hidden_size"]
        output_size = data["output_size"]
        all_words = data["all_words"]
        tags = data["tags"]

        model = NeuralNet(input_size, hidden_size, output_size).to(self.device)
        model.load_state_dict(data["model_state"])

        bag_of_words = BagOfWords(prepocessor=TextPreprocessor())  # Make sure this matches your actual implementation

        return model, bag_of_words, all_words, tags

    def get_response(self, input: str) -> list:
        treated_intents = set()
        ouputs = []
        for sentence in segment_sentences(input)["user_input"]:
            X = self.bag_of_words.extract_features(sentence)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(dtype=torch.float).to(self.device)

            output = self.model(X)
            _, predicted = torch.max(output, dim=1)

            tag = self.tags[predicted.item()]
            if tag not in treated_intents:
                probabilities = torch.softmax(output, dim=1)
                prob = probabilities[0][predicted.item()]

                if prob.item() > 0.75:
                    treated_intents.add(tag)
                    ouputs.append(np.random.choice(self.intents_data[tag]['responses']))
                else:
                    ouputs.append("I do not understand...")

        return ouputs

if __name__ == '__main__':
    path_to_model = PathFinder().get_complet_path('ressources/model/bow_lemmatizer.pth')
    chatbot = ChatBot(model_file=path_to_model)

    print("Let's chat! type 'quit' to exit.")
    while True:
        sentence = input("You: ")
        if sentence == "quit":
            break
        response = chatbot.get_response(sentence)
        print("Bot:", response)