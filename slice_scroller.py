# -*- coding: utf-8 -*-
"""
Created on Mon Oct 26 15:09:59 2020

@author: rw1816
"""
import numpy as np
import matplotlib.pyplot as plt
import imageio

class IndexTracker(object):
    def __init__(self, ax, X):
        self.ax = ax
        ax.set_title('use scroll wheel to navigate images')

        self.X = X
        rows, cols, self.slices = X.shape
        self.ind = self.slices//2

        self.im = ax.imshow(self.X[:, :, self.ind])
        self.update()

    def onscroll(self, event):
        
        if event.button == 'up':
            self.ind = (self.ind + 1) % self.slices
        else:
            self.ind = (self.ind - 1) % self.slices
        self.update()

    def update(self):
        self.im.set_data(self.X[:, :, self.ind])
        ax.set_ylabel('slice %s' % self.ind)
        self.im.axes.figure.canvas.draw()


fig, ax = plt.subplots(1, 1)

filename = "F://OneDrive - Imperial College London//Post-doc//build_data//b1_220920//Accel_316_build12020-09-22_dwell_voxels.tiff"
T = imageio.volread(filename)
X=T.transpose()

tracker = IndexTracker(ax, X)

fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
plt.show()