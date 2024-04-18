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
    """
    A class for creating a chatbot that can understand and respond to natural language inputs. It integrates
    feature extraction, preprocessing, and deep learning models to process and respond to user queries.

    Attributes:
        __tags (list): A list of possible tags or categories the bot can recognize.
        __all_words (list): A list of all words the model knows and can recognize.
        __extractor (Extractor): The feature extraction mechanism used to convert text input into a format suitable for the model.
        __model (Modeling): The neural network model that predicts the category of the input.
        __device (torch.device): The computation device (CPU or GPU) on which the model is loaded.
        __intents_data (dict): A dictionary storing the responses and functionalities associated with each intent.
    """

    def __init__(self, model_file: str):
        """
        Initializes the chatbot with a pre-trained model and loads the intents configuration.

        Parameters:
            model_file (str): The path to the pre-trained model file.
        """
        self.__tags = None
        self.__all_words = None
        self.__extractor = None
        self.__model = None
        self.__intents_data = dict()
        self.__device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.load_model(model_file)
        self.__load_intents()

    def __load_intents(self):
        """
        Loads intents data from a JSON file and initializes intent handling configurations.
        """
        file_path = PathFinder().get_complet_path('ressources/json_files/intents.json')
        # Load intents data from JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            for intent in data.get('intents'):
                self.__intents_data[intent['tag']] = {
                    'responses': intent['responses'],
                    'function': intent['function'],
                    'module': intent["module"],
                    "class": intent["class"],
                    "parameters": intent["parameters"]
                }

    def load_model(self, model_file):
        """
         Loads a pre-trained model along with its configuration and necessary data for feature extraction.

         Parameters:
             model_file (str): The path to the file containing the trained model and its metadata.
         """
        data = torch.load(model_file, map_location=self.__device)

        self.__model = Modeling.select_model(model_name=data["modeling_name"], input_size=data["input_size"],
                                               hidden_size=data["hidden_size"], num_classes=data["output_size"],
                                               device=self.__device)

        self.__model.load_state_dict(data["model_state"])
        self.__model.eval()

        self.__extractor = Extractor(preprocessor=Preprocessor(preprocessor_name=data["preprocessor"],
                                                               remove_stopwords=data["remove_stopwords"]),
                                     extractor_name=data[
                                         "extractor"])  # Make sure this matches your actual implementation

        self.__all_words, self.__tags = data["all_words"], data["tags"]

    def get_response(self, user_input: str) -> list:
        """
        Processes an input string to determine and execute an appropriate response based on the model's predictions and the defined intents.

        Parameters:
            user_input (str): The user input text to process.

        Returns:
            list: A list of responses from the chatbot.
        """
        treated_intents = set()
        outputs = []
        treated_user_input = segment_sentences(user_input)
        for sentence in treated_user_input["user_input"]:
            X = self.__extractor.extract_features(sentence)
            X = X.reshape(1, X.shape[0])
            X = torch.from_numpy(X).to(dtype=torch.float).to(self.__device)

            output = self.__model(X)
            _, predicted = torch.max(output, dim=1)

            tag = self.__tags[predicted.item()]
            if tag not in treated_intents:
                probabilities = torch.softmax(output, dim=1)
                prob = probabilities[0][predicted.item()]

                if prob.item() > 0.7:
                    treated_intents.add(tag)
                    outputs.append(np.random.choice(self.__intents_data[tag]['responses']))
                    if (self.__intents_data[tag]['class'] != ""):
                        module = importlib.import_module(self.__intents_data[tag]['module'])
                        class_instance = getattr(module, self.__intents_data[tag]['class'])()
                        function_to_call = getattr(class_instance, self.__intents_data[tag]['function'])

                        for item in self.__intents_data[tag]['parameters']['dynamic']:
                            self.__intents_data[tag]['parameters']['static'][item] = treated_user_input[item]

                        param = list(self.__intents_data[tag]['parameters']['static'].values())
                        # Call the function with parameters unpacked from the list
                        outputs.append(function_to_call(*param))
                    elif (self.__intents_data[tag]['function'] != ""):
                        module = importlib.import_module(self.__intents_data[tag]['module'])
                        function_to_call = getattr(module, self.__intents_data[tag]['function'])

                        for item in self.__intents_data[tag]['parameters']['dynamic']:
                            self.__intents_data[tag]['parameters']['static'][item] = treated_user_input[item]
                        param = list(self.__intents_data[tag]['parameters']['static'].values())
                        # Call the function with parameters unpacked from the list
                        outputs.append(function_to_call(*param))
                else:
                    outputs.append("Sorry, I do not understand your request...")

        return outputs
