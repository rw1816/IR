function [seqdata] = getseqinfo(fname)
%GETSEQINFO function to extracts information from FLIR .seq files
%   Functions gets information about header lengths in FLIR binary seq
%   files to enable reading of raw data without the FLIR atlas library.
%   Not tested at all, works with FLIR A35 at 320x256 res.
%   Probably/certainly will not work with other cams/resultions
%   File seems to have 3 "headers" that get in the way of reading the raw 
%   frame data
%   1. Main file header at the begining of the file
%   2. A footer after the first frame
%   3. A header for each frame

%this sequence always appears at the begining of a frame (in hex)
%00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 02 00 40 01 00 01 00 00 00 00 00 00 3F 01 00 00 FF 00 00 00 00 00 00 00 00 00 01 00 00 00 00 00
%in uint16 format bytes 18-19 and 20-21 are the horizontal and verticle
%resolution (320x256) in this case
%store the byte seqence in a vector (bytes in dec as this is what matlab
%expects)
framebeg=uint8([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,64,1,0,1,0,0,0,0,0,0,63,1,0,0,255,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0]);

%get a chunk of data from the begining of the file
fid=fopen(fname,'r');
fseek(fid,0,'bof');
%read 1MB from begining of file
filedata=fread(fid,1000000,'*uint8');
fclose(fid);

%find matches for the byte sequence - idx contains a vector of positions
%where a match is found
idx=strfind(filedata',framebeg);

%work out some lengths and store the results
seqdata.hres=320;
seqdata.vres=256;
seqdata.framelen=seqdata.hres*seqdata.vres*2;
seqdata.fileheadlen=idx(1)+length(framebeg)-1;
seqdata.frameheadlen=idx(3)-idx(2)-seqdata.framelen;
seqdata.firstframefootlen=idx(2)-idx(1)-seqdata.framelen-seqdata.frameheadlen;

end

