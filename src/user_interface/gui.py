import json
import threading

from flask import Flask, render_template, request
from NLP.chatbot.chatbot import ChatBot
from NLP.features_extractor.extractor import Extractor
from NLP.preprocessing.preprocessor import Preprocessor
from NLP.trainer.chat_bot_trainer import ChatBotTrainer
from utilities.file_searcher import PathFinder


class ChatInterface:

    def __init__(self, **configs):
        template = PathFinder().get_complet_path('user_interface/templates/')
        static = PathFinder().get_complet_path('user_interface/static/')
        FILE = PathFinder().get_complet_path("ressources/model/bow_lemmatizer.pth")
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
        file_path = PathFinder.get_complet_path("ressources/json_files/models.json")
        with open(file_path, 'r', encoding='utf-8') as file:
            data = file.read()
        return data

    def train_model(self):
        form = json.loads(request.form["data_forms"])
        data = {}
        for dictio in form:
            data[dictio["name"]] = dictio["value"]
        model_canvas = {
            "name": data["model_name"],
            "parameters": {
                "modeling": data["modeling"],
                "preprocessing": data["preprocessor"],
                "extractor": data["features_extractor"],
                "stopword": data["stopwords"] == "True",
                "num_epochs": int(data["num_epochs"]),
                "batch_size": int(data["batch_size"]),
                "learning_rate": float(data["learning_rate"]),
                "hidden_size": int(data["hidden_size"]),
            },
            "status": "Complete",
        }
        print(model_canvas)
        model_name = data["model_name"]
        num_epochs = int(data["num_epochs"])
        batch_size = int(data["batch_size"])
        learning_rate = float(data["learning_rate"])
        hidden_size = int(data["hidden_size"])
        preprocessor = Preprocessor(data["preprocessor"], data["stopwords"] == "True")
        extractor = Extractor(preprocessor, data["features_extractor"])
        modeling = data["modeling"]

        # Create a Thread to run the training in the background
        training_thread = threading.Thread(target=self.training, args=(
        extractor, modeling, model_name, num_epochs, batch_size, learning_rate, hidden_size, model_canvas))

        # Start the background thread
        training_thread.start()

        # Optionally, return a response immediately to indicate training has started
        return "Training started in the background", 202

    def training(self, extractor, modeling, model_name, num_epochs, batch_size, learning_rate, hidden_size, model_canvas):
        ChatBotTrainer(extractor=extractor, modeling=modeling, model_name=model_name, num_epochs=num_epochs, batch_size=batch_size, learning_rate=learning_rate,
                       hidden_size=hidden_size, model_canvas=model_canvas).start_training()
    def index(self):
        return render_template('chat.html')

    def intents(self):
        return render_template('intents.html')

    def model(self):
        return render_template('model.html')

    def test(self):
        return render_template('test.html')
