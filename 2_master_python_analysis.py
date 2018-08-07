import os,sys,time
from subprocess import *
import glob
import numpy
import datareader
import re
import arraytoimage
import i3togrid
from PIL import Image
import math

import storm_analysis.sa_library.batch_run as batchRun
import storm_analysis.sa_library.datareader as datareader
import storm_analysis.sa_library.sa_h5py as saH5Py

#define variables
expfolder = "Z:\\chenghaz002_2018.7.23\\"
storm_image_scale = int(10)
max_processes = 200

# where are your data?
storm_folder = expfolder + "acquisition\\"
#conv_folder = expfolder + "conv\\"
input_directory = storm_folder + "bins\\"

# where do you want to save the data?
output_directory = expfolder + "stormpngs\\"

# Mkdir for the output folder. --- 7.30.2018. 
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# parameters for saving out images
# which imaging channels are you saving?
channels = ["750storm", "647storm", "561storm","488storm"]
# what sigma to use for rendering images in [channels]?
sigma_channels = [1,0.5,0.5,1]

# setup automated analysis
for channel in channels:
 #for  i in range (iterations):
    base = str(channel)
 # create list of all .hdf5 files in BIN directory
    h5_files =glob.glob(input_directory + base + "*.hdf5")
 # set path to multi-fit analysis code
    hdf5_to_image = "C:/Program Files/Python36/Lib/site-packages/storm_analysis/sa_utilities/hdf5_to_image.py"

 # start processes
    cmd_lines = []
    for h5_file in h5_files:
        if base == "750storm":
            sigma = sigma_channels[0]
        elif base == "647storm":
            sigma = sigma_channels[1]
        elif base == "561storm":
            sigma = sigma_channels[2]
        elif base == "488storm":
            sigma = sigma_channels[3]
            
        print ("Found:", h5_file)
        h5_filename = os.path.basename(h5_file)
        print("Analyzing:",h5_filename,"with sigma ",str(sigma))
        tiff_out_name = output_directory + h5_filename[:-5] + ".tiff"
        cmd_lines.append(['python', hdf5_to_image,
                            "--image", tiff_out_name,
                            "--bin", h5_file,
                            "--scale", str(storm_image_scale),
                            "--sigma", str(sigma)])
    batchRun.batchRun(cmd_lines, max_processes = max_processes)
