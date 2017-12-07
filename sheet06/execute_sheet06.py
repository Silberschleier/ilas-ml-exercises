import numpy as np
from scipy.spatial.distance import cosine
from operator import itemgetter
from itertools import product
from pprint import pprint

if __name__ == '__main__':
    k = 3
    trainings_data_labeled = np.genfromtxt('test.csv', delimiter=',')
    trainings_data = trainings_data_labeled[:, :-1]
    trainings_labels = trainings_data_labeled[:, -1:]
    print(trainings_labels)
    training_means = np.mean(trainings_data, 0)
    training_std = np.std(trainings_data, 0)
    normalized_trainings_data = np.array(trainings_data) - training_means

    normalized_trainings_data /= training_std

    print(normalized_trainings_data)
    print()
    print(normalized_trainings_data[:, :-1])
    classifications = []

    for sample_index, sample in enumerate(normalized_trainings_data):
        d = [(i, cosine(normalized_trainings_data[i, :], sample)) for i in range(len(normalized_trainings_data))]
        d.sort(key=itemgetter(1))
        neighbours = d[:k+1]

        positive = 0
        print(neighbours)
        for i, value in neighbours:
            if trainings_labels[i] == 1 and i != sample_index:
                positive += 1
        print(positive)
