# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 20:21:08 2017

@author: Maren
"""

from tdidt import read_data, tdidt

def _is_leaf(tree):
    return (tree['left'] == None and tree['right'] == None)
    

# Regeln in eine lesbare Form bringen   
def _convert_rule(rule):
    rule = rule.replace(" |  | ", " and ")
    rule = rule.replace(" | ", "")
    return rule
  
    
def classify_one_sample_and_extract_rule(tree, sample, sample_index, attributes, attribute_values):
    if _is_leaf(tree):
        return " -> " + str(tree['value'])
    else:
        if attribute_values[tree['attribute']][sample_index] <= tree['threshold']:
            return " | " + str(tree['attribute']) + " < " + str(tree['threshold']) + " | " + str(classify_one_sample_and_extract_rule(tree['left'], sample, sample_index, attributes, attribute_values))
        else:
            return " | " + str(tree['attribute']) + " > " + str(tree['threshold']) + " | " + str(classify_one_sample_and_extract_rule(tree['right'], sample, sample_index, attributes, attribute_values))


def classify_and_extract_rules(tree, samples, attributes, attribute_values):
    rules = []
    for i in range(len(samples)):
        rule = classify_one_sample_and_extract_rule(tree, samples[i], i, attributes, attribute_values)
        if rule not in rules:
            rules.append(rule)
    return rules


header_train, attribute_values_train, entries_train = read_data("../data/gene_expression_training.csv")
tree = tdidt(entries_train, header_train, attribute_values_train, 3)

rules = classify_and_extract_rules(tree, entries_train, header_train, attribute_values_train)
for i in range(len(rules)):
    print("Rule " + str(i+1) + ": " + _convert_rule(rules[i]))