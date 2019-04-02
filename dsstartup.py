#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 30 11:01:41 2019

@author: bastian
"""

        
import isodata, loaddata


data = loaddata.read_data()

element = input('Enter desired Element (e.g. Ca): ')

element_data = loaddata.load_isodata_per_element(data, element)

el = isodata.Isodata(element_data)


#el.print_iso_info()
    
#create some testing scenarios
el.set_error_model(18, 10, 1e11, 300)
spk1 = el.mix_doublespike([98,100], 0.5)
mix1 = el.mix_sample_doublespike(0.3, -0.5)
meas = el.beam_simulation(-1.8, 50)
el.set_ratio_space([1,2,5,6])
