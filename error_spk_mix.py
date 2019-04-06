#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:01:41 2019

@author: bastian
"""

        
import isodata, loaddata
import numpy as np
import time


data = loaddata.read_data()

element = input('Enter desired Element (e.g. Ca): ')

element_data = loaddata.load_isodata_per_element(data, element)

el = isodata.Isodata(element_data)

ComTime = time.time()
#el.print_iso_info()
    
#create some testing scenarios
test_vector = np.linspace(0.01,0.99,1000)
al = np.zeros((len(test_vector), 3))
el.set_error_model(20, 8, 1e11, 300)


for i in range(len(test_vector)):
    
    
    
    el.mix_doublespike([2,3], test_vector[i])
    
    el.mix_sample_doublespike(0.5, -0.2)
    el.beam_simulation(1.8, 100)
    el.set_ratio_space([0,1,2,3])
    el.inversion_routine()
    al[i,:] = np.std(el.fractionation[:,0]), np.std(el.fractionation[:,1]), np.mean(el.fractionation[:,2])

print(f'run time: {time.time()-ComTime}')

import matplotlib.pyplot as plt

_ = plt.scatter(test_vector, al[:,0])
plt.axis([0,1,0,.02])
plt.xlabel('Proportion Spike-1 in Spike1:Spike2 Mix')
plt.ylabel(r'Error in $\alpha$ (1SD)')
plt.show()