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


def accuracy(result, class_labels):
    true_classified = 0
    for i in range(len(result)):
        if result[i] == class_labels[i]:
            true_classified += 1
    return true_classified / len(result)
