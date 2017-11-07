import csv
from math import log

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
    return positive / len(samples)


def _entropy(samples, pos_fraction):
    return len(samples)/len(samples)*((pos_fraction*log(1/(pos_fraction), 2))+(1-pos_fraction*log(1/(1-pos_fraction), 2)))


def _inverted_gain(samples, attribute, threshold):
    samples_below = [x for x in samples if x[attribute] <= threshold]
    samples_above = [x for x in samples if x[attribute] > threshold]
    _pos_below_frac = _pos_classification_fraction(samples_below)
    _pos_above_frac = _pos_classification_fraction(samples_above)

    return _entropy(samples_below, _pos_below_frac) + _entropy(samples_above, _pos_above_frac)


def tidt(samples, attributes):
    if _is_perfectly_classified(samples):
        return {'value': samples[0]['class_label'], 'left': None, 'right': None}
    # TODO: no tests splits the data
