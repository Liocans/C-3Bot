from modules.NLP.modeling.neural_net import NeuralNet


class Modeling:

    @staticmethod
    def select_model(modeling_name: str, input_size: int, hidden_size: int, num_classes: int, device) -> NeuralNet:
        """
        Selects and initializes a neural network model based on the specified model name.

        Parameters:
            modeling_name (str): The name of the model to be selected.
            input_size (int): The size of the input features.
            hidden_size (int): The size of the hidden layers in the neural network.
            num_classes (int): The number of classes for classification.
            device: The device on which to initialize the model (e.g., "cpu" or "cuda").

        Returns:
            NeuralNet : An instance of the selected neural network model.
        """
        if modeling_name == "NeuralNet":
            return NeuralNet(input_size=input_size, hidden_size=hidden_size, num_classes=num_classes).to(device=device)
