#! python 3
# -*- coding: utf-8 -*-
#

__author__  = "Carl Flint"

# Copyright 2017 Carl Flint
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import argparse
import arcpy
import time
import os

# Save file in C:\python27\ArcgisX.X
#
# help function
# python PDFtoTIFFv2.py -h
#
# example run
# python PDFtoTIFFv2.py -r path/to/PDFs -o /path/to/output/folder

class PDFtoTIFF(object):

    def _recursive(self):
        arcpy.env.workspace = self.root
        # do work
        # loop through files with extension pdf in root directory
        for x in arcpy.ListFiles('*.pdf'):
            # strip file extension from fileName
            nameStrip = x[:-4]
            # add .tif to fileName
            nameTIFF = nameStrip+'.tif'
            # add feedback to cmd line as to what file we are on
            print('opening file {}'.format(nameStrip))
            # get the correct full file path for the pdf
            inPDF = os.path.join(self.root,x)
            #print(inPDF)
            # get the correct full file path for the output tiff
            outTIFF = os.path.join(self.output, nameTIFF)
            #print(outTIFF)
            # use arcGIS like it wasn't intended to...
            arcpy.PDFToTIFF_conversion(inPDF,outTIFF)

    def make(self, args):
        self.root = args.root
        self.output = args.output
        print('reading PDFs from directory {}'.format(self.root))
        print('writing TIFFs to directory {}'.format(self.output))
        self._recursive()


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
    print('Batch process took {}'.format(runTime))
