# -*- coding: utf-8 -*-
"""
First attempt at a script to deal with the FLIR IR camera data, working from matfile as produced by seq2mat
Aim to crop and downsample the data so it can fit in memory
Created on Wed Sep 30 18:39:31 2020
@author: rw1816
"""
import cv2
import argparse
import tkinter as tk
from tkinter.filedialog import askopenfilename
import h5py

ref_pt = []
cropping = False

def draw_box(event, x, y, flags, param):

    global ref_pt, cropping
    
    if event == cv2.EVENT_LBUTTONDOWN:
        
        ref_pt = [(x, y)]
        cropping = True
        
    elif event == cv2.EVENT_LBUTTONUP:
        
        ref_pt.append((x,y))
        cropping = False

    cv2.rectangle(img, ref_pt[0], ref_pt[1], (0, 255, 0), 2)
    cv2.imshow("Select area to keep", img)

#tk.withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename(title='Select matfile') # show an "Open" dialog box and return the path to the selected file
matfile = h5py.File(filename)
nframes = matfile['nframes'][0][0]

frame_drop = input('Keep every nth frame, pass nothing to keep all') #keep every nth frame
if frame_drop == 0:
    frame_ind = 1
    
else:
    frame_ind = frame_drop

img = matfile['I'][nframes/2, :, :] 
img=img*255
clone = img.copy()
cv2.namedWindow("Select area to keep")
cv2.setMouseCallback("Select area to keep", draw_box)

while True:
	# display the image and wait for a keypress
	cv2.imshow("Select area to keep", img)
	key = cv2.waitKey(1) & 0xFF
	# if the 'r' key is pressed, reset the cropping region
	if key == ord("r"):
		img = clone.copy()
	# if the 'c' key is pressed, break from the loop
	elif key == ord("c"):
		break

if len(ref_pt) == 2:
	roi = clone[ref_pt[0][1]:ref_pt[1][1], ref_pt[0][0]:ref_pt[1][0]]
	cv2.imshow("Cropped frame", roi)
	cv2.waitKey(0)
    
cv2.destroyAllWindows()
print(ref_pt)
#I = np.zeros((256, 320, 3000)) #declare a blank array we will read into, buffer size = 3000
#
#for i in range(0, int(nframes+1)):  
#    
#    I[:, :, i] = matfile['I'][i, :, :]
#    
#    I = cv2.adaptiveThreshold(I, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    #from some reason the stack direction is [0] reading out of matfile,
    #so we broadcast into [x,y,z]
    
