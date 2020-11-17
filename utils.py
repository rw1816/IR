# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 18:04:22 2020

@author: rw1816
"""
import numpy as np
import cv2

def frames_to_layers(I):

    nframes = np.size(I, 2)
    layerframe=np.ones(nframes, dtype='uint16')
    line_x=int(np.size(I,1)/2)
    iswiper=np.zeros(nframes)
    
    for i in range(0, nframes):
        if np.std(I[:, line_x-5:line_x+5, i]) < 10:
            iswiper[i]=1
    # we are looking for the second wiper here, towards the front where it brings the powder.
    # this motion is slower and we can see the wiper more easily
    # N.B. this process is going to be dependent upon recording frame rate so may need to be changed.
                
    for i in range(1, len(iswiper)):
        
        if iswiper[i:i+4].all() == 1:
            iswiper[i] = 1
            
        else:
            iswiper[i] = 0
            
    for i in range(1, len(iswiper)):
        
        if iswiper[i]==1 and iswiper[i+1:i+3].any() == 1:
            iswiper[i] = 0
            
        else:
            iswiper[i] = iswiper[i]
            
    wiper_index=np.where(iswiper==1)
            
    for i in range(1, nframes):
        if iswiper[i]==1:
            layerframe[i]=layerframe[i-1]+1
            
        else:
            layerframe[i]=layerframe[i-1]
            
    return layerframe, wiper_index

"""
clean_spatter reads in the dwell temperature voxel array, thresholds to create a binary mask
and then removes small outlying objects. This should smoothen up the apparent surface
of the voxel representation.
"""

def clean_spatter(D):
    
    mask = np.zeros((np.size(D, 0), np.size(D, 1), np.size(D, 2)), dtype='uint8')
    opening = np.zeros((np.size(D, 0), np.size(D, 1), np.size(D, 2)), dtype='uint8')
    kernel = np.ones((2,1), dtype='uint8')

    for i in range(0, np.size(D, 2)):
    
        mask[:,:,i] = cv2.threshold(D[:,:,i], 10, 1, cv2.THRESH_BINARY)[1]
        opening[:,:,i] = cv2.morphologyEx(mask[:,:,i], cv2.MORPH_OPEN, kernel)
        
        
#def drop_supports(D):

        