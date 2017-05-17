#! python 3
# -*- coding: utf-8 -*-
#

__author__  = "Carl Flint"

import arcpy, argparse
import os, time

# Save file in C:\python27\ArcgisX.X
#
# help function
# python PDFtoTIFFv2.py -h
#
# example run
# python PDFtoTIFFv2.py -r path/to/PDFs -o /path/to/output/folder

class PDFtoTIFF(object):

    def _recursive(self, rootDir, outDir):
        rootdir = rootDir
        outdir = outDir
        arcpy.env.workspace = rootdir
        # do work
        # loop through files with extension pdf in root directory
        for x in arcpy.ListFiles('*.pdf'):
            # start the clock
            start = time.time()
            # strip file extension from fileName
            nameStrip = x[:-4]
            # add .tif to fileName
            nameTIFF = nameStrip+'.tif'
            # add feedback to cmd line as to what file we are on
            print('opening file %s' % nameStrip)
            # get the correct full file path for the pdf
            inPDF = os.path.join(rootdir,x)
            #print(inPDF)
            # get the correct full file path for the output tiff
            outTIFF = os.path.join(outdir, nameTIFF)
            #print(outTIFF)
            # use arcGIS like it wasn't intended to...
            arcpy.PDFToTIFF_conversion(inPDF,outTIFF)
            # stop the clock
            end = time.time()
            # calculate runTime
            runTime = end - start
            # print confirmation that file was created and took x time
            print(nameStrip+' converted to TIFF and took %s ' % runTime)


    def make(self, args):
        self.root = args.root
        self.output = args.output
        print('reading PDFs from directory %s' % self.root)
        print('writing TIFFs to directory %s' % self.output)
        self._recursive(self.root, self.output)

if __name__ == "__main__":
    # start global clock
    start = time.time()
    parser = argparse.ArgumentParser()
    # define workspace for function to grab pdf's from
    parser.add_argument("-r", "--root", help="directory of PDF files", default=".")
    # set output directory to place converted tiff's
    parser.add_argument("-o", "--output", help="output directory for TIFFs", default="")
    args = parser.parse_args()
    # call function and pass arguments
    PDFtoTIFF().make(args)
    # end global clock and calculate run time
    end = time.time()
    runTime = end - start
    # print it just for kicks
    print('Batch process took %s ' % runTime)
