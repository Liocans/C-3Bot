from modules.NLP.modeling.neural_net import NeuralNet


class Modeling():

    def select_model(self, model_name, input_size, hidden_size, num_classes, device):
        if model_name == "NeuralNet":
            return NeuralNet(input_size, hidden_size, num_classes).to(device=device)
