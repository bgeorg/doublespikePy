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
test_vector = np.linspace(0.1,0.9,20)
al = np.zeros((len(test_vector), len(test_vector)))

for j in range(len(test_vector)):
    
    el.mix_doublespike([33,34], test_vector[j])

    for i in range(len(test_vector)):
        
        el.set_error_model(20, 8, 1e11, 300)
        
        #el.mix_doublespike([57,58], 0.5)
        
        el.mix_sample_doublespike(test_vector[i], -0.2)
        el.beam_simulation(1.8, 100)
        el.set_ratio_space([32,33,34,36])
        el.inversion_routine()
        al[j,i] = np.std(el.fractionation[:,0])
        #print(f'alpha = {np.mean(el.fractionation[:,0])}, beta = {np.mean(el.fractionation[:,1])}')

import matplotlib.pyplot as plt
#
#_ = plt.plot(test_vector, al)
#plt.show()

Y = test_vector[::-1]    #create scale for Y-axis 
X = test_vector[::-1]                      #create scale for X-axis
Z = al                      #Z-axis in contur is z-score 


#print Z-score matrix to screen - and/or write to csv file ... 

fig1 = plt.contourf(X, Y, Z, 25, cmap='RdGy') 
#plt.colorbar()
plt.xlabel('Peak Pressure P$_{0}$')
plt.ylabel('initial FeO$_{BSE}$')
#manual_loc = [(0,1),(1,2)]
#plt.clabel(fig1, inline=1, fontsize=10)
plt.show()