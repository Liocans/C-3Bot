from flask import Flask, render_template, request, jsonify
import os


class ChatInterface:

    def __init__(self, **configs):
        template = os.path.abspath('user_interface/templates/')
        static = os.path.abspath('user_interface/static/')
        self.app = Flask(__name__, template_folder=template, static_folder=static)
        self.configs(**configs)
        self.create_endpoints()
        self.run()

    def create_endpoints(self):
        self.add_endpoint('/', 'index', self.index)

    def configs(self, **configs):
        for config, value in configs:
            self.app.config[config.upper()] = value

    def add_endpoint(self, endpoint=None, endpoint_name=None, handler=None, methods=['GET'], *args, **kwargs):
        self.app.add_url_rule(endpoint, endpoint_name, handler, methods=methods, *args, **kwargs)

    def run(self, **kwargs):
        self.app.run(**kwargs)

    def index(self):
        return render_template('chat.html')
