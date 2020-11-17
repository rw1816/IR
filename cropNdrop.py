# -*- coding: utf-8 -*-
"""
First attempt at a script to deal with the FLIR IR camera data, working from matfile as produced by seq2mat
Aim to crop and downsample the data so it can fit in memory
Created on Wed Sep 30 18:39:31 2020
@author: rw1816
"""
import cv2
from tkinter import *
from tkinter.filedialog import askopenfilename
import h5py
from os import path
import numpy as np
import subprocess, sys

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

root=Tk()
root.withdraw() # we don't want a full GUI, so keep the root window from appearing
root.update()
root.filename = askopenfilename(title='Select matfile') # show an "Open" dialog box and return the path to the selected file
root.destroy()

meta_filename=(root.filename[0:-4] + '.txt')
with open(meta_filename, 'r') as f:
    lines=f.readlines()
    matching = [s for s in lines if "Frame Rate" in s]
    frame_rate = int(matching[0][-3:-1])

matfile = h5py.File(root.filename[0:-4] + '.mat')
nframes = matfile['nframes'][0][0]

frame_drop = input('frame rate = {0} fps. Keep every nth frame, pass nothing to keep all'.format(frame_rate)) #keep every nth frame
if frame_drop == '':
    frame_ind = 1
    
else:
    frame_ind = int(frame_drop)

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

#pull out the cropping coordinates, remember images are indexed [y,x] (row, column), as conventional matrices
y1 = ref_pt[0][1]
y2 = ref_pt[1][1]
x1 = ref_pt[0][0]
x2 = ref_pt[1][0]

I = np.zeros((y2-y1, x2-x1, int(nframes/frame_ind)+1 ), dtype='uint16') #declare a blank array we will read into, buffer size = 3000

for i in range(0, np.int(nframes)-1, frame_ind):  
    
    I[:, :, np.int(i/frame_ind)] = matfile['I'][i, y1:y2, x1:x2]
    if i % 10000 == 0:
        print('Completed {0} of {1} frames'.format(i, int(nframes/frame_ind)+1))
        
file_append = input('for multipart builds, type string to append to outfile name')
np.save(root.filename[0:-4] + file_append + '.npy', I)
print('Complete!')
    # from some reason the stack direction is [0] reading out of matfile,
    # so we broadcast into [x,y,z]


    
