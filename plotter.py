# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 11:49:49 2020
Plot some curves out of the IR data, working from the TIFF of dwell voxels
@author: rw1816
"""
import imageio
import matplotlib.pyplot as plt
import cv2
import numpy as np
from skimage import measure, morphology
import pandas as pd
import utils

plt.rcParams['font.family'] = 'serif'
#plt.rcParams['font.serif'] = 'Arial'
plt.rcParams['font.size'] = '14.0'
plt.rcParams['text.usetex'] = True

filename = "F://OneDrive - Imperial College London//Post-doc//build_data//b1_220920//Accel_316_build1_joined_2020-09-22_dwell_voxels.tiff"
T = imageio.volread(filename)
T=T.transpose()

#%% plot the mean layer temperature w.r.t. build height, layer number

mean_temp=np.zeros(np.size(T, 2))
build_height=np.arange(0, np.size(T, 2)*0.05, 0.05)
for i in range(0, len(mean_temp)):
    layer = T[:,:,i]
    mean_temp[i]=np.mean(layer[layer!=0])
 
fig=plt.figure(figsize=(4, 4), facecolor='w')
ax=plt.axes() 
plt.plot(build_height, mean_temp)

ax.set(xlabel = 'Build height (mm)', ylabel = r'Mean layer temperature before melt (\textdegree C)')
plt.savefig('F://OneDrive - Imperial College London//Post-doc//build_data//b1_220920//plots\dwell_temp.svg', facecolor='w', bbox_inches='tight')

#%% 
#mask = np.zeros((np.size(T, 0), np.size(T, 1), np.size(T, 2)), dtype='bool')
labels, num = morphology.label(T, return_num=True)
cleaned_label_img = morphology.remove_small_objects(labels, 5) #do some cleaning on the random spots





