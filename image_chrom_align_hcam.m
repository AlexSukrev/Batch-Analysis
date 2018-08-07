%clear all
%arg1 = 'Z:\Colenso\05_25_18_sample5\'
local_exp =  arg1;
rel_conv_ints = '1111';
analysisfolder = cat(2, local_exp, 'analysis/');
ISanalysisfolder = cat(2, analysisfolder, 'individual_sections/');
%folders for merged image ouput
%mergeconv = cat(2, analysisfolder, 'unaligned/conv_merged/');
%mergestorm = cat(2, analysisfolder, 'unaligned/storm_merged/');
%conv561only = cat(2, analysisfolder, 'unaligned/conv_561/');
%mergeconv488561 = cat(2, analysisfolder, 'unaligned/conv_561_storm_488/');
%folders for downsampled merged image output
%mergeconvds = cat(2, analysisfolder, 'unaligned/conv_merged_ds/');
%mergestormds = cat(2, analysisfolder, 'unaligned/storm_merged_ds/');
%conv561onlyds = cat(2, analysisfolder, 'unaligned/conv_561_ds/');
%mergeconv488561ds = cat(2, analysisfolder, 'unaligned/conv_561_storm_488_ds/');

%local = num2str(local_exp);
%disp(local)
%disp (' is my local exp')
%c = strsplit(local, '/');
%cs = c(end)
%disp (' is the coverslip number')

acq_path = cat(2, local_exp, 'acquisition/');
slices = (numel(dir(fullfile(ISanalysisfolder, '0*')))-1);
% load transformation matrix
reg_pth = [local_exp 'acquisition/bead_registration/'];
load([reg_pth 'beadworkspace_region2_10x']);

%load([reg_pth 'IRbeadworkspace_region2_10x']);
%
for slice = 0:slices;
filename.storm488 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/rawimages/for_matlab/488storm_',sprintf('%03d',slice),'.tif');
filename.storm561 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/rawimages/for_matlab/561storm_',sprintf('%03d',slice),'.tif');
filename.storm647 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/rawimages/for_matlab/647storm_',sprintf('%03d',slice),'.tif');
filename.storm750 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/rawimages/for_matlab/750storm_',sprintf('%03d',slice),'.tif');
filename.convVis488 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/rawimages/for_matlab/488Visconv_',sprintf('%03d',slice),'.tif');
filename.convVis561 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/rawimages/for_matlab/561Visconv_',sprintf('%03d',slice),'.tif');
filename.convVis647 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/rawimages/for_matlab/647Visconv_',sprintf('%03d',slice),'.tif');
filename.convIR647 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/rawimages/for_matlab/647IRconv_',sprintf('%03d',slice),'.tif');
filename.convIR750 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/rawimages/for_matlab/750IRconv_',sprintf('%03d',slice),'.tif');
filenameout.storm488 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/488storm_',sprintf('%03d',slice),'.tif');
filenameout.storm647 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/647storm_',sprintf('%03d',slice),'.tif');
filenameout.storm561 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/561storm_',sprintf('%03d',slice),'.tif');
filenameout.storm750 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/750storm_',sprintf('%03d',slice),'.tif');
filenameout.convVis488 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/488Visconv_',sprintf('%03d',slice),'.tif');
filenameout.convVis561 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/561Visconv_',sprintf('%03d',slice),'.tif');
filenameout.convVis647 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/647Visconv_',sprintf('%03d',slice),'.tif');
filenameout.convIR647 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/647IRconv_',sprintf('%03d',slice),'.tif');
filenameout.convIR750 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/750IRconv_',sprintf('%03d',slice),'.tif');
filenameout.conv7502 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/750IRconv_',sprintf('%03d',slice),'_3.tif');

%filenameoufilenameout.convIR750 = strcat(ISanalysisfolder,sprintf('%04d',slice),'/aligned/750IRconv_',sprintf('%03d',slice),'.tif');t.convmerge = strcat(mergeconv,sprintf('%02d',cs),'_',sprintf('%03d', slice),'.tif');
%filenameout.stormmerge = strcat(mergestorm,sprintf('%02d',cs),'_',sprintf('%03d', slice),'.tif');
%filenameout.conv561only = strcat(conv561only,sprintf('%02d',cs),'_',sprintf('%03d', slice),'.tif');
%filenameout.mergeconv488561 = strcat(mergeconv488561,sprintf('%02d',cs),'_',sprintf('%03d', slice),'.tif');
%filenameout.convmergeds = strcat(mergeconvds,sprintf('%02d',cs),'_',sprintf('%03d', slice),'.tif');
%filenameout.stormmergeds = strcat(mergestormds,sprintf('%02d',cs),'_',sprintf('%03d', slice),'.tif');
%filenameout.conv561onlyds = strcat(conv561onlyds,sprintf('%02d',cs),'_',sprintf('%03d', slice),'.tif');
%filenameout.mergeconv488561ds = strcat(mergeconv488561ds,sprintf('%02d',cs),'_',sprintf('%03d', slice),'.tif');
%filenameout.conv7502 = strcat(analysisfolder,sprintf('%04d',slice),'/aligned/750conv_',sprintf('%03d',slice),'_3.tif');

if exist(filenameout.conv7502)==0
% load data
im.conv488 = im2double(imread(filename.convVis488));
im.conv488 = imresize(im.conv488,10)./ str2double(rel_conv_ints(4));
im.conv488adj = imadjust(im.conv488,stretchlim(im.conv488,[0.8 1]),[0 1]);

im.conv561 = im2double(imread(filename.convVis561));
im.conv561 = imresize(im.conv561,10)./str2double(rel_conv_ints(3));
im.conv561adj = imadjust(im.conv561,stretchlim(im.conv561,[0 1]),[0 1]);

im.conv647 = im2double(imread(filename.convVis647));
im.conv647 = imresize(im.conv647,10)./str2double(rel_conv_ints(2));
im.conv647adj = imadjust(im.conv647,stretchlim(im.conv647,[0 1]),[0 1]);

im.convIR647 = im2double(imread(filename.convIR647));
im.convIR647 = imresize(im.convIR647,10)./str2double(rel_conv_ints(2));
im.convIR647adj = imadjust(im.convIR647,stretchlim(im.convIR647,[0 1]),[0 1]);

im.conv750 = im2double(imread(filename.convIR750));
im.conv750 = imresize(im.conv750,10)./str2double(rel_conv_ints(1));
im.conv750adj = imadjust(im.conv750,stretchlim(im.conv750,[0 1]),[0 1]);
disp('images loaded')
if exist(filename.storm488)==2

im.storm488 = im2double(imread(filename.storm488));
else
im.storm488 = im.conv488adj;
end

%im.storm561 = im2double(imread(filename.storm561));
if exist(filename.storm647)==2
im.storm647 = im2double(imread(filename.storm647));
else
im.storm647 = im.conv647adj;
end

if exist(filename.storm750)==2
im.storm750 = im2double(imread(filename.storm750));
else
im.storm750 = im.conv750adj;
end

%correct for storm to conv drift
[output.storm488] = dftregistration(fft2(im.conv488adj),fft2(im.storm488),100);

%[output.storm561] = dftregistration(fft2(im.conv561adj),fft2(im.storm561),100);

[output.storm647] = dftregistration(fft2(im.conv647adj),fft2(im.storm647),100);

[output.storm750] = dftregistration(fft2(im.conv750adj),fft2(im.storm750),100);

xform647 = [ 1  0  0
          0  1  0
         (output.storm647(4)) (output.storm647(3))  1 ];
tform_translate647 = maketform('affine',xform647);
imagesize = size(im.conv647)
xdata = [1 imagesize(2)];
ydata = [1 imagesize(1)];
imreg.storm647 = imtransform(im.storm647, tform_translate647, 'XData',xdata,'YData',ydata);

%xform561 = [ 1  0  0
%          0  1  0
%         (output.storm561(4)) (output.storm561(3))  1 ];
%tform_translate561 = maketform('affine',xform561);
%imreg.storm561 = imtransform(im.storm561, tform_translate561, 'XData',xdata,'YData',ydata);

xform488 = [  1  0  0
          0  1  0
         (output.storm488(4)) (output.storm488(3))  1 ];
tform_translate488 = maketform('affine',xform488);
[imreg.storm488] = imtransform(im.storm488, tform_translate488, 'XData',xdata,'YData',ydata);

xform750 = [  1  0  0
          0  1  0
        (output.storm750(4)) (output.storm750(3))  1 ];
tform_translate750 = maketform('affine',xform750);
[imreg.storm750] = imtransform(im.storm750, tform_translate750, 'XData',xdata,'YData',ydata);
%pad images for warping

[im.conv488_warp] = imtransform(im.conv488, tform_488_2_647,'XData',[1 imagesize(2)],'YData',[1 imagesize(1)]);
[im.conv561_warp] = imtransform(im.conv561, tform_561_2_647,'XData',[1 imagesize(2)],'YData',[1 imagesize(1)]);
[im.conv750_warp] = imtransform(im.conv750, tform_750_2_647,'XData',[1 imagesize(2)],'YData',[1 imagesize(1)]);

%if exist(filename.storm488)==2

[im.storm488_warp] = imtransform(imreg.storm488, tform_488_2_647,'XData',[1 imagesize(2)],'YData',[1 imagesize(1)]);
%[im.storm561_warp] = imtransform(imtrans.storm561, tform_ 561_ 2_ 647,'XData',[1 6000],'YData',[1 6000]);
[im.storm750_warp] = imtransform(imreg.storm750, tform_750_2_647,'XData',[1 imagesize(2)],'YData',[1 imagesize(1)]);
%end
disp('storm images aligned')

%translate 647Visconv to 647IRconv
%[output.conv647] = dftregistration(fft2(im.convIR647),fft2(im.conv647),100);
%xform647 = [ 1  0  0
        %  0  1  0
         %(output.conv647(4)) (output.conv647(3))  1 ];
%tform_translate647 = maketform('affine',xform647);
%xdata = [1 2560];
%ydata = [1 2560];
%im.conv647 = imtransform(im.conv647, tform_translate647, 'XData',xdata,'YData',ydata);
%im.conv488_warp = imtransform(im.conv488_warp, tform_translate647, 'XData',xdata,'YData',ydata);
%im.conv561_warp = imtransform(im.conv561_warp, tform_translate647, 'XData',xdata,'YData',ydata);

%if exist(filename.storm488)==2

%im.storm488_warp = imtransform(im.storm488_warp, tform_translate647, 'XData',xdata,'YData',ydata);
%im.storm561_warp = imtransform(im.storm561_warp, tform_translate647, 'XData',xdata,'YData',ydata);
%end
%save files
%im.rg_conv = cat(3, im.conv647, im.conv750_warp, im.conv488_warp);
%imwrite(im.rg_conv, filenameout.convrgb);
imwrite(im.conv488_warp, filenameout.convVis488);
imwrite(im.conv561_warp, filenameout.convVis561);
imwrite(im.conv647, filenameout.convVis647);
%imwrite(im.convIR647_warp, filenameout.convIR647);
imwrite(im.conv750_warp, filenameout.convIR750);
%if exist(filename.storm488)==2
imwrite(imreg.storm647, filenameout.storm647);
%imwrite(im.storm561_warp, filenameout.storm561);
imwrite(im.storm488_warp, filenameout.storm488);
imwrite(im.storm750_warp, filenameout.storm750);
disp('chromatic alignment done')


% write out merged images 
%im.conv_rgb = cat(3. im.conv647,im.conv750_warp,im.conv488_warp);
%imwrite(im.conv_rgb, filenameout.mergeconv);

%im.storm_rgb = cat(3, im.storm647,im.storm750_warp,im.storm488_warp);
%imwrite(im.storm_rgb, filenameout.stormmerge);

%imwrite(im.conv_561_warp, filenameout.conv561only);

%im.align561488 = imfuse(im.conv561_warp,im.conv488_warp);
%imwrite(im.align561488, filenameout.mergeconv488561);

%im.conv_rgbds = imresize(im.conv_rgb,0.1);
%imwrite(im.conv_rgbds, filenameout.mergeconvds);

%im.storm_rgbds = imresize(im.storm_rgb,0.1);
%imwrite(im.storm_rgbds, filenameout.stormmergeds);

%im.conv_561_warpds = imresize(im.conv561_warp,0.1);
%imwrite(im.conv_561_warpds, filenameout.conv561onlyds);
%
%im.align561488ds = imresize(im.align561488,0.1);
%imwrite(im.align561488ds, filenameout.mergeconv488561ds);
%end

end
end
%end
%disp(['done writing slice', num2str(slice)])
%if exist('im') == 1
%imwrite(imresize(im.conv750,0.05), filenameout.convIR7502);
%end
