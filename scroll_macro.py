#### import the simple module from the paraview
from paraview.simple import *
import time
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# get active source.
clip1 = GetActiveSource()

# Properties modified on clip1.ClipType
clip1.ClipType.Offset = 1.0

# Properties modified on clip1.ClipType
clip1.ClipType.Offset = 1.0
clip1.InsideOut=1
# find source
threshold1 = FindSource('Threshold1')

# find source
tIFFSeriesReader1 = FindSource('TIFFSeriesReader1')

# find source
accel_316_build1_joined_20200922_dwell_voxelstiff = FindSource('Accel_316_build1_joined_2020-09-22_dwell_voxels.tiff')

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1508, 813]

# get display properties
clip1Display = GetDisplayProperties(clip1, view=renderView1)

for i in range(0, 30):
	clip1.ClipType.Offset = i
	Render()
	time.sleep(0.5)

for i in range(41, 79):
	clip1.ClipType.Offset = i
	Render()
	time.sleep(0.5)