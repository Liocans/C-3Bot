import numpy as np
import torch

from modules.NLP.features_extractor.extractor import Extractor
from modules.NLP.modeling.modeling import Modeling
import json

from modules.NLP.preprocessing.sentence_segmenter import segment_sentences
from modules.NLP.preprocessing.preprocessor import Preprocessor
from utilities.path_finder import PathFinder


class ChatBot:
    def __init__(self, model_file):
        self.tags = None
        self.all_words = None
        self.extractor = None
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.load_model(model_file)
        self.model.eval()
        self.intents_data = dict()
        self.__load_intents()

    def __load_intents(self):
        file_path = PathFinder().get_complet_path('ressources/json_files/intents.json')
        # Load intents data from JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for intent in data.get('intents'):
                self.intents_data[intent['tag']] = {
                    'responses': intent['responses'],
                    'function': intent['function']
                }

    def load_model(self, model_file):
        data = torch.load(model_file, map_location=self.device)

        self.model = Modeling().select_model(model_name=data["modeling_name"], input_size=data["input_size"],
                                        hidden_size=data["hidden_size"], num_classes=data["output_size"],
                                        device=self.device)

        self.model.load_state_dict(data["model_state"])

        self.extractor = Extractor(preprocessor=Preprocessor(preprocessor_name=data["preprocessor"], remove_stopwords=data["remove_stopwords"]),
                              extractor_name=data["extractor"])  # Make sure this matches your actual implementation

        self.all_words, self.tags = data["all_words"], data["tags"]

    def get_response(self, input: str) -> list:
        treated_intents = set()
        ouputs = []
        for sentence in segment_sentences(input)["user_input"]:
            X = self.extractor.extract_features(sentence)
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
