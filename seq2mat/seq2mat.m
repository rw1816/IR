%   Paul Hooper - Imperial College London
%   paul.hooper@imperial.ac.uk

function [] = seq2mat(filename,nframestoconv)
%seq2mat this function converts a FLIR .seq file into a MATLAB .mat file
%   The function reads in the raw binary data from the seq and stores in a
%   matfile object. Using a matfile object allows files larger than RAM to
%   be proccessed with ease. It also compresses the data on the fly to
%   about 30% of the original size. Runs about as fast as Zipping
%   externally, maybe slightly quicker

%   Members of the matfile object are
%   m.I(:,:,n) stores the raw frame data in uint16 where n is the frame number.
%   m.nframes is the total number of frames

%   File header and frame headers are stored in binary and
%   not decoded into anything meaningful. This is so we have them if needed
%   at a later date.
%   m.seqfileheaderbytes is the main file header in uint8
%   m.seqfirstframefooterbytes is the main file header in uint8
%   m.frameheader(:,n) is the frame header in uint8 where n is the frame
%   number

%   nframestoconv specifies the number of frames to convert - used to
%   truncate the file when forgot to stop recording
%   the number of frames in the output is not strict and will be rounded up
%   to nearest buf_size

%check fileanme is valid
if exist(filename,'file')~=2
    error('File not found %s', filename);
    return;
end

% if nothing specified for n frames to convert, do whole file
if nargin<2
    nframestoconv=inf;
end
    
%get head offsets etc from seq
seqdata=getseqinfo(filename);

[fpath,fname,fext] = fileparts(filename);
m = matfile(fullfile(fpath,[fname '.mat']));
m.Properties.Writable = true;

fid=fopen(filename,'r');

%some initial arrays to get us started
m.I=uint16(zeros(seqdata.hres,seqdata.vres,2000));
m.frameheader=uint8(zeros(seqdata.frameheadlen,2000));

%read file header bytes
m.seqfileheaderbytes=fread(fid,seqdata.fileheadlen,'*uint8');
%read first frame
m.I(1:seqdata.hres,1:seqdata.vres,1)=fread(fid,[seqdata.hres seqdata.vres],'*uint16');
%read first frame footer bytes
m.seqfirstframefooterbytes=fread(fid,seqdata.firstframefootlen,'*uint8');

%now rest of file is frame header + frame data sequence
%calculate attempted read size, read multiple frames to speed things up
buf_size=2000;
read_size=(seqdata.frameheadlen+seqdata.framelen)*buf_size;
cframe=2;
tic;
while (~feof(fid) & (cframe<nframestoconv))
    data_buf=fread(fid,read_size,'*uint8');
    %check to see if all bytes where read (or we're at end of file)
    if length(data_buf)~=read_size
        buf_size=length(data_buf)/(seqdata.frameheadlen+seqdata.framelen);
    end
    %reshape the data so that the frame headers can be removed
    data_buf=reshape(data_buf,[seqdata.framelen+seqdata.frameheadlen,buf_size]);
    %store headers
    m.frameheader(1:seqdata.frameheadlen,cframe:(cframe+buf_size-1))=data_buf(1:seqdata.frameheadlen,:);
    %remove headers
    data_buf(1:seqdata.frameheadlen,:)=[];
    %store data in image array
    m.I(:,:,cframe:(cframe+buf_size-1))=reshape(typecast(data_buf(:), 'uint16'),[seqdata.hres,seqdata.vres,buf_size]);
    %update cframe
    cframe=cframe+buf_size;
    %display progress
    fpos=ftell(fid);
    disp(['Processed ' num2str(cframe) ' frames and ' num2str(fpos/10^6) ' MB']);
end
%save total number of frames
m.nframes=cframe;
disp('Done!');
toc
fclose(fid);

end
