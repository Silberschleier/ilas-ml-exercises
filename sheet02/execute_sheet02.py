from methods import *
import json

if __name__ == '__main__':
    depth = 10
    header_train, attribute_values_train, entries_train = read_data("data/gene_expression_training.csv")
    #tree = tdidt(entries_train, header_train, attribute_values_train, depth)

    with open('methods/trees/ausgabe_depth_10.json') as fp:
        tree = json.load(fp)

    generate_dot_from_graph(tree, 'output_depth-{}.dot'.format(depth))
    # pprint(tree)

    header_test, attribute_values_test, entries_test = read_data("data/gene_expression_test.csv")
    res_test = classify(tree, entries_test, header_test, attribute_values_test)
    res_train = classify(tree, entries_train, header_train, attribute_values_train)

    class_labels_test = []
    for entry in entries_test:
        class_labels_test.append(entry['class_label'])

    class_labels_train = []
    for entry in entries_train:
        class_labels_train.append(entry['class_label'])

    print("Depth: {}".format(depth))
    print("Accuracy Train: " + str(accuracy(res_train, class_labels_train)))
    print("Accuracy Test: " + str(accuracy(res_test, class_labels_test)))

    class_labels_test = []
    for entry in entries_test:
        class_labels_test.append(entry['class_label'])

    reduced_error_pruning(tree, tree, entries_test, header_test, attribute_values_test, class_labels_test)
    generate_dot_from_graph(tree, 'pruned_output_depth-{}.dot'.format(depth))

    res_test = classify(tree, entries_test, header_test, attribute_values_test)
    res_train = classify(tree, entries_train, header_train, attribute_values_train)

    class_labels_train = []
    for entry in entries_train:
        class_labels_train.append(entry['class_label'])

    print("Accuracies after reduced error pruning:")
    print("Accuracy Train: " + str(accuracy(res_train, class_labels_train)))
    print("Accuracy Test: " + str(accuracy(res_test, class_labels_test)))
    #print(tree)
