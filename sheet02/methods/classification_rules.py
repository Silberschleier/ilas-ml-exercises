# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 20:21:08 2017

@author: Maren
"""
import json
from tdidt import read_data
from classification import accuracy

def _is_leaf(tree):
    return (tree['left'] == None and tree['right'] == None)
    

# Regeln in eine lesbare Form bringen   
def _rules_to_string(ruleset):
    rule_string = ""
    for rule in ruleset['rules']:
        rule_string += str(rule)
    rule_string += " -> " + str(ruleset['value'])
    return rule_string
  
    
def classify_one_sample_and_extract_rule(tree, sample, sample_index, attributes, attribute_values):
    if _is_leaf(tree):
        return {'value': tree['value'], 'rules': set()}
    else:
        if attribute_values[tree['attribute']][sample_index] <= tree['threshold']:
            ruleset = classify_one_sample_and_extract_rule(tree['left'], sample, sample_index, attributes, attribute_values)
            ruleset['rules'].add((tree['attribute'], "<=", tree['threshold']))
            return ruleset
        else:
            ruleset = classify_one_sample_and_extract_rule(tree['right'], sample, sample_index, attributes, attribute_values)
            ruleset['rules'].add((tree['attribute'], ">=", tree['threshold']))
            return ruleset
            

def classify_and_extract_rules(tree, samples, attributes, attribute_values):
    rules = []
    for i in range(len(samples)):
        rule = classify_one_sample_and_extract_rule(tree, samples[i], i, attributes, attribute_values)
        if rule not in rules:
            rules.append(rule)
    return rules


def classify_one_sample(rules, sample, sample_index, attributes, attribute_values):
    for r in rules:
        for rule in r['rules']:
            rule_applies = True
            if rule[1] == '<=':
                if attribute_values[rule[0]][sample_index] > rule[2]:
                    rule_applies = False
                    break
            else:
                if attribute_values[rule[0]][sample_index] < rule[2]:
                    rule_applies = False
                    break
        if rule_applies:
            return r['value']


def classify_with_rules(rules, samples, attributes, attribute_values):
    res = []
    for i in range(len(samples)):
        res.append(classify_one_sample(rules, samples[i], i, attributes, attribute_values))
    return res


def prune_rules(rules):
    for r in rules:
        for l in r['rules']:
            rule_without_l = r - set(l)
            if err_pessimistic(rule_without_l) < err_pessimistic(r):
                r.remove(l)
                

def observed_error():
    pass


def err_pessimistic(rule):
    pass


with open('trees/ausgabe_depth_3.json') as fp:
    tree = json.load(fp)
header_train, attribute_values_train, entries_train = read_data("../data/gene_expression_training.csv")

rules = classify_and_extract_rules(tree, entries_train, header_train, attribute_values_train)
for i in range(len(rules)):
    print("Rule " + str(i+1) + ": " + _rules_to_string(rules[i]))

header_test, attribute_values_test, entries_test = read_data("../data/gene_expression_test.csv")
res_test = classify_with_rules(rules, entries_test, header_test, attribute_values_test)
res_train = classify_with_rules(rules, entries_train, header_train, attribute_values_train)

class_labels_test = []
for entry in entries_test:
    class_labels_test.append(entry['class_label'])

class_labels_train = []
for entry in entries_train:
    class_labels_train.append(entry['class_label'])

print("Accuracy Train: " + str(accuracy(res_train, class_labels_train)))
print("Accuracy Test: " + str(accuracy(res_test, class_labels_test)))