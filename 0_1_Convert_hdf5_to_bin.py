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
expfolder = "Z:\\chenghaz006_2018.9.4\\"
max_processes = 100

# where are your data?
storm_folder = expfolder + "acquisition\\"
input_directory = storm_folder + "bins\\"
output_directory = storm_folder + "real_bins\\"

# Mkdir for the output folder.
if not os.path.exists(output_directory):
    os.mkdir(output_directory)

# which imaging channels are you saving?
channels = ["750storm", "647storm", "561storm","488storm"]

# setup automated analysis
for channel in channels:
 #for  i in range (iterations):
    base = str(channel)
 # create list of all .hdf5 files in BIN directory
    h5_files =glob.glob(input_directory + base + "*.hdf5")
 # set path to multi-fit analysis code
    hdf5_to_bin = "C:/Program Files/Python36/Lib/site-packages/storm_analysis/sa_utilities/hdf5_to_bin.py"

 # start processes
    cmd_lines = []
    for h5_file in h5_files:
            
        print ("Found:", h5_file)
        h5_filename = os.path.basename(h5_file)
        print("Converting:",h5_filename)
        bin_out_name = output_directory + h5_filename[:-5] + ".bin"
        cmd_lines.append(['python', hdf5_to_bin,
                            "--hdf5", h5_file,
                            "--bin", bin_out_name
                            ])
    batchRun.batchRun(cmd_lines, max_processes = max_processes)
