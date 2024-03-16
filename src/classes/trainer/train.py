import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from classes.extractor.bag_of_words import BagOfWords
from classes.modeling.neural_net import NeuralNet


class ChatDataset(Dataset):

    def __init__(self, num_epochs=1000, batch_size=8, learning_rate=0.001, hidden_size=8):
        self.bag_of_words = BagOfWords()
        self.num_epochs = num_epochs
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.hidden_size = hidden_size
        self.n_samples = 0
        self.x_train = []
        self.y_train = []
        self.input_size = 0
        self.output_size = 0
        self.create_train_set()

    def create_train_set(self):
        for (sentence, tag) in self.bag_of_words.train_x_y:
            # X: bag of words for each pattern_sentence
            bag = self.bag_of_words.generate_bow(sentence)
            self.x_train.append(bag)
            # y: PyTorch CrossEntropyLoss needs only class labels, not one-hot
            label = self.bag_of_words.tags.index(tag)
            self.y_train.append(label)

        self.x_train = np.array(self.x_train)
        self.y_train = np.array(self.y_train)

        self.input_size = len(self.x_train[0])
        self.output_size = len(self.bag_of_words.tags)
        self.n_samples = len(self.x_train)

    # support indexing such that dataset[i] can be used to get i-th sample
    def __getitem__(self, index):
        return self.x_train[index], self.y_train[index]

    # we can call len(dataset) to return the size
    def __len__(self):
        return self.n_samples

if __name__ == '__main__':

    dataset = ChatDataset()
    train_loader = DataLoader(dataset=dataset,
                              batch_size=dataset.batch_size,
                              shuffle=True,
                              num_workers=0)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = NeuralNet(dataset.input_size, dataset.hidden_size, dataset.output_size).to(device)

    # Loss and optimizer
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=dataset.learning_rate)

    # Train the modeling
    for epoch in range(dataset.num_epochs):
        for (words, labels) in train_loader:
            words = words.to(dtype=torch.float).to(device)
            labels = labels.to(dtype=torch.long).to(device)

            # Forward pass
            outputs = model(words)
            # if y would be one-hot, we must apply
            # labels = torch.max(labels, 1)[1]
            loss = criterion(outputs, labels)

            # Backward and optimize
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        if (epoch + 1) % 100 == 0:
            print(f'Epoch [{epoch + 1}/{dataset.num_epochs}], Loss: {loss.item():.4f}')

    print(f'final loss: {loss.item():.4f}')

    data = {
        "model_state": model.state_dict(),
        "input_size": dataset.input_size,
        "hidden_size": dataset.hidden_size,
        "output_size": dataset.output_size,
        "all_words": dataset.bag_of_words.vocab,
        "tags": dataset.bag_of_words.tags
    }

    FILE = "../../ressources/model/data.pth"
    torch.save(data, FILE)

    print(f'training complete. file saved to {FILE}')
