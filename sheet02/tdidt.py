import csv
from math import log
from operator import itemgetter


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

    return header, attribute_values, entries


def _is_perfectly_classified(samples):
    value = samples[0]['class_label']
    for s in samples:
        if s['class_label'] != value:
            return False
    return True


def _pos_classification_fraction(samples):
    positive = 0
    for sample in samples:
        if sample['class_label'] == 1:
            positive += 1
    # avoid division by 0
    if len(samples) == 0:
        res = 0
    else:
        res = positive / len(samples)
    return res


def _entropy(samples, sample_subset, pos_fraction):
    # avoid division by 0
    if pos_fraction == 0:
        pos_fraction = 0.0001
    if pos_fraction == 1:
        pos_fraction = 0.999
    return len(sample_subset) / len(samples) * ((pos_fraction * log(1 / pos_fraction, 2)) + (1 - pos_fraction * log(1 / (1 - pos_fraction), 2)))


def _split_samples(samples, attribute, threshold):
    samples_below = [x for x in samples if x[attribute] <= threshold]
    samples_above = [x for x in samples if x[attribute] > threshold]
    return samples_below, samples_above


def _inverted_gain(samples, attribute, threshold):
    samples_below, samples_above = _split_samples(samples, attribute, threshold)
    _pos_below_frac = _pos_classification_fraction(samples_below)
    _pos_above_frac = _pos_classification_fraction(samples_above)

    return _entropy(samples, samples_below, _pos_below_frac) + _entropy(samples, samples_above, _pos_above_frac)


def tidt(samples, attributes, attribute_values):
    if _is_perfectly_classified(samples):
        return {'value': samples[0]['class_label'], 'left': None, 'right': None}
    # TODO: no tests splits the data

    candidates = []
    for attribute in attributes:
        for threshold in attribute_values[attribute]:
            candidates.append((attribute, threshold, _inverted_gain(samples, attribute, threshold)))

    best_attribute, best_threshold, best_gain = min(candidates, key=itemgetter(2))
    samples_below, samples_above = _split_samples(samples, best_attribute, best_threshold)

    return {
        'attribute': best_attribute,
        'threshold': best_threshold,
        'samples': len(samples),
        'left': tidt(samples_below, attributes, attribute_values),
        'right': tidt(samples_above, attributes, attribute_values)
    }
    
#header, attribute_values, entries = read_data("gene_expression_training.csv")

#tree = tidt(entries, header, attribute_values)

#print(tree)
