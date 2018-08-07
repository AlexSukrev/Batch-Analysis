import glob
import os
import sys
from PIL import Image, ImageFilter, ImageOps
import sa_library.datareader as daxspereader
import numpy
from scipy import misc, ndimage
import re
import sa_library.arraytoimage as arraytoimage
import sa_library.i3togrid as i3togrid
import math
import time

# where are your data?
expfolder = "Z:\\Colenso\\05_25_18_sample5\\"
acq_folder = expfolder + "acquisition\\"

# pass argument to FIJI (inelegant, but functional)
arg1 = "Z:/Colenso/05_25_18_sample5/"

# initialize lens distortion correction
print ("starting distortion correction generation")
if not os.path.isfile(acq_folder + "dist_corr/distCorr.txt"):
    # set cmd line arguments and open subprocess
    fijisub = ('C:\\Users\\Colenso\\Fiji.app\\ImageJ-win64' + ' -macro fiji_distcorr_make.py ' + arg1)
    print (fijisub)
    subprocess.Popen(fijisub, shell=True)

# look for distortion correction file to finish process
while not os.path.isfile(acq_folder + "dist_corr/distCorr.txt"):
    time.sleep(10)
print (str(coverslip)  + " fiji_dcorr_bead is finished")  
