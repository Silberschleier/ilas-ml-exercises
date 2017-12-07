import numpy as np
from scipy.spatial.distance import cosine
from operator import itemgetter
<<<<<<< HEAD
from tdidt_classification import tdidt, classify_tdidt
=======
from heapq import nsmallest
>>>>>>> 9fbba220ac8628ea25a22cdc953a48016d3b969a


def read_data(path):
    data_labeled = np.genfromtxt(path, delimiter=',')
    data = data_labeled[:, :-1]
    labels = data_labeled[:, -1:]

    return data, labels
    
def convert_data(data_labeled):
    # convert to format suitable for tdidt implementation
    entries = []
    header = list(range(1,len(data_labeled[0]-1)))
    header.append('class_label')
    attribute_values = {attribute: [] for attribute in header}
    for row in data_labeled:
        entries.append({label: float(value) for label, value in zip(header, row)})
        for attribute, value in zip(header, row):
            attribute_values[attribute].append(float(value))
    header.remove('class_label')
    return header, attribute_values, entries


def classify(k, trainings_data, test_data, trainings_labels, test_labels):
    correct_classifications = 0
    for sample_index, sample in enumerate(test_data):
        d = [(i, cosine(trainings_data[i, :], sample)) for i in range(len(trainings_data))]
        neighbours = nsmallest(k, d, key=itemgetter(1))

        positive = 0
        for i, value in neighbours:
            if trainings_labels[i] == 1:
                positive += 1

        classification = 1 if positive > k - positive else 0
        if classification == test_labels[sample_index]:
            correct_classifications += 1

    accuracy = correct_classifications / len(test_data)
    return accuracy


if __name__ == '__main__':
    trainings_data, trainings_labels = read_data('spam_training.csv')
    test_data, test_labels = read_data('spam_test.csv')

    training_means = np.mean(trainings_data, 0)
    training_std = np.std(trainings_data, 0)

    # Normalize
    normalized_trainings_data = np.array(trainings_data) - training_means
    normalized_trainings_data /= training_std
    normalized_test_data = np.array(test_data) - training_means
    normalized_test_data /= training_std

    # kNN classification
    #for k in [1, 3, 5]:
        #accuracy = classify(k, normalized_trainings_data, normalized_test_data, trainings_labels, test_labels)
        #print('Accuracy for k = {}: {}'.format(k, accuracy))
    
    # re-attach labels to the data
    train_data_labeled = np.concatenate((normalized_trainings_data, trainings_labels), axis=1)
    test_data_labeled = np.concatenate((normalized_test_data, test_labels), axis=1)
    
    # TDIDT classification
    depth = 5
    header_train, attribute_values_train, entries_train = convert_data(train_data_labeled)
    tdidt = tdidt(entries_train,  header_train, attribute_values_train, depth)
    print(tdidt)
    header_test, attribute_values_test, entries_test = convert_data(test_data_labeled)
    accuracy_tdidt = classify_tdidt(tdidt, entries_test, header_test, attribute_values_test, test_labels)
    print('Accuracy des Decision Tree mit Tiefe ' + str(depth) + ': ' + str(accuracy_tdidt))

    # Filter attributes for task 4.4
    selected_features = [1, 3]
    filtered_trainings_data = normalized_trainings_data[:, selected_features]
    filtered_test_data = normalized_test_data[:, selected_features]

    print('Task 3:')
    print('-------\n')
    for k in [1, 3, 5]:
        accuracy = classify(k, normalized_trainings_data, normalized_test_data, trainings_labels, test_labels)
        print('Accuracy for k = {}: {}'.format(k, accuracy))

    print('\n\nTask 4.4:')
    print('---------\n')
    for k in []:
        accuracy = classify(k, filtered_trainings_data, filtered_test_data, trainings_labels, test_labels)
        print('Accuracy for k = {}: {}'.format(k, accuracy))
