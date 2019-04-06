#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 21:36:15 2019

@author: bastian
"""

import geometricfunctions as gmf
import numpy as np

def inversion(el, R_meas):
        
        beta = -1.5      # instrumental fractionation in #
        alpha = 0.2   # natural fractionation 
        
    # start routine here: assign starting variables and isotope ratios
    
        for n in range (4): #for more iterations increase range
            Rx1 = el.R_std[0]
            Ry1 = el.R_std[1]
            Rz1 = el.R_std[2]
    
            Rx2 = el.R_std[0] * (el.R_mass[0]) ** alpha
            Ry2 = el.R_std[1] * (el.R_mass[1]) ** alpha
            Rz2 = el.R_std[2] * (el.R_mass[2]) ** alpha
        
            # create line (a) - call geometric line function  
            Pd,Pe,Pf,Pg = gmf.line(Rx1,Rx2,Ry1,Ry2,Rz1,Rz2)
      
        #store vaiables of line (a) for later intercept calc.
            P1d = Pd
            P1e = Pe
            P1f = Pf
            P1g = Pg
    
            Rx3 = el.R_spk[0]
            Ry3 = el.R_spk[1]
            Rz3 = el.R_spk[2]
        
        
        # construct plane (A) - call geometric plane function
            Pa,Pb,Pc = gmf.plane(Rx1,Rx2,Rx3,Ry1,Ry2,Ry3,Rz1,Rz2,Rz3)
        
          
            for m in range (6): #(nested into n, for more iterations increase 1:m, where m = 2,3,4, ... x.)
    
                Rx1 = R_meas[0] #measured ratios
                Ry1 = R_meas[1]
                Rz1 = R_meas[2]
    
                Rx2 = R_meas[0] * (el.R_mass[0]) ** beta
                Ry2 = R_meas[1] * (el.R_mass[1]) ** beta
                Rz2 = R_meas[2] * (el.R_mass[2]) ** beta
                
                # create line (b) - call gemometric line function
                Pd,Pe,Pf,Pg = gmf.line(Rx1,Rx2,Ry1,Ry2,Rz1,Rz2)
                
                #Intercept Plane (A) and line (b) call geometric intercept function
                InX,InY,InZ = gmf.intercept(Pa,Pb,Pc,Pd,Pe,Pf,Pg)
                
                
                #calculate instrumental mass-bias
                RMTRU = InX    #estimate of real mixture ratios
               
                beta = np.log(RMTRU/R_meas[0]) / np.log(el.R_mass[0]) #refine instrumental mass-bias from measured and real mixture ratios
    
       
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
            #RSTRU = InX #estimate of real sample ratio offset by natural fractionation alpha
            #alpha = np.log(RSTRU/el.R_std[0]) / np.log(el.R_mass[0]) # refine estimate of natrual fractionation
            alpha_array = np.array([InX,InY,InZ])
            
            alpha = np.mean(np.log(alpha_array/el.R_std) / np.log(el.R_mass))
            
            
        alpha = -alpha
        beta = beta
        R1 = el.R_std
        R2 = el.R_std*el.R_mass**alpha
        R3 = el.R_spk
        R4 = R_meas
        R5 = R_meas*el.R_mass**beta
        
        n1 = np.cross((R1-R2), (R1-R3))
        n2 = np.cross((R4-R5),(R4-R3))
        vdot = np.dot(n1,n2)
        cosangle = vdot/(np.linalg.norm(n1)*np.linalg.norm(n2))
        angle = (360-180-(np.rad2deg(np.arccos(cosangle))))
        #print(cosangle)
        
        return [alpha, beta, angle]