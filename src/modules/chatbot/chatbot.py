import json
import os

import numpy as np
import torch
import importlib

from modules.NLP.features_extractor.extractor import Extractor
from modules.NLP.modeling.BERT import BertIntentClassifier
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
        self.__extractor = None
        self.__model = None
        self.__intents_data = dict()
        self.__device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.__modeling_name = None
        self.load_essential(model_file)
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

    def load_essential(self, model_file):
        """
         Loads a pre-trained model along with its configuration and necessary data for feature extraction.

         Parameters:
             model_file (str): The name of the file containing the trained model and its metadata.
         """

        path_file = PathFinder.get_complet_path("ressources/models/" + model_file)

        if (os.path.isdir(path_file)):
            self.__modeling_name = "BERT"
            self.__model = BertIntentClassifier(model_name=model_file)
            self.__model.load_model()

        else:
            data = torch.load(path_file, map_location=self.__device)
            self.__modeling_name = data["modeling_name"]

            self.__model = Modeling.select_model(modeling_name=data["modeling_name"], input_size=data["input_size"],
                                                 hidden_size=data["hidden_size"], num_classes=data["output_size"],
                                                 device=self.__device)
            self.__model.load_state_dict(data["model_state"])
            self.__model.eval()

            preprocessor = Preprocessor(preprocessor_name=data["preprocessor"], remove_stopwords=data["remove_stopwords"])
            self.__extractor = Extractor(preprocessor=preprocessor, extractor_name=data["extractor"], vocab=data["vocab"],
                                         docs=data["docs"], tags=data["tags"], window=data["window"], vector_size=data["vector_size"],
                                         model_name=model_file)


    def predict_tag(self, sentence):
        """
        Determines the tag of a given sentence using a deep learning model.

        This function is specifically added to facilitate testing the comprehension and response capabilities
        of chatbots during their testing phase. It transforms the input sentence into numerical features
        via a feature extractor, reshapes these features to be compatible with the model, and then feeds
        the data to the model to obtain an intent prediction.

        Args:
            sentence (str): The sentence for which the intent needs to be determined.

        Returns:
            str: The predicted intent for the given sentence, corresponding to one of the pre-trained
                 labels of the model.

        Note:
            This function is part of the testing tools and is not intended for use in production
            applications.
        """

        if(self.__modeling_name=="BERT"):
            print(sentence)
            return self.__model.predict(text=sentence)

        X = self.__extractor.extract_features(sentence)
        X = X.reshape(1, X.shape[0])
        X = torch.from_numpy(X).to(dtype=torch.float).to(self.__device)

        output = self.__model(X)
        _, predicted = torch.max(output, dim=1)

        probabilities = torch.softmax(output, dim=1)
        prob = probabilities[0][predicted.item()]

        return self.__extractor.tags[predicted.item()] if prob.item() > 0.7 else ""

    def get_response(self, user_input: str) -> list:
        """
        Processes an input string to determine and execute an appropriate response based on the model's predictions and the defined intents.

        Parameters:
            user_input (str): The user input text to process.

        Returns:
            list: A list of responses from the chatbot.
        """
        treated_tags = []
        outputs = []
        treated_user_input = segment_sentences(user_input)
        for sentence in treated_user_input["user_input"]:

            predicted_tag = self.predict_tag(sentence)
            if predicted_tag not in treated_tags:

                if predicted_tag != "":
                    treated_tags.append(predicted_tag)
                    outputs.append(np.random.choice(self.__intents_data[predicted_tag]['responses']))

                    if self.__intents_data[predicted_tag]['class'] != "":
                        module = importlib.import_module(self.__intents_data[predicted_tag]['module'])
                        class_instance = getattr(module, self.__intents_data[predicted_tag]['class'])()
                        function_to_call = getattr(class_instance, self.__intents_data[predicted_tag]['function'])

                        for item in self.__intents_data[predicted_tag]['parameters']['dynamic']:
                            self.__intents_data[predicted_tag]['parameters']['static'][item] = treated_user_input[item]

                        param = list(self.__intents_data[predicted_tag]['parameters']['static'].values())
                        # Call the function with parameters unpacked from the list
                        outputs.append(function_to_call(*param))

                    elif self.__intents_data[predicted_tag]['function'] != "":
                        module = importlib.import_module(self.__intents_data[predicted_tag]['module'])
                        function_to_call = getattr(module, self.__intents_data[predicted_tag]['function'])

                        for item in self.__intents_data[predicted_tag]['parameters']['dynamic']:
                            self.__intents_data[predicted_tag]['parameters']['static'][item] = treated_user_input[item]
                        param = list(self.__intents_data[predicted_tag]['parameters']['static'].values())
                        # Call the function with parameters unpacked from the list
                        outputs.extend(function_to_call(*param))

                else:
                    outputs.append("Sorry, I do not understand your request...")

        return outputs
