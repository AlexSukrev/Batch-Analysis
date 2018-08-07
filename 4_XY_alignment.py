import glob
import os
import sys
from PIL import Image, ImageFilter, ImageOps
import sa_library.datareader as daxspereader
import numpy
import subprocess
from scipy import misc, ndimage
import re
import sa_library.arraytoimage as arraytoimage
import sa_library.i3togrid as i3togrid
import math
import time

# where are your data?
expfolder = "Z:\\chenghaz002_2018.7.23\\"
fijifolder = "Z:\\chenghaz002_2018.7.23\\"

# set folder paths
acq_folder = expfolder + "acquisition\\"
bin_folder = acq_folder + "bins\\"
conv_folder = acq_folder
storm_folder = expfolder + "stormtiffs\\"

# build analysis folder
if not os.path.exists(expfolder + 'analysis\\'):                
    os.mkdir(expfolder + 'analysis\\')
    os.mkdir(expfolder + "analysis\\individual_sections\\")

# assign folder paths
s_analysisfolder = expfolder + "analysis\\"
ISanalysisfolder = s_analysisfolder + "individual_sections\\"

# build individual section folders
if not os.path.exists(ISanalysisfolder + '0000\\'):  
    files = glob.glob(acq_folder + "IRconv*.dax")
    for file in files:
        sectionfolder = os.path.basename(file)
        name = os.path.basename(file[:-4])
        idx = name.split('_')
        index = (int(idx[1]))
        strsequence = "%04d" % index
        os.mkdir (ISanalysisfolder + strsequence)
        os.mkdir (ISanalysisfolder + strsequence + "/rawimages/")
        os.mkdir (ISanalysisfolder + strsequence + "/aligned/")
        os.mkdir (ISanalysisfolder + strsequence + "/rawimages/for_matlab/")

# determine number of sections being analyzed and assign as object
slicenum = len(os.listdir(ISanalysisfolder))

# determine 99th percentile of intensity values for pixels in conventional images

# find all the Visconv movies
Visconv_files = glob.glob(acq_folder + 'Visconv_' + '*.dax')
if len(Visconv_files)>0:
        cnt = 0
# pad matrices
        aperc_v488 = [0]*len(Visconv_files)
        aperc_v561 = [0]*len(Visconv_files)
        aperc_v647 = [0]*len(Visconv_files)
        for file in Visconv_files:
            # read 647 image intensities and load to matrix
            dax_file = daxspereader.inferReader(file)
            image = dax_file.loadAFrame(6).astype(numpy.uint16)
            aperc_v647[cnt] = numpy.percentile(image, 99.999)
            # read 561 image intensities and load to matrix
            image = dax_file.loadAFrame(14).astype(numpy.uint16)
            aperc_v561[cnt] = numpy.percentile(image, 99.999)
            # read 488 image intensities and load to matrix
            image = dax_file.loadAFrame(19).astype(numpy.uint16)
            aperc_v488[cnt] = numpy.percentile(image, 99.999)
           
            cnt = cnt+1
            
# find all the IRconv movies
IRconv_files = glob.glob(acq_folder + 'IRconv_' + '*.dax')
if len(IRconv_files)>0:
        cnt = 0
        # pad matrices
        aperc_IR750 = [0]*len(IRconv_files)
        aperc_IR647 = [0]*len(IRconv_files)
        for file in IRconv_files:
            # read 750 image intensities and load to matrix
            dax_file = daxspereader.inferReader(file)
            image = dax_file.loadAFrame(1).astype(numpy.uint16)
            aperc_IR750[cnt] = numpy.percentile(image, 99.999)
            # read 647 image intensities and load to matrix
            image = dax_file.loadAFrame(6).astype(numpy.uint16)
            aperc_IR647[cnt] = numpy.percentile(image, 99.999)
            
            cnt = cnt+1

    # compute the mean 99th percentile for all images, convert to 8 bit depth, and save in a list          
rel_conv_ints = [0]*5
rel_conv_ints[0] =  numpy.mean(aperc_v488)/256
rel_conv_ints[1] =  numpy.mean(aperc_v561)/256
rel_conv_ints[2] =  numpy.mean(aperc_v647)/256
rel_conv_ints[3] =  numpy.mean(aperc_IR647)/256
rel_conv_ints[4] =  numpy.mean(aperc_IR750)/256
print (rel_conv_ints,"are the relative conventional intensities")

# determine the 99th percentile of intensity values for all pixels in the ffc images

# find all the VisFFC movies
VisFFC_files = glob.glob(acq_folder + 'VisFFC_' + '*.dax')
if len(VisFFC_files)>0:
        cnt = 0
# pad matrices
        aperc_v488 = [0]*len(VisFFC_files)
        aperc_v561 = [0]*len(VisFFC_files)
        aperc_v647 = [0]*len(VisFFC_files)
        for file in VisFFC_files:
# read 647 image intensities and load to matrix
            dax_file = daxspereader.DaxReader(file)
            image = dax_file.loadAFrame(16).astype(numpy.uint16)
            aperc_v647[cnt] = numpy.percentile(image, 99.95)
# read 561 image intensities and load to matrix
            image = dax_file.loadAFrame(44).astype(numpy.uint16)
            aperc_v561[cnt] = numpy.percentile(image, 99.95)
# read 488 image intensities and load to matrix
            image = dax_file.loadAFrame(59).astype(numpy.uint16)
            aperc_v488[cnt] = numpy.percentile(image, 99.95)

            cnt = cnt+1

# find all the IRFFC movies
IRFFC_files = glob.glob(acq_folder + 'IRFFC_' + '*.dax')
if len(IRFFC_files)>0:
        cnt = 0
# pad matrices
        aperc_IR750 = [0]*len(IRFFC_files)
        aperc_IR647 = [0]*len(IRFFC_files)
        for file in IRFFC_files:
# read 750 image intensities and load to matrix (adjusted to exclude small fraction of saturated pixels)
            dax_file = daxspereader.DaxReader(file)
            image = dax_file.loadAFrame(1).astype(numpy.uint16)
            aperc_IR750[cnt] = numpy.percentile(image, 99.95)
            # read 647 image intensities and load to matrix (adjusted to exclude small fraction of saturated pixels)
            image = dax_file.loadAFrame(6).astype(numpy.uint16)
            aperc_IR647[cnt] = numpy.percentile(image, 99.95)

            cnt = cnt+1

# compute the mean 99th percentile for all images, convert to 8 bit depth, and save in a list 
rel_ffc_ints = [0]*5
rel_ffc_ints[0] =  numpy.mean(aperc_v488)/256
rel_ffc_ints[1] =  numpy.mean(aperc_v561)/256
rel_ffc_ints[2] =  numpy.mean(aperc_v647)/256
rel_ffc_ints[3] =  numpy.mean(aperc_IR647)/256
rel_ffc_ints[4] =  numpy.mean(aperc_IR750)/256
print (rel_ffc_ints,"are the relative FFC intensities")


# find conventional images and save out for warping
Visconv_files = glob.glob(conv_folder + 'Visconv_*' + '.dax')
for file in Visconv_files:
    #print ("File:", os.path.basename(file))
    name = os.path.basename(file[:-4])
    idx = name.split('_')
    index = (int(idx[1]))
# load 488 Visconv images
    dax_file = daxspereader.inferReader(file)
    image = dax_file.loadAFrame(19).astype(numpy.uint16)
# normalize histogram
    print ("saving out Visconv images")
    #print (int(rel_conv_ints[0]), " is the 488 mean intensity ")
    image = numpy.floor_divide(image,int(rel_conv_ints[0]))
# generate image and convert to grayscale
    pilimage = Image.fromarray(image,'I;16')
    pilimage = pilimage.convert('L')
    #pilimage = pilimage.rotate(-90)
    #pilimage = pilimage.transpose(Image.FLIP_LEFT_RIGHT)
# save the result
    name = os.path.basename(file)
    pilimage.save(ISanalysisfolder + "%04d" % index + "/rawimages/488" + name[:-4] + ".tif")

# load 561 Visconv images
    dax_file = daxspereader.inferReader(file)
    image = dax_file.loadAFrame(14).astype(numpy.uint16)
# normalize histogram
    #print (rel_conv_ints, " are the mean conventional intensitites ")
    #print (int(rel_conv_ints[1]), " is the 561 mean intensity ")
    image = numpy.floor_divide(image,int(rel_conv_ints[1]))
# generate image and convert to grayscale
    pilimage = Image.fromarray(image,'I;16')
    pilimage = pilimage.convert('L')
    #pilimage = pilimage.rotate(-90)
    #pilimage = pilimage.transpose(Image.FLIP_LEFT_RIGHT)
# save the result
    name = os.path.basename(file)
    pilimage.save(ISanalysisfolder + "%04d" % index + "/rawimages/561" + name[:-4] + ".tif")

# load 647 Visconv images
    dax_file = daxspereader.inferReader(file)
    image = dax_file.loadAFrame(6).astype(numpy.uint16)
# normalize histogram
    #print (rel_conv_ints, " are the mean conventional intensitites ")
    #print (int(rel_conv_ints[2]), " is the 561 mean intensity ")
    image = numpy.floor_divide(image,int(rel_conv_ints[2]))
# generate image and convert to grayscale
    pilimage = Image.fromarray(image,'I;16')
    pilimage = pilimage.convert('L')
    #pilimage = pilimage.rotate(-90)
    #pilimage = pilimage.transpose(Image.FLIP_LEFT_RIGHT)
# save the result
    name = os.path.basename(file)
    pilimage.save(ISanalysisfolder + "%04d" % index + "/rawimages/647" + name[:-4] + ".tif")

for i in range(9):
# load 488 image data as array and resize
    im = Image.open(acq_folder + '488VisFFC_' + str(i) + '.tif')
    imnp = numpy.array(im)
    imnp = numpy.reshape(imnp,(640,640,1))
    if i == 0:
        imstack = imnp
    else:  
        imstack = numpy.concatenate((imstack, imnp), axis=2)
# average images 
    avgim = numpy.average(imstack,axis=2)
    pilimage = Image.fromarray(avgim)
# blur image 
    ffc488np = ndimage.gaussian_filter(pilimage,20)
    ffc488np[ffc488np == 0] = 1
    ffc488mean = numpy.mean(ffc488np)
    #print (ffc488mean)

# load 561 image data as array and resize
    im = Image.open(acq_folder + '561VisFFC_' + str(i) + '.tif')
    imnp = numpy.array(im)
    imnp = numpy.reshape(imnp,(640,640,1))
    if i == 0:
        imstack = imnp
    else:  
        imstack = numpy.concatenate((imstack, imnp), axis=2)
# average images 
    avgim = numpy.average(imstack,axis=2)
    pilimage = Image.fromarray(avgim)
# blur image 
    ffc561np = ndimage.gaussian_filter(pilimage,20)
    ffc561np[ffc561np == 0] = 1
    ffc561mean = numpy.mean(ffc561np)
    #print (ffc561mean, ' is the 561 FFC mean')

# load 647 image data as array and resize
    im = Image.open(acq_folder + '647VisFFC_' + str(i) + '.tif')
    imnp = numpy.array(im)
    imnp = numpy.reshape(imnp,(640,640,1))
    if i == 0:
        imstack = imnp
    else:  
        imstack = numpy.concatenate((imstack, imnp), axis=2)
# average images 
    avgim = numpy.average(imstack,axis=2)
    pilimage = Image.fromarray(avgim)
# blur image 
    ffcVis647np = ndimage.gaussian_filter(pilimage,20)
    ffcVis647np[ffcVis647np == 0] = 1
    ffcVis647mean = numpy.mean(ffcVis647np)
    #print (ffcVis647mean)

for i in range (slicenum):
    im = Image.open((ISanalysisfolder + "%04d" % i + "/rawimages/488Visconv_" + "%02d" % i + ".tif"))
    im = im.convert('L')
    imnp = numpy.array(im)*ffc488mean
    corr = numpy.array(imnp/ffc488np)
    pilimage = Image.fromarray(corr)
    pilimage = pilimage.convert('L')
    pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/488Visconv_" + "%03d" % i + ".tif")
        
    im = Image.open((ISanalysisfolder + "%04d" % i + "/rawimages/561Visconv_" + "%02d" % i + ".tif"))
    im = im.convert('L')
    imnp = numpy.array(im)*ffc561mean
    corr = numpy.array(imnp/ffc561np)
    pilimage = Image.fromarray(corr)
    pilimage = pilimage.convert('L')
    pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/561Visconv_" + "%03d" % i + ".tif")

    im = Image.open((ISanalysisfolder + "%04d" % i + "/rawimages/647Visconv_" + "%02d" % i + ".tif"))
    im = im.convert('L')
    imnp = numpy.array(im)*ffcVis647mean
    corr = numpy.array(imnp/ffcVis647np)
    pilimage = Image.fromarray(corr)
    pilimage = pilimage.convert('L')
    pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/647Visconv_" + "%03d" % i + ".tif")

IRconv_files = glob.glob(conv_folder + 'IRconv_*' + '.dax')
for file in IRconv_files:
    #print ("File:", os.path.basename(file))
    name = os.path.basename(file[:-4])
    idx = name.split('_')
    index = (int(idx[1]))
    # load 647 IRconv images
    dax_file = daxspereader.inferReader(file)
    image = dax_file.loadAFrame(6).astype(numpy.uint16)
    # normalize histogram
    print ("saving out IRconv images")
    #print (int(rel_conv_ints[3]), " is the 647IR mean intensity ")
    image = numpy.floor_divide(image,int(rel_conv_ints[3]))
    # generate image and convert to grayscale
    pilimage = Image.fromarray(image,'I;16')
    pilimage = pilimage.convert('L')
    #pilimage = pilimage.rotate(-90)
    #pilimage = pilimage.transpose(Image.FLIP_LEFT_RIGHT)
    # save the result
    name = os.path.basename(file)
    pilimage.save(ISanalysisfolder + "%04d" % index + "/rawimages/647" + name[:-4] + ".tif")

    # load 750 IRconv images
    dax_file = daxspereader.inferReader(file)
    image = dax_file.loadAFrame(1).astype(numpy.uint16)
    # normalize histogram
    #print (rel_conv_ints, " are the mean conventional intensitites ")
    #print (int(rel_conv_ints[4]), " is the 647IR mean intensity ")
    image = numpy.floor_divide(image,int(rel_conv_ints[4]))
    # generate image and convert to grayscale
    pilimage = Image.fromarray(image,'I;16')
    pilimage = pilimage.convert('L')
    #pilimage = pilimage.rotate(-90)
    #pilimage = pilimage.transpose(Image.FLIP_LEFT_RIGHT)
    # save the result
    name = os.path.basename(file)
    pilimage.save(ISanalysisfolder + "%04d" % index + "/rawimages/750" + name[:-4] + ".tif")

# set FFC image range    
for i in range(9):
# load 647IR image data as array and resize
    im = Image.open(acq_folder + '647IRFFC_' + str(i) + '.tif')
    imnp = numpy.array(im)
    imnp = numpy.reshape(imnp,(640,640,1))
    if i == 0:
        imstack = imnp
    else:  
        imstack = numpy.concatenate((imstack, imnp), axis=2)
# average images 
    avgim = numpy.average(imstack,axis=2)
    pilimage = Image.fromarray(avgim)
# blur image 
    ffcIR647np = ndimage.gaussian_filter(pilimage,20)
    ffcIR647np[ffcIR647np == 0] = 1
    ffcIR647mean = numpy.mean(ffcIR647np)
    #print (ffcIR647mean)

# load 750 image data as array and resize
    im = Image.open(acq_folder + '750IRFFC_' + str(i) + '.tif')
    imnp = numpy.array(im)
    imnp = numpy.reshape(imnp,(640,640,1))
    if i == 0:
        imstack = imnp
    else:  
        imstack = numpy.concatenate((imstack, imnp), axis=2)
# average images 
    avgim = numpy.average(imstack,axis=2)
    pilimage = Image.fromarray(avgim)
# blur image 
    ffc750np = ndimage.gaussian_filter(pilimage, sigma=20)
    ffc750np[ffc750np == 0] = 1
    ffc750mean = numpy.mean(ffc750np)
    #print (ffc750mean)

for i in range (slicenum):
    im = Image.open((ISanalysisfolder + "%04d" % i + "/rawimages/647IRconv_" + "%02d" % i + ".tif"))
    im = im.convert('L')
    imnp = numpy.array(im)*ffcIR647mean
    corr = numpy.array(imnp/ffcIR647np)
    pilimage = Image.fromarray(corr)
    pilimage = pilimage.convert('L')
    pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/647IRconv_" + "%03d" % i + ".tif")

    im = Image.open((ISanalysisfolder + "%04d" % i + "/rawimages/750IRconv_" + "%02d" % i + ".tif"))
    im = im.convert('L')
    imnp = numpy.array(im)*ffc750mean
    corr = numpy.array(imnp/ffc750np)
    pilimage = Image.fromarray(corr)
    pilimage = pilimage.convert('L')
    pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/750IRconv_" + "%03d" % i + ".tif")


# find STORM images and save out for warping

channels = ["750","647","561","488"]
if os.path.isfile(ISanalysisfolder + "0000/Aligned/" + "Storm_" + "%02d" % i + "_mlist.tiff"):
    print ("storm movies ready for alignment")
else: 
    for channel in channels:
         base = str(channel)
    print ("Saving out STORM images for Matlab warp...")
    for i in range (slicenum):
        if os.path.isfile(storm_folder + base + "Storm_" + "%02d" % i + "_mlist.tiff"):
            im = Image.open(storm_folder + base + "Storm_" + "%02d" % i + "_mlist.tiff")
            im = im.convert('L')
            imeq = ImageOps.equalize(im)
            npeq = ndimage.gaussian_filter(imeq, sigma=1)
            ffc488up = ndimage.zoom(ffc488np, 10, order=1)
            imffc = numpy.multiply(npeq,numpy.log10(ffc488mean))
            imffc = numpy.divide(imffc,numpy.log10(ffc488up))
            pilimage = Image.fromarray(imffc)
            pilimage = pilimage.convert('L')
            imadj = ImageOps.autocontrast(pilimage)
            pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/"
                        + base + "storm_" + "%03d" % i + ".tif")

#apply warping transform to images
print ("starting Matlab image alignment...")

if not os.path.isfile(ISanalysisfolder + "%04d" % (slicenum-1)
                      + "/aligned/488Visconv_" + "%03d" % (slicenum-1) + ".tif"):
    matsub = ("""matlab -nosplash -nodisplay -r "arg1='""" + expfolder + """'; image_chrom_align_hcam" """)
    subprocess.check_call(matsub ,shell=True)

while not os.path.isfile(ISanalysisfolder + "%04d" % (slicenum-1)
                         + "/aligned/488Visconv_" + "%03d" % (slicenum-1) + ".tif"):
    print ("...still waiting...")
    time.sleep(60) 
#apply distortion correction and tiling in fiji

print ("Matlab image alignment is finished, starting lens distortion correction...") 

# pass argument to FIJI (inelegant, but functional)
arg2 = fijifolder

print ("starting fiji_dcorr")
# set cmd line arguments and open subprocess
fijisub = ('C:\\Users\\Colenso\\Fiji.app\\ImageJ-win64' + ' -macro fiji_distcorr1field_hcam.py ' + arg2)
subprocess.check_call(fijisub ,shell=True)
        
#    while not os.path.exists(testobj):
#        time.sleep(10)
print ("XY alignment is done!")  




