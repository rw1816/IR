# -*- coding: utf-8 -*-
"""
Created on Wed Oct 21 16:25:06 2020

@author: rw1816
"""
import imageio
import numpy as np

T_top = imageio.volread("F:\\OneDrive - Imperial College London\\Post-doc\\build_data\\b1_220920\\Accel_316_build1part22020-09-22_dwell_voxels.tiff")
T_bottom = imageio.volread("F:\\OneDrive - Imperial College London\\Post-doc\\build_data\\b1_220920\\Accel_316_build12020-09-22_dwell_voxels.tiff")

T_top_padded = np.zeros((np.size(T_top, 0), np.size(T_bottom, 1), np.size(T_bottom, 2)), dtype='uint16')

T_top_padded[:, 2:61, 16:87] = T_top
zeros=np.zeros((400, np.size(T_bottom, 1), np.size(T_bottom, 2)))

total= np.vstack((T_bottom, zeros, T_top_padded))
total=total.astype('uint16')
imageio.volwrite("F:\\OneDrive - Imperial College London\\Post-doc\\build_data\\b1_220920\\Accel_316_build1_joined_2020-09-22_dwell_voxels.tiff", total, format='TIFF')
