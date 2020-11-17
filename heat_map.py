# -*- coding: utf-8 -*-
"""
Created on Fri Oct  2 16:32:43 2020

First attempt to plot at heat map from the FLIR A35 data
@author: rw1816
"""

import numpy as np
from temp_calibration import raw2tempSol, raw2tempPow
import scipy.signal as signal
import utils
import imageio
from tkinter import *
from tkinter.filedialog import askopenfilename, askdirectory
from os import path

root=Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
root.update()
root.filename = askopenfilename(title='Select numpy file') # show an "Open" dialog box and return the path to the selected file
root.destroy()

arr_obj = np.load(root.filename, mmap_mode='r')
I = arr_obj[:, :, :]

#recording is at 30fps
rec_length = int(np.size(I, 2)/30)      #note try and back this out of the seq
time = np.arange(0, rec_length, 1/30.0)
        
layerframe, wiper_index = utils.frames_to_layers(I)
num_layers=int(max(layerframe))
num_peaks = np.zeros((np.size(I,0) , np.size(I,1)))
D = np.zeros((np.size(I, 0), np.size(I, 1), num_layers), dtype='uint16') #delcare a blank array of the voxel space, 1 per layer

#loop through each pixel position
        
for i in range(0, (np.size(D, 0))):
    for j in range(0, np.size(D, 1)):
        
        laser_peaks, properties = signal.find_peaks(I[i, j, :], distance=(200), prominence=(1200))
        dwell_ind = laser_peaks-30
        layers_ind = layerframe[dwell_ind]
        num_peaks[i,j] = len(laser_peaks)
        for k in range(0, len(dwell_ind)):
            
            peak_layer=int(layerframe[dwell_ind[k]])
            D[i, j, peak_layer-1] = np.mean((I[i, j, dwell_ind[k]-1], I[i, j, dwell_ind[k]], I[i, j, dwell_ind[k]+1]))

#D=utils.clean_spatter(D)

T=np.zeros((np.size(I, 0), np.size(I, 1), num_layers), dtype='uint16')
T=raw2tempPow(D)
T=T.astype('uint16')

root2=Tk()
root2.withdraw() # we don't want a full GUI, so keep the root window from appearing
root2.update()
outfolder = askdirectory(title='Select save location') # show an "Open" dialog box and return the path to the selected file
root2.destroy()


imageio.volwrite(path.join(outfolder, path.split(root.filename)[1][0:-4] + '_dwell_voxels.tiff'), np.transpose(T), format='TIFF') #write out the TIFF stack
#imageio wants [z,x,y] so we transpose
#now its time to open the tiff stack in paraview 

