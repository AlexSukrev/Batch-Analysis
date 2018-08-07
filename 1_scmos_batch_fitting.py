#!/usr/bin/python
#
# Batch multifit analysis.
# 
# Colenso 05_30_18

import glob
import os, time, datetime
import multiprocessing
import signal
import subprocess
import sys
import threading

import storm_analysis.sa_library.batch_run as batchRun
import storm_analysis.sa_library.datareader as datareader

# set path to raw data files
expfolder = "Z:\\chenghaz002_2018.7.23\\"
XML_folder = expfolder + "XMLs\\"

# set path to additional analysis files
analysis_files = "C:\\Batch_analysis\\"

# how many .DAX movies to analyze at once?
max_processes = 100

# set directory for raw STORM .DAX files
input_directory = expfolder + "acquisition\\"
# make directory for bead registration output

# create new directory for bead alignment files
if not os.path.exists(input_directory + "bead_registration\\"):
    os.mkdir(input_directory + "bead_registration\\")
bead_registration = input_directory + "bead_registration\\"

# create new directory for bin files
if not os.path.exists(input_directory + "bins\\"):
    os.mkdir (input_directory + "bins\\")
bin_folder = input_directory + "bins\\"

# If there are no previous STORM molecule lists found, start the STORM analysis
if not os.path.isfile(bin_folder + "647storm_00_mlist.bin"):
    # Which color channels are you analyzing?   
    #channels = ["750","647","561","488","IRbead","Visbead"]
    channels = ["750","647","561","488"]

    # setup automated STORM analysis
    for channel in channels:
     #for  i in range (iterations):
        base = str(channel)
        # set output directory for analyzed molecule lists
        output_directory = input_directory + "bins\\"
        # set path to analysis parameters
        multi_xml = XML_folder + base + ".xml"
        # set minimum length of .DAX file for analysis
        minimum_length = 100
        # create list of all .DAX files in STORM directory
        dax_files =glob.glob(input_directory + base + "*.dax")
        # set path to multi-fit analysis code
        mufit_exe = "C:/Program Files/Python36/Lib/site-packages/storm_analysis/sCMOS/scmos_analysis.py"

        # start processes
        cmd_lines = []
        # for each STORM movie
        for movie_file in dax_files:
            # read the file information and determine if it is long enough
            movie_obj = datareader.inferReader(movie_file)
            if(movie_obj.filmSize()[2] > minimum_length):
                # set file name parameters for jobs
                print("Analyzing:", movie_file,"with xml file",multi_xml)
                basename = os.path.basename(movie_file)
                mlistname = output_directory + "/" + basename[:-4] + "_mlist.hdf5"
                # start fitting
                cmd_lines.append(['python', mufit_exe,
                                  "--movie", movie_file,
                                  "--bin", mlistname,
                                  "--xml", multi_xml])
        # run the fitting in a batch with the specified number of concurrent processes
        batchRun.batchRun(cmd_lines, max_processes = max_processes)

# If there are no previous bead molecule lists found, start the bead analysis
if not os.path.isfile(bin_folder + "IRbead_1_00_647mlist.bin"):

    # set bead fitting channels
    channels = ["IRbead","Visbead"]

    # setup automated bead analysis
    for channel in channels:
        base = str(channel)
        # set output directory for analyzed molecule lists
        output_directory = input_directory + "bins\\"
        # set path to analysis parameters
        xml = ["Visbead_647.xml","Visbead_561.xml","Visbead_488.xml","IRbead_750.xml","IRbead_647.xml"]
   
        # set minimum length of .DAX file for analysis
        minimum_length = 100
        if channel == "IRbead":
            minimum_length = 10

        # create list of all .DAX files in bead directory
        dax_files =glob.glob(input_directory + base + "*.dax")
        #print (dax_files)
    
        # set path to multi-fit analysis code
        mufit_exe = "C:/Program Files/Python36/Lib/site-packages/storm_analysis/sCMOS/scmos_analysis.py"

        # start processes
        cmd_lines = []
        for movie_file in dax_files:
            movie_name = os.path.basename(movie_file[:-4])
            # run analysis on Visbeads
            if movie_name[0]=='V':

                movie_obj = datareader.inferReader(movie_file)
                if(movie_obj.filmSize()[2] > minimum_length):

                    basename = os.path.basename(movie_file)
                    mlistname = output_directory + "/" + basename[:-4]
                    # fit 647 portion of Visbead dax file
                    cmd_lines.append(['python', mufit_exe,
                                      "--movie", movie_file,
                                      "--bin", mlistname + "_647mlist.hdf5",
                                      "--xml", XML_folder + xml[0]])
                    print("Analyzing:", movie_file,"with xml file",xml[0])
                    # fit 561 portion of Visbead dax file
                    cmd_lines.append(['python', mufit_exe,
                                      "--movie", movie_file,
                                      "--bin", mlistname + "_561mlist.hdf5",
                                      "--xml", XML_folder + xml[1]])
                    print("Analyzing:", movie_file,"with xml file",xml[1])
                     # fit 488 portion of Visbead dax file
                    cmd_lines.append(['python', mufit_exe,
                                      "--movie", movie_file,
                                      "--bin", mlistname + "_488mlist.hdf5",
                                      "--xml", XML_folder + xml[2]])
                    print("Analyzing:", movie_file,"with xml file",xml[2])

            # run analysis on IRbeads
            elif movie_name[0]=="I":

                movie_obj = datareader.inferReader(movie_file)
                if(movie_obj.filmSize()[2] > minimum_length):

                    basename = os.path.basename(movie_file)
                    mlistname = output_directory + "/" + basename[:-4]
                    # fit 750 portion of IRbead dax file
                    cmd_lines.append(['python', mufit_exe,
                                      "--movie", movie_file,
                                      "--bin", mlistname + "_750mlist.hdf5",
                                      "--xml", XML_folder + xml[3]])
                    print("Analyzing:", movie_file,"with xml file",xml[3])
                    # fit 647 portion of IRbead dax file
                    cmd_lines.append(['python', mufit_exe,
                                      "--movie", movie_file,
                                      "--bin", mlistname + "_647mlist.hdf5",
                                      "--xml", XML_folder + xml[4]])
                    print("Analyzing:", movie_file,"with xml file",xml[4])
            
        batchRun.batchRun(cmd_lines, max_processes = max_processes)

# perform bead registration in MATLAB
print ("starting matlab gen_bead_warp analysis")
if not os.path.isfile(bead_registration + 'Cumulative_distribution_for_registration_self.tif'):
    matsub = ("""matlab -nosplash -nodisplay -r "arg1='""" + expfolder + """'; gen_bead_warp_hcam" """)
    subprocess.Popen(matsub ,shell=True)
          
while not os.path.isfile(bead_registration + 'Cumulative_distribution_for_registration_self.tif'):
    time.sleep(10)
print ("Bead alignment is finished")  
print("The test part is skipped" + "\n" + "Done! ")


#The following codes are for testing purpose. No need if everything works well in previous codes. 
#Note that the following code won't end as expected for a customized because the test images are saved under 'Z:\Colenso\05_25_18_sample5\acquisition\bead_registration'

    #test warping transform on beads (only if two bead passes)
#if not os.path.isfile(bead_registration + 'Cumulative_distribution_for_registration_1_based_on_2.fig'):
#    print ("starting matlab_test_bead_warp")
#    matsub = ("""matlab -nosplash -nodisplay -r "arg1='""" + expfolder + """'; test_bead_warp_hcam" """)
#    subprocess.Popen(matsub ,shell=True)

#while not os.path.isfile(bead_registration + 'Cumulative_distribution_for_registration_1_based_on_2.fig'):
#    time.sleep(10)
#print ("Bead testing is finished")  
