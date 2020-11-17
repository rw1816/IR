@echo off

title Plot voxel data from FLIR A35 infra-red camera

set arg1=%1
exiftool %1

python 