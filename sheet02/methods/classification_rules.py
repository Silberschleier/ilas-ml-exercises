# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 20:21:08 2017

@author: Maren
"""
import json
from tdidt import read_data

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
            ruleset['rules'].add((tree['attribute'], " < ", tree['threshold']))
            return ruleset
        else:
            ruleset = classify_one_sample_and_extract_rule(tree['right'], sample, sample_index, attributes, attribute_values)
            ruleset['rules'].add((tree['attribute'], " > ", tree['threshold']))
            return ruleset
            

def classify_and_extract_rules(tree, samples, attributes, attribute_values):
    rules = []
    for i in range(len(samples)):
        rule = classify_one_sample_and_extract_rule(tree, samples[i], i, attributes, attribute_values)
        if rule not in rules:
            rules.append(rule)
    return rules


def prune_rules(rules):
    for r in rules:
        for l in r['rules']:
            rule_without_l = r - set(l)
            if err_pessimistic(rule_without_l) < err_pessimistic(r):
                r.remove(l)
                

def err_pessimistic(rule):
    


with open('trees/ausgabe_depth_10.json') as fp:
    tree = json.load(fp)
header_train, attribute_values_train, entries_train = read_data("../data/gene_expression_training.csv")

rules = classify_and_extract_rules(tree, entries_train, header_train, attribute_values_train)
for i in range(len(rules)):
    print("Rule " + str(i+1) + ": " + _rules_to_string(rules[i]))