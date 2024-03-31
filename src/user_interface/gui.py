from flask import Flask, render_template, request, jsonify
import os

from NLP.chatbot.chatbot import ChatBot
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
        self.add_endpoint('/get', 'get_response', self.get_response, ['GET','POST'])

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)

    def get_response(self):
        return self.chatbot.get_response(request.form["msg"])

    def index(self):
        return render_template('chat.html')
