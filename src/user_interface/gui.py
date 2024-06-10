import json
import os
import threading

import torch
from flask import Flask, render_template, request, jsonify, Response

from modules.chatbot.chatbot import ChatBot
from modules.chatbot.trainer.chat_bot_trainer import ChatBotTrainer
from modules.chatbot.chatbot_test import test_chatbot
from utilities.path_finder import PathFinder


class ChatInterface:
    """
    A Flask web application interface for managing a chatbot system. This class encapsulates setup,
    configuration, and routing logic to handle chat-related functionalities, including interactions,
    training, and model management, while providing a web interface.

    Attributes:
        __chatbot (ChatBot): An instance of the ChatBot class to handle chat functionalities.
        __app (Flask): An instance of the Flask web framework configured for serving the chatbot interface.

    Note:
        The double underscore prefix in method names signifies private methods which should not be accessed
        outside of the class context.
    """

    def __init__(self, **configs: dict):
        """
        Initializes the ChatInterface, sets up the Flask application, and loads necessary resources.

        Parameters:
            **configs (dict): A dictionary of configuration options for the Flask application.
        """
        template = PathFinder().get_complet_path('user_interface/templates/')
        static = PathFinder().get_complet_path('user_interface/static/')
        file = ("bow_lemmatizer.pth")
        self.__chatbot = ChatBot(file)
        self.__app = Flask(__name__, template_folder=template, static_folder=static)
        self.__configs(**configs)
        self.__create_endpoints()
        self.__run()

    def __create_endpoints(self) -> None:
        """
        Sets up and registers the URL endpoints for the Flask application, associating endpoints with their
        respective handling functions.
        """
        self.__add_endpoint('/', 'index', self.__index)
        self.__add_endpoint('/intents', 'intents', self.__intents)
        self.__add_endpoint('/model', 'model', self.__model)
        self.__add_endpoint('/test', 'test', self.__test)
        self.__add_endpoint('/get_response', 'get_response', self.__get_response, ['GET', 'POST'])
        self.__add_endpoint('/load_intents', 'load_intents', self.__load_intents)
        self.__add_endpoint('/load_models', 'load_models', self.__load_models)
        self.__add_endpoint('/train_model', 'train_model', self.__train_model, ['GET', 'POST'])
        self.__add_endpoint("/load_models_filenames", "load_models_filenames", self.__load_models_filenames,
                            ['GET', 'POST'])
        self.__add_endpoint("/change_chatbot_model", "change_chatbot_model", self.__change_chatbot_model, ['GET', 'POST'])
        self.__add_endpoint("/load_tests", "load_tests", self.__load_tests, ['GET', 'POST'])
        self.__add_endpoint("/test_chatbot", "__test_chatbot", self.__test_chatbot, ['GET', 'POST'])

    def __configs(self, **configs: dict) -> None:
        """
        Configures Flask application settings from provided keyword arguments, setting them in the application's
        configuration.

        Parameters:
            **configs (dict): A dictionary of configuration options where the keys are configuration names
                              and the values are settings.
        """
        for config, value in configs:
            self.__app.config[config.upper()] = value

    def __add_endpoint(self, endpoint: str = None, endpoint_name: str = None, handler: callable = None,
                       methods: list = ['GET'], *args, **kwargs) -> None:
        """
        Adds a specific endpoint to the Flask application.

        Parameters:
            endpoint (str): The URL path for the endpoint.
            endpoint_name (str): The name of the endpoint.
            handler (callable): The function to handle requests at the endpoint.
            methods (list, optional): HTTP methods that the endpoint should respond to (e.g., ['GET', 'POST']).
            *args: Additional positional arguments passed to Flask's add_url_rule.
            **kwargs: Additional keyword arguments passed to Flask's add_url_rule.
        """
        self.__app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def __run(self, **kwargs: dict) -> None:
        """
        Starts the Flask application.

        Parameters:
            **kwargs (dict): Keyword arguments for Flask's run method, such as `debug` and `port`.
        """
        self.__app.run(debug=False, **kwargs)

    def __get_response(self) -> list:
        """
        Processes a chat message through the chatbot and returns a response.

        Returns:
            list: A list containing responses from the chatbot based on the input message.
        """
        return self.__chatbot.get_response(request.form["msg"])

    def __load_intents(self) -> str:
        """
        Retrieves and returns the chatbot intents from a JSON file.

        Returns:
            str: JSON formatted string containing intents.
        """
        file_path = PathFinder.get_complet_path("ressources/json_files/intents.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data

    def __load_models(self) -> str:
        """
        Gathers and returns information about all trained models available in the specified directory.

        Returns:
            str: JSON formatted string listing all models and their parameters.
        """
        json_data = {'models': []}
        path = PathFinder.get_complet_path("ressources/models/")
        # Traverse the directory and find all .pth files
        for file in os.listdir(path):
            if file.endswith(".pth"):
                data = torch.load(path + file)
                model_item = {
                    'name': file.removesuffix(".pth"),
                    'parameters': {
                        'modeling': data["modeling_name"],
                        'preprocessing': data["preprocessor"],
                        'extractor': data["extractor"],
                        'stopword': data["remove_stopwords"],
                        'epochs': data["num_epochs"],
                        'batch_size': data["batch_size"],
                        'learning_rate': data["learning_rate"],
                        'hidden_size': data["hidden_size"]
                    }
                }
            else:
                config_path = path+file+"/config.json"
                with open(config_path, 'r') as f:
                    config = json.load(f)

                    model_item = {
                        'name': file,
                        'parameters': {
                            'modeling': config["model_type"],
                            'preprocessing': "None",
                            'extractor': "BERT",
                            'stopword': "None",
                            'epochs': config["num_epochs"],
                            'batch_size': config["batch_size"],
                            'learning_rate': config["learning_rate"],
                            'hidden_size': "None"
                        }
                    }
            json_data['models'].append(model_item)

        # Convert the Python dictionary to a JSON string
        return json.dumps(json_data, indent=4)

    def __load_models_filenames(self) -> Response:
        """
        Retrieves filenames of all trained models available in the models directory.

        Returns:
            Response: A Flask JSON response containing a list of model filenames.
        """
        directory = PathFinder.get_complet_path("ressources/models/")  # Change this to your directory path
        files = os.listdir(directory)
        return jsonify(files)

    def __load_tests(self) -> str:
        """
        Retrieves and returns the chatbot tests from a JSON file.

        Returns:
            str: JSON formatted string containing tests.
        """
        file_path = PathFinder.get_complet_path("ressources/json_files/chatbot_test_result.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data

    def __change_chatbot_model(self) -> str:
        """
        Loads a specified model into the chatbot based on the model filename provided in the request.

        Returns:
            str: Simple text response to confirm the model was loaded.
        """

        self.__chatbot.load_essential(model_file=request.form["filename"])
        return 'ok'

    def __test_chatbot(self):
        # Create a Thread to run the training in the background
        training_thread = threading.Thread(target=test_chatbot,
                                           args=(request.form["filename"],))

        # Start the background thread
        training_thread.start()
        return "Testing started in the background", 202

    def __train_model(self) -> tuple:
        """
        Starts a new thread to train a model with specified parameters from the form data provided in the request.

        Returns:
            Tuple[str, int]: A response message indicating that training has started, with a HTTP status code.
        """
        form = json.loads(request.form["data_forms"])
        data = {}
        for dictio in form:
            data[dictio["name"]] = dictio["value"]

        # Create a Thread to run the training in the background
        training_thread = threading.Thread(target=self.__training,
                                           args=(data["features_extractor"], data["preprocessor"],
                                                 data["stopwords"] == "True", data["modeling"],
                                                 data["model_name"], int(data["num_epochs"]),
                                                 int(data["batch_size"]),
                                                 float(data["learning_rate"]),
                                                 int(data["hidden_size"])))

        # Start the background thread
        training_thread.start()

        # Optionally, return a response immediately to indicate training has started
        return "Training started in the background", 202

    def __training(self, extractor_name: str, preprocessor_name: str, stopwords: bool, modeling_name: str,
                   model_name: str, num_epochs: int, batch_size: int, learning_rate: float, hidden_size: int) -> None:
        """
        Function to run the training process for a chatbot model on a separate thread.

        Parameters:
            extractor_name (str): Name of the feature extractor.
            preprocessor_name (str): Name of the data preprocessor.
            stopwords (bool): Whether to remove stopwords.
            modeling_name (str): Name of the model architecture.
            model_name (str): Desired name for the trained model.
            num_epochs (int): Number of training epochs.
            batch_size (int): Training batch size.
            learning_rate (float): Learning rate for the training.
            hidden_size (int): Size of the hidden layers in the model.
        """
        ChatBotTrainer(extractor_name=extractor_name, preprocessor_name=preprocessor_name, remove_stopwords=stopwords,
                       modeling_name=modeling_name, model_name=model_name, num_epochs=num_epochs, batch_size=batch_size,
                       learning_rate=learning_rate, hidden_size=hidden_size).start_training()

    def __index(self) -> str:
        """
        Returns the main chat interface page template.

        Returns:
            Rendered template: Flask rendered template for the chat interface.
        """
        return render_template('chat.html')

    def __intents(self) -> str:
        """
        Returns the intents management page template.

        Returns:
            Rendered template: Flask rendered template for managing intents.
        """
        return render_template('intents.html')

    def __model(self) -> str:
        """
        Returns the model management page template.

        Returns:
            Rendered template: Flask rendered template for model management.
        """
        return render_template('model.html')

    def __test(self) -> str:
        """
        Returns the testing interface page template.

        Returns:
            Rendered template: Flask rendered template for testing the chatbot.
        """
        return render_template('test.html')
