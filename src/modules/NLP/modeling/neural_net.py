import torch.nn as nn


class NeuralNet(nn.Module):
    """
    A simple feedforward neural network with three layers, designed for classification tasks. It uses ReLU as the
    activation function between layers to introduce non-linearity.

    Attributes:
        l1 (nn.Linear): The first linear layer.
        l2 (nn.Linear): The second linear layer.
        l3 (nn.Linear): The third linear layer which outputs the logits for each class.
        relu (nn.ReLU): The ReLU activation function used between layers.

    Methods:
        forward(x): Defines the forward pass of the model.
    """

    def __init__(self, input_size: int = None, hidden_size: int = None, num_classes: int = None):
        """
        Initializes the NeuralNet model with specified sizes for input, hidden, and output layers.

        Parameters:
            input_size (int, optional): The number of input features. Defaults to None.
            hidden_size (int, optional): The number of features in the hidden layers. Defaults to None.
            num_classes (int, optional): The number of classes for the output layer. Defaults to None.
        """
        super(NeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, features):
        """
        Performs a forward pass through the network with ReLU activations after each of the first two linear layers.

        Parameters:
            features (torch.Tensor): The input tensor containing features for which predictions are to be made.

        Returns:
            torch.Tensor: The output tensor containing logits for each class before the softmax activation.
        """
        out = self.l1(features)
        out = self.relu(out)
        out = self.l2(out)
        out = self.relu(out)
        out = self.l3(out)
        # no activation and no softmax at the end
        return out

    @property
    def modeling_name(self) -> str:
        """
        Provides the name of the model configuration, which can be useful for dynamic model loading or logging.

        Returns:
            str: The name of the model, "NeuralNet".
        """
        return "NeuralNet"
