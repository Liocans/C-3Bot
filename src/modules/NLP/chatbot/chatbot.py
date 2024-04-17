import json

import numpy as np
import torch
import importlib

from modules.NLP.features_extractor.extractor import Extractor
from modules.NLP.modeling.modeling import Modeling
from modules.NLP.preprocessing.preprocessor import Preprocessor
from modules.NLP.preprocessing.sentence_segmenter import segment_sentences
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
                    'function': intent['function'],
                    'module': intent["module"],
                    "class": intent["class"],
                    "parameters": intent["parameters"]
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
        outputs = []
        treated_user_input = segment_sentences(input)
        for sentence in treated_user_input["user_input"]:
            X = self.extractor.extract_features(sentence)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(dtype=torch.float).to(self.device)

            output = self.model(X)
            _, predicted = torch.max(output, dim=1)

            tag = self.tags[predicted.item()]
            if tag not in treated_intents:
                probabilities = torch.softmax(output, dim=1)
                prob = probabilities[0][predicted.item()]

                if prob.item() > 0.7:
                    treated_intents.add(tag)
                    outputs.append(np.random.choice(self.intents_data[tag]['responses']))
                    if(self.intents_data[tag]['class'] != ""):
                        module = importlib.import_module(self.intents_data[tag]['module'])
                        class_instance = getattr(module, self.intents_data[tag]['class'])()
                        function_to_call = getattr(class_instance, self.intents_data[tag]['function'])

                        for item in self.intents_data[tag]['parameters']['dynamic']:
                            self.intents_data[tag]['parameters']['static'][item] = treated_user_input[item]

                        param = list(self.intents_data[tag]['parameters']['static'].values())
                        # Call the function with parameters unpacked from the list
                        outputs.append(function_to_call(*param))
                    elif (self.intents_data[tag]['function'] != ""):
                        module = importlib.import_module(self.intents_data[tag]['module'])
                        function_to_call = getattr(module, self.intents_data[tag]['function'])

                        for item in self.intents_data[tag]['parameters']['dynamic']:
                            self.intents_data[tag]['parameters']['static'][item] = treated_user_input[item]
                        param = list(self.intents_data[tag]['parameters']['static'].values())
                        # Call the function with parameters unpacked from the list
                        outputs.append(function_to_call(*param))
                else:
                    outputs.append("Sorry, I do not understand your request...")
        print(outputs)
        return outputs
