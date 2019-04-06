#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:01:41 2019

@author: bastian
"""

        
import isodata, loaddata
import numpy as np
import time
import matplotlib.pyplot as plt
import itertools



data = loaddata.read_data()

element = input('Enter desired Element (e.g. Ca): ')

element_data = loaddata.load_isodata_per_element(data, element)

el = isodata.Isodata(element_data)

ComTime = time.time()
#el.print_iso_info()
    
#create some testing scenarios
spike_combs = list(itertools.combinations(range(el.nspikes), 2))
inv_combs = list(itertools.combinations(range(el.niso), 4))


test_vector = np.linspace(0.01,0.99,100)
al = np.zeros((len(test_vector), len(spike_combs)))
el.set_error_model(20, 8, 1e11, 300)


for combo in spike_combs:

    for i in range(len(test_vector)):
    
        
        el.mix_doublespike(list(combo), 0.5)
        
        el.mix_sample_doublespike(test_vector[i], -0.2)
        el.beam_simulation(-1.8, 100)
        el.set_ratio_space([0,1,2,3])
        el.inversion_routine()
        al[i,combo] = np.std(el.fractionation[:,0])
    _ = plt.plot(test_vector, al)
print(f'run time: {time.time()-ComTime}')




plt.axis([0,1,0,0.02], figsize=[15,10])
plt.xlabel('Proportion Spike1 in Spike1:Spike2 Mix')
plt.ylabel(r'Error in $\alpha$ (1SD)')
plt.legend(spike_combs)
plt.show()