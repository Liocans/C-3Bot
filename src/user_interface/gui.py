import json
import os
import threading

import torch
from flask import Flask, render_template, request, jsonify

from modules.NLP.chatbot.chatbot import ChatBot
from modules.NLP.trainer.chat_bot_trainer import ChatBotTrainer
from utilities.path_finder import PathFinder


class ChatInterface:

    def __init__(self, **configs):
        template = PathFinder().get_complet_path('user_interface/templates/')
        static = PathFinder().get_complet_path('user_interface/static/')
        FILE = PathFinder().get_complet_path("ressources/models/bow_lemmatizer.pth")
        self.chatbot = ChatBot(FILE)
        self.app = Flask(__name__, template_folder=template, static_folder=static)
        self.configs(**configs)
        self.create_endpoints()
        self.run()

    def create_endpoints(self):
        self.add_endpoint('/', 'index', self.index)
        self.add_endpoint('/intents', 'intents', self.intents)
        self.add_endpoint('/model', 'model', self.model)
        self.add_endpoint('/test', 'test', self.test)
        self.add_endpoint('/get_response', 'get_response', self.get_response, ['GET', 'POST'])
        self.add_endpoint('/get_intents', 'get_intents', self.get_intents)
        self.add_endpoint('/get_models', 'get_models', self.get_models)
        self.add_endpoint('/train_model', 'train_model', self.train_model, ['GET', 'POST'])
        self.add_endpoint("/get_models_filenames","get_models_filenames",self.get_models_filenames,['GET', 'POST'])
        self.add_endpoint("/load_model", "load_model", self.load_model, ['GET', 'POST'])

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(debug=True, **kwargs)

    def get_response(self) -> list:
        return self.chatbot.get_response(request.form["msg"])

    def get_intents(self) -> str:
        file_path = PathFinder.get_complet_path("ressources/json_files/intents.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data

    def get_models(self) -> str:
        json_data = {'models':[]}
        path = PathFinder.get_complet_path("ressources/models/")
        # Traverse the directory and find all .pth files
        for file in os.listdir(path):
            if file.endswith(".pth"):
                data = torch.load(path+file)
                model_item = {
                    'name': file.removesuffix(".pth"),
                    'parameters': {
                        'modeling': data["modeling_name"],
                        'preprocessing': data["preprocessor"],
                        'extractor': data["extractor"],
                        'stopword': data["remove_stopwords"],  # or False
                        'epochs': data["num_epochs"],
                        'batch_size': data["batch_size"],
                        'learning_rate': data["learning_rate"],
                        'hidden_size': data["hidden_size"]
                    }
                }
                json_data['models'].append(model_item)

        # Convert the Python dictionary to a JSON string
        return json.dumps(json_data, indent=4)

    def get_models_filenames(self):
        directory = PathFinder.get_complet_path("ressources/models/")  # Change this to your directory path
        files = os.listdir(directory)
        files = [file.removesuffix(".pth") for file in files]
        return jsonify(files)

    def load_model(self):
        self.chatbot.load_model(model_file=PathFinder.get_complet_path("ressources/models/"+request.form["filename"]+".pth"))
        return 'ok'

    def train_model(self):
        form = json.loads(request.form["data_forms"])
        data = {}
        for dictio in form:
            data[dictio["name"]] = dictio["value"]

        # Create a Thread to run the training in the background
        training_thread = threading.Thread(target=self.training, args=(data["features_extractor"], data["preprocessor"],
                                                                       data["stopwords"] == "True", data["modeling"],
                                                                       data["model_name"], int(data["num_epochs"]),
                                                                       int(data["batch_size"]),
                                                                       float(data["learning_rate"]),
                                                                       int(data["hidden_size"])))

        # Start the background thread
        training_thread.start()

        # Optionally, return a response immediately to indicate training has started
        return "Training started in the background", 202

    def training(self, extractor_name, preprocessor_name, stopwords, modeling_name, model_name, num_epochs, batch_size,
                 learning_rate, hidden_size):
        ChatBotTrainer(extractor_name=extractor_name, preprocessor_name=preprocessor_name, stopwords=stopwords,
                       modeling_name=modeling_name, model_name=model_name, num_epochs=num_epochs, batch_size=batch_size,
                       learning_rate=learning_rate, hidden_size=hidden_size).start_training()

    def index(self):
        return render_template('chat.html')

    def intents(self):
        return render_template('intents.html')

    def model(self):
        return render_template('model.html')

    def test(self):
        return render_template('test.html')
