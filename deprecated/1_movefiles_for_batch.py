import os
import glob
import math
import shutil

expfolder = "Z:\\Colenso\\05_25_18_sample5\\"
storm_folder = expfolder + "acquisition\\"

#files1 = glob.glob(storm_folder + "488storm*")
files2 = glob.glob(storm_folder + "647storm*")
files3 = glob.glob(storm_folder + "750storm*")
files4 = glob.glob(storm_folder + "IRconv*")
files5 = glob.glob(storm_folder + "Visconv*")
files6 = glob.glob(storm_folder + "IRffc*")
files7 = glob.glob(storm_folder + "Visffc*")
files8 = glob.glob(storm_folder + "IRbead_1_*")
files9 = glob.glob(storm_folder + "IRbead_2_*")
files10 = glob.glob(storm_folder + "Visbead_1_*")
files11 = glob.glob(storm_folder + "Visbead_2_*")


os.mkdir (expfolder + "storm\\")
os.mkdir (expfolder + "ffc\\")
os.mkdir (expfolder + "conv\\")
os.mkdir (expfolder + "registration\\")
os.mkdir (expfolder + "Region1\\")
os.mkdir (expfolder + "Region2\\")
os.mkdir (expfolder + "stormpngs\\")


storm = expfolder + "storm\\"
ffc = expfolder + "ffc\\"
conv = expfolder + "conv\\"
region1 = expfolder + "Region1\\"
region2 = expfolder + "Region2\\"          

#for file in files1:
 #shutil.move(file, storm)

for file in files2:
 shutil.move(file, storm)

for file in files3:
 shutil.move(file, storm)

for file in files4:
 shutil.move(file, conv)

for file in files5:
 shutil.move(file, conv)

for file in files6:
 shutil.move(file, ffc)

for file in files7:
 shutil.move(file, ffc)

for file in files8:
 shutil.move(file, region1)

for file in files9:
 shutil.move(file, region2)

for file in files10:
 shutil.move(file, region1)

for file in files11:
 shutil.move(file, region2)         
          
          
 

