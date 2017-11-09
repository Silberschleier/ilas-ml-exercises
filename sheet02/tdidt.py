import csv
from math import log
from operator import itemgetter
from pprint import pprint
from .visualization import *


def read_data(path):
    entries = []
    with open(path) as fp:
        datareader = csv.reader(fp, delimiter=',')
        header = next(datareader)
        attribute_values = {attribute: [] for attribute in header}
        for row in datareader:
            entries.append({label: float(value) for label, value in zip(header, row)})
            for attribute, value in zip(header, row):
                attribute_values[attribute].append(float(value))
    header.remove('class_label')
    return header, attribute_values, entries


def _is_perfectly_classified(samples):
    value = samples[0]['class_label']
    for s in samples:
        if s['class_label'] != value:
            return False
    return True


def _pos_classification_count(samples):
    positive = 0
    for sample in samples:
        if sample['class_label'] == 1:
            positive += 1
    return positive


def _pos_classification_fraction(samples):
    positive = _pos_classification_count(samples)
    # avoid division by 0
    if len(samples) == 0:
        res = 0
    else:
        res = positive / len(samples)
    return res


def _entropy(samples, sample_subset, pos_fraction):
    # avoid division by 0
    if pos_fraction == 0 or pos_fraction == 1:
        return 0
    return (len(sample_subset) / len(samples)) * ((pos_fraction * log(1 / pos_fraction, 2)) + ((1 - pos_fraction) * log(1 / (1 - pos_fraction), 2)))


def _split_samples(samples, attribute, threshold):
    samples_below = [x for x in samples if x[attribute] <= threshold]
    samples_above = [x for x in samples if x[attribute] > threshold]
    return samples_below, samples_above


def _inverted_gain(samples, attribute, threshold):
    samples_below, samples_above = _split_samples(samples, attribute, threshold)
    _pos_below_frac = _pos_classification_fraction(samples_below)
    _pos_above_frac = _pos_classification_fraction(samples_above)

    return _entropy(samples, samples_below, _pos_below_frac) + _entropy(samples, samples_above, _pos_above_frac)


def tdidt(samples, attributes, attribute_values, max_depth):
    count_positive = _pos_classification_count(samples)
    count_negative = len(samples) - count_positive
    if _is_perfectly_classified(samples):
        return {'value': samples[0]['class_label'], 'left': None, 'right': None, 'samples': len(samples), 'pos_samples': count_positive, 'neg_samples': count_negative}

    if max_depth == 0:
        if count_positive >= count_negative:
            value = 1.0
        else:
            value = 0.0
        return {'value': value, 'left': None, 'right': None, 'samples': len(samples), 'pos_samples': count_positive, 'neg_samples': count_negative}


    candidates = []
    for attribute in attributes:
        for threshold in attribute_values[attribute]:
            candidates.append((attribute, threshold, _inverted_gain(samples, attribute, threshold)))

    best_attribute, best_threshold, best_gain = min(candidates, key=itemgetter(2))
    samples_below, samples_above = _split_samples(samples, best_attribute, best_threshold)

    return {
        'attribute': best_attribute,
        'threshold': best_threshold,
        'gain': best_gain,
        'samples': len(samples), 'pos_samples': count_positive, 'neg_samples': count_negative,
        'left': tdidt(samples_below, attributes, attribute_values, max_depth-1),
        'right': tdidt(samples_above, attributes, attribute_values, max_depth-1)
    }
    

def _is_leaf(tree):
    return (tree['left'] == None and tree['right'] == None)
    
    
def classify_one_sample(tree, sample, sample_index, attributes, attribute_values):
    if _is_leaf(tree) == True:
        return tree['value']
    else:
        if attribute_values[tree['attribute']][sample_index] <= tree['threshold']:
            return classify_one_sample(tree['left'], sample, sample_index, attributes, attribute_values)
        else:
            return classify_one_sample(tree['right'], sample, sample_index, attributes, attribute_values)
    
    
def classify(tree, samples, attributes, attribute_values):
    res = []
    for i in range(len(samples)):
        res.append(classify_one_sample(tree, samples[i], i, attributes, attribute_values))
    return res
    
    
def _accuracy(result, class_labels):
    true_classified = 0
    for i in range(len(result)):
        if result[i] == class_labels[i]:
            true_classified += 1
    return true_classified / len(result)
    
    
if __name__ == '__main__':
    header, attribute_values, entries = read_data("data/gene_expression_training.csv")
    tree = tdidt(entries, header, attribute_values, 4)

    generate_dot_from_graph(tree, 'output.dot')
    #pprint(tree)
    
    header_test, attribute_values_test, entries_test = read_data("data/gene_expression_test.csv")
    res = classify(tree, entries_test, header_test, attribute_values_test)
    #print(res)
    class_labels = []
    for entry in entries_test:
        class_labels.append(entry['class_label'])
    #print(class_labels)
    print("Accuracy: " + str(_accuracy(res, class_labels)))