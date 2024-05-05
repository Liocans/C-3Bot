import torch.nn as nn


class EnhancedNeuralNet(nn.Module):
    """
    An enhanced feedforward neural network for classification tasks, featuring batch normalization and dropout.

    Attributes:
        l1 (nn.Linear): The first linear layer.
        bn1 (nn.BatchNorm1d): Batch normalization for the first layer.
        l2 (nn.Linear): The second linear layer.
        bn2 (nn.BatchNorm1d): Batch normalization for the second layer.
        l3 (nn.Linear): The output linear layer.
        relu (nn.ReLU): The ReLU activation function.
        dropout (nn.Dropout): Dropout layer to reduce overfitting.

    Methods:
        forward(x): Defines the forward pass of the model.
    """

    def __init__(self, input_size: int = None, hidden_size: int = None, num_classes: int = None,
                 dropout_rate: float = 0.5):
        """
        Initializes the EnhancedNeuralNet model with specified sizes for input, hidden, output layers, and dropout rate.

        Parameters:
            input_size (int, optional): The number of input features.
            hidden_size (int, optional): The number of features in the hidden layers.
            num_classes (int, optional): The number of classes for the output layer.
            dropout_rate (float, optional): The dropout rate used after each activation function to prevent overfitting.
        """
        super(EnhancedNeuralNet, self).__init__()
        self.l1 = nn.Linear(input_size, hidden_size)
        self.bn1 = nn.BatchNorm1d(hidden_size)
        self.l2 = nn.Linear(hidden_size, hidden_size)
        self.bn2 = nn.BatchNorm1d(hidden_size)
        self.dropout = nn.Dropout(dropout_rate)
        self.l3 = nn.Linear(hidden_size, num_classes)
        self.relu = nn.ReLU()

    def forward(self, features):
        """
        Performs a forward pass through the network, applying batch normalization before activation and dropout after activation.

        Parameters:
            features (torch.Tensor): The input tensor containing features for predictions.

        Returns:
            torch.Tensor: The output tensor containing logits for each class.
        """
        out = self.l1(features)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.l2(out)
        out = self.bn2(out)
        out = self.relu(out)
        out = self.dropout(out)
        out = self.l3(out)
        return out

    @property
    def modeling_name(self) -> str:
        """
        Provides the name of the model configuration, which can be useful for dynamic model loading or logging.

        Returns:
            str: The name of the model, "EnhancedNeuralNet".
        """
        return "EnhancedNeuralNet"

