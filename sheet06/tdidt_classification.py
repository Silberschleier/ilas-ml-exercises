from math import log
from operator import itemgetter

# code copied from sheet02, only slightly modified

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

def _is_leaf(tree):
    return tree['left'] is None and tree['right'] is None


def classify_one_sample(tree, sample, sample_index, attributes, attribute_values):
    if _is_leaf(tree):
        return tree['value']
    else:
        if attribute_values[tree['attribute']][sample_index] <= tree['threshold']:
            return classify_one_sample(tree['left'], sample, sample_index, attributes, attribute_values)
        else:
            return classify_one_sample(tree['right'], sample, sample_index, attributes, attribute_values)


def classify_tdidt(tree, samples, attributes, attribute_values, class_labels):
    res = []
    for i in range(len(samples)):
        res.append(classify_one_sample(tree, samples[i], i, attributes, attribute_values))
    true_classified = 0
    for i in range(len(res)):
        if res[i] == class_labels[i]:
            true_classified += 1
    return true_classified / len(res)

def get_attributes(tree, attr_list):
    if _is_leaf(tree) == False:
        attr_list.append(tree['attribute']-1)
        get_attributes(tree['left'], attr_list)
        get_attributes(tree['right'], attr_list)