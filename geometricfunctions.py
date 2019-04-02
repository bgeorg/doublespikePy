#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  1 21:08:47 2019

@author: bastian
"""

## ---- makeplane function --- 
def plane(Rx1,Rx2,Rx3,Ry1,Ry2,Ry3,Rz1,Rz2,Rz3):
## function to calculate plane coordinates

  PaUp = Ry1 * (Rz3 - Rz2) + Ry2 * (Rz1 - Rz3) + Ry3 * (Rz2 - Rz1)
  PaDn = Ry1 * (Rx3 - Rx2) + Ry2 * (Rx1 - Rx3) + Ry3 * (Rx2 - Rx1)
  Pa = PaUp / PaDn
  
  PbUp = Rx1 * (Rz2 - Rz3) + Rx2 * (Rz3 - Rz1) + Rx3 * (Rz1 - Rz2)
  PbDn = Rx1 * (Ry2 - Ry3) + Rx2 * (Ry3 - Ry1) + Rx3 * (Ry1 - Ry2)
  Pb = PbUp / PbDn
  
  Pc = Rz1 - Pa * Rx1 - Pb * Ry1
  
  return [Pa,Pb,Pc]


## ---- makeintercept function
def intercept(Pa,Pb,Pc,Pd,Pe,Pf,Pg):
## function to calculate intercept coordinate
#MAKEINTERCEPT 
 
    InX = (Pb * Pg - Pb * Pe + Pe * Pf - Pc * Pf) / (Pa * Pf + Pb * Pd - Pd * Pf)
    InY = (Pa * Pe - Pa * Pg + Pd * Pg - Pc * Pd) / (Pa * Pf + Pb * Pd - Pd * Pf)
    InZ = Pa * InX + Pb * InY + Pc

    return [InX,InY,InZ]



## ---- makeline function
def line(Rx1,Rx2,Ry1,Ry2,Rz1,Rz2):
## function to calculate line coordiantes  


    Pd = (Rz1 - Rz2) / (Rx1 - Rx2);
    Pe = Rz1 - Rx1 * Pd;
    Pf = (Rz1 - Rz2) / (Ry1 - Ry2);
    Pg = Rz1 - Ry1 * Pf;
    
    return [Pd,Pe,Pf,Pg]