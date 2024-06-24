import torch
import string
import unicodedata

class NameData:
    allowed_characters = string.ascii_lowercase
    n_letters = len(allowed_characters)


    def __init__(self, label, text):
        self.label = label
        self.text = NameData.unicodeToAscii(text)
        self.tensor =  NameData.lineToTensor(self.text)

    def __str__(self):
        return f"label={self.label}, text={self.text}\ntensor = {self.tensor}"

    # Turn a Unicode string to plain ASCII, thanks to https://stackoverflow.com/a/518232/2809427
    def unicodeToAscii(s):
        return ''.join(
            c for c in unicodedata.normalize('NFD', s)
            if unicodedata.category(c) != 'Mn'
            and c in NameData.allowed_characters
        )

    # Find letter index from all_letters, e.g. "a" = 0
    def letterToIndex(letter):
        return NameData.allowed_characters.find(letter)

    # Turn a line into a <line_length x 1 x n_letters>,
    # or an array of one-hot letter vectors
    def lineToTensor(line):
        tensor = torch.zeros(len(line), 1, NameData.n_letters)
        for li, letter in enumerate(line):
            tensor[li][0][NameData.letterToIndex(letter)] = 1
        return tensor

from io import open
import glob
import os
import unicodedata
import string
import time

import torch
from torch.utils.data import Dataset

class NamesDataset(Dataset):

    def __init__(self, data_dir):
        self.data_dir = data_dir #for provenance of the dataset
        self.load_time = time.localtime #for provenance of the dataset
        labels_set = set() #set of all classes

        self.data = []

        #read all the txt files in the specified directory
        text_files = glob.glob(os.path.join(data_dir, '*.txt'))
        for filename in text_files:
            label = os.path.splitext(os.path.basename(filename))[0]
            labels_set.add(label)
            lines = NamesDataset.readLines(filename)
            for name in lines:
                if len(name) > 0:
                    self.data.append(NameData(label=label, text=name))

        self.labels = list(labels_set)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        data_item = self.data[idx]
        label_tensor = torch.tensor([self.labels.index(data_item.label)], dtype=torch.long)
        return label_tensor, data_item.tensor, data_item.label, data_item.text

    # Read a file and split into lines
    def readLines(filename):
        lines = open(filename, encoding='utf-8').read().strip().split('\n')
        return lines

import torch.nn as nn
import torch.nn.functional as F
import random

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_labels, criterion = nn.NLLLoss()):
        super(RNN, self).__init__()

        self.hidden_size = hidden_size
        self.output_labels = output_labels

        self.i2h = nn.Linear(input_size, hidden_size)
        self.h2h = nn.Linear(hidden_size, hidden_size)
        self.h2o = nn.Linear(hidden_size, len(output_labels))
        self.softmax = nn.LogSoftmax(dim=1)

        self.criterion = criterion

    def initHidden(self):
        return torch.zeros(1, self.hidden_size)

    def forward(self, input, hidden):
        hidden = F.tanh(self.i2h(input) + self.h2h(hidden))
        output = self.h2o(hidden)
        output = self.softmax(output)
        return output, hidden

    def forward_multi(self, line_tensor):
        hidden = self.initHidden()

        for i in range(line_tensor.size()[0]):
            output, hidden = self.forward(line_tensor[i], hidden)

        return output, hidden

    def label_from_output(self, output):
        top_n, top_i = output.topk(1)
        label_i = top_i[0].item()
        return self.output_labels[label_i], label_i

    def learn_single(self, label_tensor, line_tensor, learning_rate = 0.005):
        #Train the RNN for one example with a learning rate that defaults to 0.005.
        rnn.zero_grad()
        output, hidden = self.forward_multi(line_tensor)

        loss = self.criterion(output, label_tensor)
        loss.backward()

        # Add parameters' gradients to their values, multiplied by learning rate
        for p in self.parameters():
            p.data.add_(p.grad.data, alpha=-learning_rate)

        return output, loss.item()

    def learn_batch(self, training_data, n_iters = 1000, report_every = 100):
        """
        Learn on a batch of training_data for a specified number of iterations and reporting thresholds
        """

        # Keep track of losses for plotting
        current_loss = 0
        all_losses = []

        start = time.time()
        print(f"training data = {training_data}")
        print(f"size = {len(training_data)}")

        for iter in range(1, n_iters + 1):
            rand_idx = random.randint(0,len(training_data)-1)
            (label_tensor, text_tensor, label, text) = training_data[rand_idx]
            #print(f"learning on {label} => {text}")
            output, loss = self.learn_single(label_tensor, text_tensor)
            current_loss += loss

            # Print ``iter`` number, loss, name and guess
            if iter % report_every == 0:
                all_losses.append(current_loss / report_every)
                print(f"{iter} ({iter / n_iters:.0%}): \t iteration loss = {all_losses[-1]}")
                current_loss = 0

        return all_losses


import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def evaluate(rnn, testing_data):
    confusion = torch.zeros(len(rnn.output_labels), len(rnn.output_labels))

    with torch.no_grad(): # do not record the gradiants during eval phase
        for i in range(len(testing_data)):
            (label_tensor, text_tensor, label, text) = testing_data[i]
            (output, hidden) = rnn.forward_multi(text_tensor)
            guess, guess_i = rnn.label_from_output(output)
            label_i = rnn.output_labels.index(label)
            confusion[label_i][guess_i] += 1

    # Normalize by dividing every row by its sum
    for i in range(len(rnn.output_labels)):
        confusion[i] = confusion[i] / confusion[i].sum()

    # Set up plot
    fig = plt.figure()
    ax = fig.add_subplot(111)
    cax = ax.matshow(confusion.numpy())
    fig.colorbar(cax)

    # Set up axes
    ax.set_xticklabels([''] + rnn.output_labels, rotation=90)
    ax.set_yticklabels([''] + rnn.output_labels)

    # Force label at every tick
    ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
    ax.yaxis.set_major_locator(ticker.MultipleLocator(1))

    # sphinx_gallery_thumbnail_number = 2
    plt.show()

if __name__ == "__main__":

    alldata = NamesDataset("data/learning")
    print(f"loaded {len(alldata)} items of data")
    print(f"example = {alldata[0]}")

    train_set, test_set = torch.utils.data.random_split(alldata, [.8, .2])
    print(f"train examples = {len(train_set)}, validation examples = {len(test_set)}")

    n_hidden = NameData.n_letters
    hidden = torch.zeros(1, n_hidden)
    rnn = RNN(NameData.n_letters, n_hidden, alldata.labels)

    all_losses = rnn.learn_batch(train_set, n_iters=10000, report_every=1000)

    plt.figure()
    plt.plot(all_losses)
    plt.show()

    evaluate(rnn, test_set)