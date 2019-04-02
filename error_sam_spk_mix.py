#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:01:41 2019

@author: bastian
"""

        
import isodata, loaddata
import numpy as np


data = loaddata.read_data()

element = input('Enter desired Element (e.g. Ca): ')

element_data = loaddata.load_isodata_per_element(data, element)

el = isodata.Isodata(element_data)


#el.print_iso_info()
    
#create some testing scenarios
test_vector = np.linspace(0.01,0.99,100)
al = np.zeros((len(test_vector), 1))


for i in range(len(test_vector)):
    
    el.set_error_model(20, 8, 1e11, 300)
    
    el.mix_doublespike([32,33], test_vector[i])
    
    el.mix_sample_doublespike(0.5, -0.2)
    el.beam_simulation(1.8, 100)
    el.set_ratio_space([32,33,34,36])
    el.inversion_routine()
    al[i] = np.std(el.fractionation[:,0])
    #print(f'alpha = {np.mean(el.fractionation[:,0])}, beta = {np.mean(el.fractionation[:,1])}')

import matplotlib.pyplot as plt

_ = plt.plot(test_vector, al)
plt.show()