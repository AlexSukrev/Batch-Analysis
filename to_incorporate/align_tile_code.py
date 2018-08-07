
def align_tile(local_exp, slicenum,rel_conv_ints):
    leseg =  local_exp.split('/')
    rc_exp =  '/'.join(leseg[:-3]) + '/'
    storm_image_scale = int(10)
    acq_folder = local_exp + 'acquisition/'
    analysis_folder = local_exp + 'analysis/'
    ISanalysisfolder = analysis_folder + 'individual_sections/'
    rawstorm= analysis_folder + 'stormpngs/'
    rel_conv_ints = conv_ints(local_exp)

    #auto_to_image#
    channels = ["750storm", "647storm", "561storm","488storm"]
    output_directory = rawstorm
    input_directory = analysis_folder + "bins/"
    image_max = float(256)

    for channel in channels:
    # image_base = channel
     def file_compare(x, y):
         x = int(re.sub(r'[^\d]', r'', x))
         y = int(re.sub(r'[^\d]', r'', y))
         return cmp(x, y)
     if os.path.isfile(input_directory):
        bin_files = [input_directory + channel + '_' + "%02d" % int(slicenum) + 'mlist.hdf5']
     else:
        bin_files = sorted(glob.glob(input_directory + channel + '_'
                                     + "%02d" % int(slicenum) + 'mlist.hdf5'), file_compare)
     manual_1st = 0
     index = manual_1st
     for file in bin_files:
         # Sort out the file names
     #    index = int(file.split("_")[-2])
     #    out_name = output_directory + image_base + "_7%03d" % index
         name = os.path.basename(file)
         imgname = name[:-10]
         if file == (input_directory + channel + "_0001_mlist.bin"):
           out_name = output_directory + imgname
         else:
           out_name = output_directory + imgname

         
         print (file)
         if os.path.getsize(file)>100000:
             # Create image
             image_i3g = i3togrid.I3GData(file, scale = storm_image_scale)
             if (image_i3g.getNumberMolecules() > 0):
                 print (" -> " + out_name)
                 if file == (input_directory + channel + "_0001_mlist.bin"):
                     index = index
                 else:
                     index += 1

                 image = image_i3g.i3To2DGridAllChannelsMerged()
                 image = numpy.transpose(image).copy()
                 image = image/image_max
                 image[(image > 1.0)] = 1.0
            
                 if (len(sys.argv) == 6):
                     print ("  inverting image")
                     image = 1.0 - image
                 arraytoimage.singleColorImage(image, out_name, autoscale = False)
         else:
             print (str(os.path.getsize(file)) + "bin file is less than 100kb! bad molecule list")

    convfolder = acq_folder
    #save_all_conv#
    #this is modified from Hazen's dax_to_png.py
    files = glob.glob(convfolder + 'Visconv_' + "%02d" % int(slicenum) + '.dax')
    for file in files:
        print ("File:", os.path.basename(file))

        # load dax file
        dax_file = daxspereader.inferReader(file)
        image = dax_file.loadAFrame(16).astype(numpy.uint16)
        print (rel_conv_ints, " are the mean conventional intensitites ")
        print (int(rel_conv_ints[0]), " is the 488 mean intensity ")
        image = numpy.divide(image,int(rel_conv_ints[0]))

        pilimage = Image.fromarray(image,'I;16')
        #pilimage = pilimage.convert('L')
        pilimage = pilimage.rotate(-90)
        pilimage = pilimage.transpose(Image.FLIP_LEFT_RIGHT)

        # save the result
        name = os.path.basename(file)
        idx = name.split('_')
        index1 = idx[1]
        index = (int(index1[:3]))
        print (index)
        pilimage.save(ISanalysisfolder + "%04d" % index + "/rawimages/488" + name[:-4] + ".tif")
        
        #488ffc
        for i in range(9):
            im = Image.open(acq_folder + '488VisFFC_' + str(i) + '.tif')
            imnp = numpy.array(im)
            imnp = numpy.reshape(imnp,(640,640,1))
            if i == 0:
                imstack = imnp
            else:  
                imstack = numpy.concatenate((imstack, imnp), axis=2)
        avgim = numpy.average(imstack,axis=2)
        pilimage = Image.fromarray(avgim)
    
        ffc488np = ndimage.gaussian_filter(pilimage,5)
        ffc488np[ffc488np == 0] = 1
        ffc488mean = numpy.mean(ffc488np)
        print (ffc488mean)
             
       
        image = dax_file.loadAFrame(11).astype(numpy.uint16)
        print (int(rel_conv_ints[1]), " is the 561 mean intensity ")
        image = numpy.divide(image,int(rel_conv_ints[1]))
        


        pilimage = Image.fromarray(image,'I;16')
       # pilimage = pilimage.convert('L')
        pilimage = pilimage.rotate(-90)
        pilimage = pilimage.transpose(Image.FLIP_LEFT_RIGHT)

            # save the result
        pilimage.save(ISanalysisfolder + "%04d" % index + "/rawimages/561" + name[:-4] + ".tif")

        #561ffc
        for i in range(9):
         im = Image.open(acq_folder + '561VisFFC_' + str(i) + '.tif')
         imnp = numpy.array(im)
         imnp = numpy.reshape(imnp,(640,640,1))
         if i == 0:
             imstack = imnp
        else:  
             imstack = numpy.concatenate((imstack, imnp), axis=2)
        avgim = numpy.average(imstack,axis=2)
        pilimage = Image.fromarray(avgim)
        ffc561np = ndimage.gaussian_filter(pilimage,5)
        ffc561np[ffc561np == 0] = 1
        ffc561mean = numpy.mean(ffc561np)
        print (ffc561mean)
     
        image = dax_file.loadAFrame(6).astype(numpy.uint16)
        print (int(rel_conv_ints[2]), " is the 647 mean intensity ")
        image = numpy.divide(image,int(rel_conv_ints[2]))
       

        

        pilimage = Image.fromarray(image,'I;16')
       # pilimage = pilimage.convert('L')
        pilimage = pilimage.rotate(-90)
        pilimage = pilimage.transpose(Image.FLIP_LEFT_RIGHT)

            # save the result
        pilimage.save(ISanalysisfolder + "%04d" % index + "/rawimages/647" + name[:-4] + ".tif")

            #647Visffc
        for i in range(9):
         im = Image.open(acq_folder + '647VisFFC_' + str(i) + '.tif')
         imnp = numpy.array(im)
         imnp = numpy.reshape(imnp,(640,640,1))
        if i == 0:
            imstack = imnp
        else:  
            imstack = numpy.concatenate((imstack, imnp), axis=2)
        avgim = numpy.average(imstack,axis=2)
        pilimage = Image.fromarray(avgim)
        ffcVis647np = ndimage.gaussian_filter(pilimage,5)
        ffcVis647np[ffcVis647np == 0] = 1
        ffcVis647mean = numpy.mean(ffcVis647np)
        print (ffcVis647mean)

    files = glob.glob(convfolder + 'IRconv_' + "%03d" % int(slicenum) + '.dax')
    for file in files:
        print ("File:", os.path.basename(file))

            # load dax file
        dax_file = daxspereader.inferReader(file)
        image = dax_file.loadAFrame(6).astype(numpy.uint16)
        print (int(rel_conv_ints[3]), " is the 647IR mean intensity ")
        image = numpy.divide(image,int(rel_conv_ints[3]))
        


        pilimage = Image.fromarray(image,'I;16')
        #pilimage = pilimage.convert('L')
        pilimage = pilimage.rotate(-90)
        pilimage = pilimage.transpose(Image.FLIP_LEFT_RIGHT)

         # save the result
        name = os.path.basename(file)
        idx = name.split('_')
        index1 = idx[1]
        index = (int(index1[:3]))
        pilimage.save(ISanalysisfolder + "%04d" % index + "/rawimages/647" + name[:-4] + ".tif")

      #647IRffc
        for i in range(9):
         im = Image.open(acq_folder + '647IRFFC_' + str(i) + '.tif')
         imnp = numpy.array(im)
         imnp = numpy.reshape(imnp,(640,640,1))
        if i == 0:
            imstack = imnp
        else:  
            imstack = numpy.concatenate((imstack, imnp), axis=2)
        avgim = numpy.average(imstack,axis=2)
        
        pilimage = Image.fromarray(avgim)
        ffcIR647np = ndimage.gaussian_filter(pilimage,5)
        ffcIR647np[ffcIR647np == 0] = 1
        ffcIR647mean = numpy.mean(ffcIR647np)
        print (ffcIR647mean)

        image = dax_file.loadAFrame(1).astype(numpy.uint16)
        print (int(rel_conv_ints[4]), " is the 750 mean intensity ")

        image = numpy.divide(image,int(rel_conv_ints[4]))

        pilimage = Image.fromarray(image,'I;16')
       # pilimage = pilimage.convert('L')
        pilimage = pilimage.rotate(-90)
        pilimage = pilimage.transpose(Image.FLIP_LEFT_RIGHT)

            # save the result
        pilimage.save(ISanalysisfolder + "%04d" % index + "/rawimages/750" + name[:-4] + ".tif")
           
         ###750ffc
        for i in range(9):
         im = Image.open(acq_folder + '750IRFFC_' + str(i) + '.tif')
         imnp = numpy.array(im)
         imnp = numpy.reshape(imnp,(640,640,1))
        if i == 0:
            imstack = imnp
        else:  
            imstack = numpy.concatenate((imstack, imnp), axis=2)
        avgim = numpy.average(imstack,axis=2)
        pilimage = Image.fromarray(avgim)
        ffc750np = ndimage.gaussian_filter(pilimage, sigma=20)
        ffc750np[ffc750np == 0] = 1
        ffc750mean = numpy.mean(ffc750np)


        #apply ffc to conventional images
        i = int(slicenum)
        l = "%03d" % int(slicenum)
        im = Image.open((ISanalysisfolder + "%04d" % i + "/rawimages/488Visconv_" + l + ".tif"))
        #im = im.convert('L')
        imnp = numpy.array(im)*ffc488mean
        corr = numpy.array(imnp/ffc488np)
        pilimage = Image.fromarray(corr)
        #pilimage = pilimage.convert('L')
        pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/488Visconv_" + "%03d" % i + ".tif")
        
        im = Image.open((ISanalysisfolder + "%04d" % i + "/rawimages/561Visconv_" + l + ".tif"))
        #im = im.convert('L')
        imnp = numpy.array(im)*ffc561mean
        corr = numpy.array(imnp/ffc561np)
        pilimage = Image.fromarray(corr)
        #pilimage = pilimage.convert('L')
        pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/561Visconv_" + "%03d" % i + ".tif")

        im = Image.open((ISanalysisfolder + "%04d" % i + "/rawimages/647Visconv_" + l + ".tif"))
        #im = im.convert('L')
        imnp = numpy.array(im)*ffcVis647mean
        corr = numpy.array(imnp/ffcVis647np)
        pilimage = Image.fromarray(corr)
       # pilimage = pilimage.convert('L')
        pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/647Visconv_" + "%03d" % i + ".tif")

        im = Image.open((ISanalysisfolder + "%04d" % i + "/rawimages/647IRconv_" + l + ".tif"))
        #im = im.convert('L')
        imnp = numpy.array(im)*ffcIR647mean
        corr = numpy.array(imnp/ffcIR647np)
        pilimage = Image.fromarray(corr)
        #pilimage = pilimage.convert('L')
        pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/647IRconv_" + "%03d" % i + ".tif")

        im = Image.open((ISanalysisfolder + "%04d" % i + "/rawimages/750IRconv_" + l + ".tif"))
        #im = im.convert('L')
        imnp = numpy.array(im)*ffc750mean
        corr = numpy.array(imnp/ffc750np)
        pilimage = Image.fromarray(corr)
        #pilimage = pilimage.convert('L')
        pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/750IRconv_" + "%03d" % i + ".tif")

    i = int(slicenum)
    l = "%03d" % int(slicenum)
    stormfile = (rawstorm + "488storm_" + l + ".png")
    print (stormfile)
    if os.path.isfile(stormfile):
        #im = Image.open((stormfile)).convert("L")
        imeq = ImageOps.equalize(im)
        npeq = ndimage.gaussian_filter(imeq, sigma=1)
        ffc488up = ndimage.zoom(ffc488np, 10, order=1)
        imffc = numpy.multiply(npeq,numpy.log10(ffc488mean))
        imffc = numpy.divide(imffc,numpy.log10(ffc488up))
        pilimage = Image.fromarray(imffc)
        #pilimage = pilimage.convert('L')
        imadj = ImageOps.autocontrast(pilimage)
        pilimage.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/488storm_" + "%03d" % i + ".tif")

    stormfile = (rawstorm + "561storm_" + l + ".png")
    if os.path.isfile(stormfile):
        #im = Image.open((stormfile)).convert("L")
        imeq = ImageOps.equalize(im)
        npeq = ndimage.gaussian_filter(imeq, sigma=1)
        ffc561up = ndimage.zoom(ffc561np, 10, order=1)
        imffc = numpy.multiply(npeq,numpy.log10(ffc561mean))
        imffc = numpy.divide(imffc,numpy.log10(ffc561up))
        pilimage = Image.fromarray(imffc)
        #pilimage = pilimage.convert('L')
        imadj = ImageOps.autocontrast(pilimage)
        imadj.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/561storm_" + "%03d" % i + ".tif")

    stormfile = (rawstorm + "647storm_" + l + ".png")
    if os.path.isfile(stormfile):
        #im = Image.open((stormfile)).convert("L")
        imeq = ImageOps.equalize(im)
        npeq = ndimage.gaussian_filter(imeq, sigma=1)
        ffcVis647up = ndimage.zoom(ffcVis647np, 10, order=1)
        imffc = numpy.multiply(npeq,numpy.log10(ffcVis647mean))
        imffc = numpy.divide(imffc,numpy.log10(ffcVis647up))
        pilimage = Image.fromarray(imffc)
        #pilimage = pilimage.convert('L')
        imadj = ImageOps.autocontrast(pilimage)
        imadj.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/647storm_" + "%03d" % i + ".tif")

    stormfile = (rawstorm + "750storm_" + l + ".png")
    if os.path.isfile(stormfile):
        #im = Image.open((stormfile)).convert("L")
        imeq = ImageOps.equalize(im)
        npeq = ndimage.gaussian_filter(imeq, sigma=1)
        ffc750up = ndimage.zoom(ffc750np, 10, order=1)
        imffc = numpy.multiply(npeq,numpy.log10(ffc750mean))
        imffc = numpy.divide(imffc,numpy.log10(ffc750up))
        pilimage = Image.fromarray(imffc)
       # pilimage = pilimage.convert('L')
        imadj = ImageOps.autocontrast(pilimage)
        imadj.save(ISanalysisfolder + "%04d" % i + "/rawimages/for_matlab/750storm_" + "%03d" % i + ".tif")
    return
