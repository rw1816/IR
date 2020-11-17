# -*- coding: utf-8 -*-
"""
Created on Mon Oct 19 12:28:42 2020
Render the volume reconstruction of the part using ParaView

@author: rw1816"""

#### import the simple module from the paraview
from paraview.simple import *
import argparse

parser = argparse.ArgumentParser(description='Produce ParaView state file for tiff stack.')
parser.add_argument('tiff_path', metavar='-i', type=str, nargs='+', help='tiff file for ParaView')
args = parser.parse_args()

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# grab objects
reader = OpenDataFile(args.tiff_path[0])
tiff = GetActiveSource()
tiff.UseCustomDataSpacing = 1
tiff.CustomDataSpacing = [0.7, 0.7, 0.05]
renderView1 = GetActiveViewOrCreate('RenderView')

#changing interaction mode based on data extents
renderView1.InteractionMode = '3D'
renderView1.CameraPosition = [35.0, 29.0, 10000.0]
renderView1.CameraFocalPoint = [35.0, 29.0, 0.0]
renderView1.CameraViewUp = [0.0, 1.0, 0.0]
# get white background
renderView1.UseGradientBackground = 0
renderView1.Background = [1.0, 1.0, 1.0]

"""
Now perform a threshold on the vector space so only melted voxels are displayed
Exclude voxels which are zero or NaN
"""
threshold1 = Threshold(Input=tiff)
threshold1.Scalars = ['POINTS', 'Tiff Scalars']
threshold1.ThresholdRange = [20.0, 900.0]
renderView2 = GetActiveViewOrCreate('RenderView')

# Properties modified on tiffScalarsLUTColorBar
# get color legend/bar for tiffScalarsLUT in view renderView1
tiffScalarsLUT = GetColorTransferFunction('TiffScalars')
tiffScalarsLUTColorBar = GetScalarBar(tiffScalarsLUT, renderView1)
tiffScalarsLUTColorBar.TitleColor = [0.0, 0.0, 0.0]
tiffScalarsLUTColorBar.TitleFontSize = 8
tiffScalarsLUTColorBar.LabelColor = [0.0, 0.0, 0.0]
tiffScalarsLUTColorBar.ComponentTitle = '(\xc2\xbaC)'
tiffScalarsLUTColorBar.RangeLabelFormat = '%-5.3g'
tiffScalarsLUTColorBar.LabelFormat = '%-5.3g'
tiffScalarsLUTColorBar.NumberOfLabels = 8
tiffScalarsLUTColorBar.Title = 'Temperature'
tiffScalarsLUTColorBar.LabelFontSize = 8

# display props
thrs_display = GetDisplayProperties(threshold1, view=renderView2)

thrs_display.SetRepresentationType('Surface')
thrs_display.ColorArrayName = ['POINTS', 'Tiff Scalars']
thrs_display.LookupTable = tiffScalarsLUT
thrs_display.OSPRayScaleArray = 'Tiff Scalars'
thrs_display.OSPRayScaleFunction = 'PiecewiseFunction'
thrs_display.SelectScaleArray = 'Tiff Scalars'
# roughly 0.7mm pixel size by 0.05mm layer height 
threshold1.add_attribute('CustomDataSpacing', [0.7, 0.7, 0.05])

# set scalar coloring
thrs_display.ColorArrayName = ['POINTS', 'Tiff Scalars']
ColorBy(thrs_display, ('POINTS', 'Tiff Scalars'))
# rescale color and/or opacity maps used to include current data range
thrs_display.RescaleTransferFunctionToDataRange(True, False)

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
thrs_display.SetScalarBarVisibility(renderView1, True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
tiffScalarsLUT.ApplyPreset('jet', True)
tiffScalarsLUT.RGBPoints = [20.0, 0.0, 0.0, 0.5625, 84.44438000000001, 0.0, 0.0, 1.0, 231.74611, 0.0, 1.0, 1.0, 311.90789794921875, 0.5, 1.0, 0.5, 416.84210205078125, 1.0, 1.0, 0.0, 563.75, 1.0, 0.0, 0.0, 600.0, 0.5, 0.0, 0.0]
savepath = args.tiff_path[0][0:-5] + '.pvsm'
SaveState(savepath)

# create a new 'TIFF Series Reader'
#dwell_voxelstiff = TIFFSeriesReader(FileNames=['F:\\code\\ir\\dwell_voxels.tiff'])
#### uncomment the following to render all views
##RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
