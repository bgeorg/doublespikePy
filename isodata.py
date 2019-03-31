#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 28 21:15:43 2019
Class isodata contains all important elemental data, as well as some important methods.
@author: bastian
"""

import numpy as np

class Isodata:
    
    """Class Isodata.
    Instances of this class represent elemental data (isotopes, masses, natural abundances, spikes ...), and
    provides a few important methods, such as setting up error-models, generating simulated mass-spec data etc.
    """
    
    def __init__(self, element_data): #element, isotope, mass, standard, spikes):
        """Initialise the instance of class Isodata. Arguments are given as tuple element_data:"""
    
        element, isotope, mass, standard, spikes = element_data #unpacking data tuple
        
        self.element = element
        self.isotope = isotope
        self.mass = mass
        self.standard = standard/sum(standard)
        self.spikes = [array/sum(array) for array in spikes]
        self.niso = len(isotope)
        self.nratio = self.niso - 1
        self.nspikes = len(spikes)
        self.isoname = [str(x) + element for x in isotope]
        
        
        
        
    def set_error_model(self, faraday_range, integration_time, amp_resistors, temperature):
        """this method sets up the error model coefficients a, b, c - 
        as well as the virtual mass-spec parameters:"""
        
        
        e=1.60217646e-19               # elementary charge Coulombs
        k=1.3806504e-23               # Boltzman constant (m**2 kg s**-2 K**-1)
        
        vmax = faraday_range              #Voltage range of Faraday array
        dt = integration_time             #integration time (seconds) per cycle
        ohm = amp_resistors               #resistor rating of amplifier board
        temp = temperature                #Temperature setting in K
        
        a = 4 * k * temp * ohm / dt               # Johnson-Nyquist noise in volts
        b = e * ohm / dt                      # Counting statistics prefactor
        
    
    
    	#by default assume Johnson noise and counting statistics
        self.errormodel_measured_intensity = vmax
        self.errormodel_measured_a = a * np.ones([self.niso])
        self.errormodel_measured_b = b * np.ones([self.niso])
        self.errormodel_measured_c = 0 * np.ones([self.niso])
        
        self.errormodel_spike_intensity = vmax
        self.errormodel_spike_a = 0 * np.ones([self.niso])
        self.errormodel_spike_b = 0 * np.ones([self.niso])
        self.errormodel_spike_c = 0 * np.ones([self.niso])
        
        self.errormodel_standard_intensity = vmax
        self.errormodel_standard_a = 0 * np.ones([self.niso])
        self.errormodel_standard_b = 0 * np.ones([self.niso])
        self.errormodel_standard_c = 0 * np.ones([self.niso])
        
        
    def print_iso_info(self):
        """print some parameters to the screen - if requried"""
        
        np.set_printoptions(precision=4, suppress=True)  #limit array print to 4 digits
        print(f'\nElement: {self.element}')
        print(f'Isotopes: {self.isotope}')
        print(f'Atomic Masses: {self.mass}')
        print(f'Natural Abundances: {self.standard}')
        
        #create spike labels dynamically for nicer print:
        spk_len = len(self.spikes)+1
        spk_names = ['spike'+str(i) for i in range(1,spk_len)]
        for i in range(len(self.spikes)):
            print(f'{spk_names[i]}: {self.spikes[i]}')
        
        
        print(f'Number of Isotopes: {self.niso}')
        print(f'Number of Ratios: {self.nratio}')
        print(f'Number of Spikes: {self.nspikes}')
        print(f'Isotope Names: {self.isoname}')
        
        ind_info = [str(ix)+'->'+(label) for ix,label in enumerate(self.isoname)]
        print(f'Isotope indexing: {ind_info}')
        
        
    def get_isotope_index(self, isotope):
        """Function receives list of isotopes, e.g. [204, 206, 208] and returns the index of
        these isotopes as in el.isotopes"""
        
        ix = [i for i,val in enumerate(self.isotope) if val in isotope]
        
        return ix
    
    
        
    def mix_doublespike(self, single_spikes, spike_mixing_proportions):
        """This function receives inputs and performs spike mixing calculations:
            
            Arguments:
            -- self
            -- single_spikes: list of the two single isotope spikes, e.g. [0, 3] or [204, 208]
                will use the 0th and 3rd spike
            -- spike_mixing_proportions: float between 0 ... 1, e.g. 0.45
                will give 0.45xspike1 + (1-0.45)*spike2
        """
        
        #check for single_spikes input format and get index when isotope masses are used:
        spike_index = [(max(single_spikes)<12) * single_spikes.copy() or self.get_isotope_index(single_spikes)][0]
                
        spkA = self.spikes[spike_index[0]]
        spkB = self.spikes[spike_index[-1]]
        
        self.dspk_mix = (spike_mixing_proportions * spkA) + ((1-spike_mixing_proportions) * spkB)

        return self.dspk_mix
    
    
    def mix_sample_doublespike(self, sample_spike_proportion, *alpha):
        """This function performes sample-doublespike mixing.
        
        Arguments:
        -- self
        -- sample_spike_proportion: mixing coefficient sample:spike, e.g.
           0.35xsample + (1-0.35)*dpsk
        -- alpha: natural fractionation can be added to the sample before mixing with spike.
        Set alpha to numerical value, e.g. 0.02 to apply fractionation.
        Set to 0 if no fractionation required
        """
        
        samp = sample_spike_proportion
    
        if alpha:
            sam_frac = self.standard * np.exp(-np.log(self.mass)*alpha[0])
            sam_frac = sam_frac/sum(sam_frac)       #renormalize after applying fractionation
            self.sam_spk_mix = (samp * sam_frac) + (1-samp) * self.dspk_mix
        else:
            self.sam_spk_mix = (samp * self.standard) + (1-samp) * self.dspk_mix
            
        return self.sam_spk_mix



    def beam_simulation(self, beta, cycles):
        """This function takes some input arguments and simulates a mass-spec analysis using
        montecarlo runs. 
        
        Arguments:
            sample_spike_mix: self.sam_spk_mix - pre-set
            double_spike: self.dspk.mix - pre-set
            
            beta: assumed instrumental fractionation (mass-bias)
            cycles: number of data points simulated


            sample(i,:)=standard.*exp(-log(mass).*alpha(i));
            ple(i,:)=sample(i,:)./sum(sample(i,:));
        """
        
        measured_signal = np.zeros((cycles, self.niso))
        measured_intensity = np.zeros((cycles, self.niso))
        measured_variance = np.zeros((cycles, self.niso))
        measured = np.zeros((cycles,self.niso))
        np.random.seed(40)
        
        for i in range(cycles):
            
            measured_signal[i,:] = self.sam_spk_mix * np.exp(-np.log(self.mass)*beta)
            measured_signal[i,:] = measured_signal[i,:]/sum(measured_signal[i,:])
            
            measured_intensity[i,:]= measured_signal[i,:] * self.errormodel_measured_intensity #scale up to vmax
            measured_variance[i,:] = self.errormodel_measured_a + self.errormodel_measured_b * measured_intensity[i,:] + self.errormodel_measured_c * (measured_intensity[i,:]**2)
            
            #run a random-multivariate_normal model on the intensity scaled beams:
            mu = np.transpose(measured_intensity[i,:])
            cov = np.diag(measured_variance[i,:])
            measured[i,:] = np.random.multivariate_normal(mu, cov, size=1)
            
            
        self.measured = measured
        
        return measured
        


