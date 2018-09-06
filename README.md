# Batch-Analysis
The goal of this project is to build a GUI system for these STORM image analysis codes. 

Hopefully, the GUI can finish the following functions: 

  1 Test the parameters: 
    Organize the raw images: put Reg_beads, FFC, conventional, and STORM images under WorkDirectory/acquisition/. 
    Copy the XML folder into the WorkDirectory. 
    Change the XML parameters for STORM images, including: 
      Change the processing frames to the last 10 frames. 
      Foreground sigma (default 1.2)
      Smoothing sigma (default 1.2)
      Threshold
      Iterations and the background are normally fix as 20 and 8 respectively.
    Use "0_fitting_parameters_evaluation.py" to generate .hdf5 files, change: 
      The directory (expfolder). (line 20)
      The number of max_processes (default 100) (line 27)
    The files will be generated to WorkDirectory/bins/. 
    - Use "2_master_python_analysis.py" to convert the output from .hdf5 to .tiff: 
      Change the directory (line 19)
      Change the max_processes (line 26)
    The images will be generated under WorkDirectory/stormpngs/
    - Or alternatively use "0_1_convert_hdf5_to_bin.py" to convert the output files to bin files and examine them with insight3. The files will be generated under "WorkDirectory/acquisition/real_bins/"
    Remember to delete the test files manually after the parameter test. 
    
  2 STORM analysis and bead_warp analysis. 
    Change the XML parameters and "1_scmos_batch_fitting.py" like in step 1. 
    Beads warp imgaes will be generated under WorkDirectory/acquisition/bead_registration/. 
    
  3 Process the bead images: 
    Call "3_bead_image_processing.py", change the expfolder and fijifolder to WorkDirectory/. 
    There are something wrong with these codes: 
      The code can't transfer arguments to "C:\Users\Colenso\Fiji.app\macros\fiji_distcorr_make.py". The argument need to be manually typed in now. 
      The code can't communicate well with the "distortion correction" plugin of fiji. The window requiring changing of lambda value never shows up. For now, the plugin need to be run manually. 
      The ouput images are all dark. The lambda value used is typically 1e-7 ~ 1e-8, which is probably quite small. 
      
  4 XY alignment and render the images. 
    Call "4_XY_alignment", change the directory. (line 16 and 17)
    The matlab codes called by this file will do the XY alignment. It works fine so far. 
    The python code used to call fiji to render the images have some problems. Probably some modification is needed so that specific channels can be rendered. 
