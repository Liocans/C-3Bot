from modules.NLP.modeling.enhanced_neural_net import EnhancedNeuralNet
from modules.NLP.modeling.neural_net import NeuralNet


class Modeling:

    @staticmethod
    def select_model(model_name: str, input_size: int, hidden_size: int, num_classes: int, device) -> NeuralNet | EnhancedNeuralNet:
        """
        Selects and initializes a neural network model based on the specified model name.

        Parameters:
            model_name (str): The name of the model to be selected.
            input_size (int): The size of the input features.
            hidden_size (int): The size of the hidden layers in the neural network.
            num_classes (int): The number of classes for classification.
            device: The device on which to initialize the model (e.g., "cpu" or "cuda").

        Returns:
            NeuralNet or EnhancedNeuralNet: An instance of the selected neural network model.
        """
        if model_name == "NeuralNet":
            return NeuralNet(input_size=input_size, hidden_size=hidden_size, num_classes=num_classes).to(device=device)

        elif model_name == "EnhancedNeuralNet":
            return EnhancedNeuralNet(input_size=input_size, hidden_size=hidden_size, num_classes=num_classes)
