#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 21:36:15 2019

@author: bastian
"""

import geometricfunctions as gmf
import numpy as np


def inversion(R_meas, R_std, R_spk, R_mass):
        
        beta = 3      # instrumental fractionation in #
        alpha = 2   # natural fractionation 
        
    # start routine here: assign starting variables and isotope ratios
    
        for n in range (6): #for more iterations increase range
            Rx1 = R_std[0]
            Ry1 = R_std[1]
            Rz1 = R_std[2]
    
            Rx2 = R_std[0] * (R_mass[0]) ** alpha
            Ry2 = R_std[1] * (R_mass[1]) ** alpha
            Rz2 = R_std[2] * (R_mass[2]) ** alpha
        
            # create line (a) - call geometric line function  
            Pd,Pe,Pf,Pg = gmf.line(Rx1,Rx2,Ry1,Ry2,Rz1,Rz2)
      
        #store vaiables of line (a) for later intercept calc.
            P1d = Pd
            P1e = Pe
            P1f = Pf
            P1g = Pg
    
            Rx3 = R_spk[0]
            Ry3 = R_spk[1]
            Rz3 = R_spk[2]
        
        
        # construct plane (A) - call geometric plane function
            Pa,Pb,Pc = gmf.plane(Rx1,Rx2,Rx3,Ry1,Ry2,Ry3,Rz1,Rz2,Rz3)
        
          
            for m in range (6): #(nested into n, for more iterations increase 1:m, where m = 2,3,4, ... x.)
    
                Rx1 = R_meas[0] #measured ratios
                Ry1 = R_meas[1]
                Rz1 = R_meas[2]
    
                Rx2 = R_meas[0] * (R_mass[0]) ** beta
                Ry2 = R_meas[1] * (R_mass[1]) ** beta
                Rz2 = R_meas[2] * (R_mass[2]) ** beta
                
                # create line (b) - call gemometric line function
                Pd,Pe,Pf,Pg = gmf.line(Rx1,Rx2,Ry1,Ry2,Rz1,Rz2)
                
                #Intercept Plane (A) and line (b) call geometric intercept function
                InX,InY,InZ = gmf.intercept(Pa,Pb,Pc,Pd,Pe,Pf,Pg)
    
                #calculate instrumental mass-bias
                RMTRU = InX    #estimate of real mixture ratios
               
                beta = np.log(RMTRU/R_meas[0]) / np.log(R_mass[0]) #refine instrumental mass-bias from measured and real mixture ratios
    
       
       #create plane (B) - call makeplane.m
            Pa,Pb,Pc = gmf.plane(Rx1,Rx2,Rx3,Ry1,Ry2,Ry3,Rz1,Rz2,Rz3)
        
       #recall variables of line (a) 
            Pd = P1d
            Pe = P1e
            Pf = P1f
            Pg = P1g
        
       #Intercept line (a) with plane (B) call makeintercept.m
            InX,InY,InZ = gmf.intercept(Pa,Pb,Pc,Pd,Pe,Pf,Pg)
        
       #calculate new alpha
            RSTRU = InX #estimate of real sample ratio offset by natural fractionation alpha
            alpha = np.log(RSTRU/R_std[0]) / np.log(R_mass[0]) # refine estimate of natrual fractionation

        alpha = -alpha
        beta = -beta
       
        
        return [alpha, beta]