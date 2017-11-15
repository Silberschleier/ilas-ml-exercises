# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 21:45:31 2017

@author: Maren
"""
import json
from tdidt import read_data, tdidt

header_train, attribute_values_train, entries_train = read_data("../data/gene_expression_training.csv")

tree3 = tdidt(entries_train, header_train, attribute_values_train, 3)

tree5 = tdidt(entries_train, header_train, attribute_values_train, 5)

tree10 = tdidt(entries_train, header_train, attribute_values_train, 10)    


with open('trees/ausgabe_depth_3.json', 'w') as fp:
  json.dump(tree3, fp)
  
with open('trees/ausgabe_depth_5.json', 'w') as fp:
  json.dump(tree5, fp)
  
with open('trees/ausgabe_depth_10.json', 'w') as fp:
  json.dump(tree10, fp)