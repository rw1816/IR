# -*- coding: utf-8 -*-
"""
Created on Tue Oct  6 17:25:37 2020

Apply the temperature calibration to the raw pixel data from the FLIR A35
@author: rw1816
"""
def raw2tempSol(I):
    
    import numpy as np
    
    a =       3.858   #%  (3.857, 3.859)
    c =      -804.6    #%  (-805.1, -804.1)
    T = 1470.0/np.log(55073.0/(I-813.0)+1.0)*a+c
    T = T - 273
    
    return T

# Coefficients with 95% confidence bounds, as determined for the in-situ thermography... 
# back in 2018 for SS316L
    
def raw2tempPow(I):
    
    import numpy as np
    
    a =       1.782     #%(2.89, 2.894)
    c =        -208.5;    #%(-501.6, -500.4)
    T = 1470.0/np.log(55073.0/(I-813.0)+1.0)*a+c #in Kelvin
    T = T - 273  #in degC
    
    return T

# Coefficients with 95% confidence bounds, as determined for the in-situ thermography... 
# back in 2018 for SS316L