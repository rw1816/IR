# IR
Codes to develop in-situ process monitoring with a FLIR Infra-Red camera
Dr Richard Williams
r.williams16@imperial.ac.uk

Imperial College London
October 2020

A series of functions and scripts to process FLIR A35 raw data into a stack of segmented tiffs for 3D visualisation and data analysis. Designed for use as an in-situ process monitoring tool for layerwise Additive Manufacturing processes. Most of the first half of the functions, which do all the heavy lifting and data processing, are called from the command line. The latter functions, for data inspection and visualisation, are of course GUI based. 

This package calls on the following:

seq2mat.m, written by Paul Hooper in MATLAB
exiftool.exe by Phil Harvey (https://exiftool.org/), which grabs metadata from the camera
ParaView (https://www.paraview.org/) for 3D data visualisation 

*** how to run *** 

--- processing the raw data into segmented tiffs ---

1. Run seq2mat.m from Paul's FLIR code, this will output a .mat of the recording.
	- cmd usage: 	

2. Run exiftool from the command line to output camera/ recording meta information
	- cmd usage: exiftool -w txt full/path/to/filename.seq

3. Run cropNdrop.py from the command line, follow programme. This will output a .npy of the isolated part.
	- cmd usage: python cropNdrop.py 

4. Run heat_map.py from the command line, this will output a .tiff xyz stack of the voxels of the part
	The tiff scalars represent the 'dwell temperature' of the part.
	- cmd usage: python heat_map.py 

*** for data visualisation ***

5. Load ParaView and open the .tiff file generated in step 3

6. Execute render.py from the Python shell in ParaView or with pvpython from cmd
	- cmd usage: pvpython render.py -i full/path/to/tiff_stack.tiff 

7. Save 'state' as a Paraview file .pvsm (must be in same folder as the tiff stack itself)

*** for numerical/ statistical analysis and plotting ***

8. 

9.
