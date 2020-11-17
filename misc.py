# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 12:25:47 2020

@author: rw1816
"""


"""
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
ax = fig.gca(projection='3d')
surf=ax.plot_surface(xx, yy, D[:,:,10])


colours=plt.cm.viridis(D)
filled = colours[:,:,:,-1] != 0
#colours=explode(colours)
ax.voxels(filled,  edgecolor='k', facecolor=colours)

xx, yy = np.meshgrid(np.linspace(0,1,61), np.linspace(0,1,71))
zz=np.ones(np.shape(xx))
plt.contourf(xx, yy, D[:,:,0])

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_zlim([0, 50])
cset = ax.contourf(xx, yy, T[:,:,0], 100, zdir='z', offset=0, cmap='plasma')
plt.colorbar(cset)
#masked_data = np.ma.masked_where(D==0, D)
#T=raw2temp(masked_data)
for i in range(0, 50):
   cset = ax.contourf(xx, yy, T[:,:,i], 100, zdir='z', offset=i, cmap='plasma')
   plt.pause(0.001)
 """  
