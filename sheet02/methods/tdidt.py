import csv
from .classification import classify, accuracy
from math import log
from operator import itemgetter


# Nodes and leafs of the tree are structs in the form:
# {
# 'value': classifikation of the leaf or None for Node
# 'attribute': splitAttribut or None for leaf
# 'threshold': splitTreshold or None for leaf
# 'gain': splitGain or None for leaf
# 'samples': number of samples from training
# 'pos_samples': number of positive samples from training
# 'neg_samples': number of negative samples from training
# 'samples_test': number of samples from test
# 'pos_samples_test': number of positive samples from test
# 'neg_samples_test': number of negative samples from test
# 'left': left childTree or None for leaf
# 'right': right childTree or None for leaf
# }


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
    return (len(sample_subset) / len(samples)) * (
    (pos_fraction * log(1 / pos_fraction, 2)) + ((1 - pos_fraction) * log(1 / (1 - pos_fraction), 2)))


def _split_samples(samples, attribute, threshold):
    samples_below = [x for x in samples if x[attribute] <= threshold]
    samples_above = [x for x in samples if x[attribute] > threshold]
    return samples_below, samples_above


def _inverted_gain(samples, attribute, threshold):
    samples_below, samples_above = _split_samples(samples, attribute, threshold)
    _pos_below_frac = _pos_classification_fraction(samples_below)
    _pos_above_frac = _pos_classification_fraction(samples_above)

    return _entropy(samples, samples_below, _pos_below_frac) + _entropy(samples, samples_above, _pos_above_frac)


def _majority_class(pos_samples, neg_samples):
    if pos_samples >= neg_samples:
        return 1.0
    else:
        return 0.0

def tdidt(samples, attributes, attribute_values, max_depth):
    count_positive = _pos_classification_count(samples)
    count_negative = len(samples) - count_positive
    if _is_perfectly_classified(samples):
        return {'value': samples[0]['class_label'], 'left': None, 'right': None, 'samples': len(samples),
                'pos_samples': count_positive, 'neg_samples': count_negative, 'attribute': None, 'threshold': None,
                'gain': None, 'samples_test': None, 'pos_samples_test': None, 'neg_samples_test': None}

    if max_depth == 0:
        value = _majority_class(count_positive, count_negative)
        return {'value': value, 'left': None, 'right': None, 'samples': len(samples), 'pos_samples': count_positive,
                'neg_samples': count_negative, 'attribute': None, 'threshold': None, 'gain': None, 'samples_test': None,
                'pos_samples_test': None, 'neg_samples_test': None}

    candidates = []
    for attribute in attributes:
        for threshold in attribute_values[attribute]:
            candidates.append((attribute, threshold, _inverted_gain(samples, attribute, threshold)))

    best_attribute, best_threshold, best_gain = min(candidates, key=itemgetter(2))
    samples_below, samples_above = _split_samples(samples, best_attribute, best_threshold)

    return {
        'value': None,  # Added for converting Node to leaf
        'attribute': best_attribute,
        'threshold': best_threshold,
        'gain': best_gain,
        'samples': len(samples), 'pos_samples': count_positive, 'neg_samples': count_negative,
        'samples_test': None, 'pos_samples_test': None, 'neg_samples_test': None,
        'left': tdidt(samples_below, attributes, attribute_values, max_depth - 1),
        'right': tdidt(samples_above, attributes, attribute_values, max_depth - 1)
    }


def count_samples_recursive(tree):
    if tree['value'] is not None:
        countingRight = 0
        if tree['value'] == 0.0:
            countingRight += tree['neg_samples']
        if tree['value'] == 1.0:
            countingRight += tree['pos_samples']
        return countingRight
    else:
        return count_samples_recursive(tree['left']) + count_samples_recursive(tree['right'])


def reduced_error_pruning(tree, subtree, samples, attributes, attribute_values, class_labels):
    # recursive postOrder:
    if subtree['left'] is not None:
        reduced_error_pruning(tree, subtree['right'], samples, attributes, attribute_values, class_labels)
    if subtree['right'] is not None:
        reduced_error_pruning(tree, subtree['left'], samples, attributes, attribute_values, class_labels)

    if subtree['right'] is not None and subtree['left'] is not None:
        majority = _majority_class(subtree['pos_samples'], subtree['neg_samples'])
        classification_unpruned = classify(tree, samples, attributes, attribute_values)

        unpruned_backup = dict(subtree)     # Well, nobody said the solution should be elegant, right?
        subtree.update({'value': majority, 'left': None, 'right': None, 'samples': subtree['pos_samples'] + subtree['neg_samples'],
                       'pos_samples': subtree['pos_samples'], 'neg_samples': subtree['neg_samples']})
        classification_pruned = classify(tree, samples, attributes, attribute_values)

        if accuracy(classification_pruned, class_labels) < accuracy(classification_unpruned, class_labels):
            subtree.update(unpruned_backup)


def postOrder(tree):
    if (tree['right'] != None):
        postOrder(tree['right'])
    if (tree['left'] != None):
        postOrder(tree['left'])
    _test(tree)  # Testfunktion zur Verifizierung der richtigen Reihenfolge


def _test(tree):
    if tree['left'] is None and tree['right'] is None:
        print('Leaf with value ' + str(tree['value']))
    else:
        print('Node with attribute ' + str(tree['attribute']))
