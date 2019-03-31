#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 20:54:43 2019

@author: bastian
"""

import sys
import csv
import pandas as pd

#def load_element_data():


file = 'maininput.csv'

# def load(file):
#     """Open .csv file containing elemental data and spike compositions"""

#     try:
#         with open(file) as csv_file:
#             csv_reader = csv.reader(csv_file, delimiter=',')
# #             loaded_txt = in_file.read().strip().split('\n')
# #             loaded_txt = [x.lower() for x in loaded_txt]
#             return csv_reader
        
#     except IOError as error:
#         print(f'{error} Error opening {file}. Terminate Program', file=sys.stderr)

#         sys.exit(1)
        
# data = load(file)
#with open(file) as csv_file:
labels = []
#    element_data = pd.read_csv(csv_file, header=0, index_col=[1], delimiter=',')
#
#for line in element_data:
#    if element_data['element'].any():
#        label = element_data['element']
#        print(label)
#        #labels.append(label)
#    else:
#        labels.append(label)
        
with open(file) as csv_file:
    lines = csv_file.readlines()[1:]
    for line in lines:
        if line.split(',')[0]:
            label = line.split(',')[0] 
            labels.append(label)
        else:
            labels.append(label)
        
    
with open(file) as csv_file:
    element_data = pd.read_csv(csv_file, header=0, delimiter=',')
    

#replace NAN element cells with respective element symbol:
element_data.insert(0, 'el', labels)
element_data.drop(element_data.columns[1], axis=1, inplace=True)

