#! python 3
# -*- coding: utf-8 -*-
#

__author__ = "Carl Flint"

import argparse
import os, time
import zipfile, tarfile

# Save file in C:\python27\ArcgisX.X
#
# help function
# python ExtractTool.py -h
#
# example run
# python ExtractTool.py -w path/to/workspace -o /path/to/output/folder -x .zip

class ExtractTool(object):

    def _findFiles(self, pathDir, tag):
        self.pathDir = pathDir
        self.tag = tag
        findList = []
        for root, dirs, files in os.walk(pathDir):
            for file in files:
                if file.endswith(tag):
                    #print(os.path.join(root, file))
                    foundFile = os.path.join(root, file)
                    findList.append(foundFile)
                    print(foundFile)
            return findList

    def _extractZip(self, fileList, targetDir):
        self.fileList = fileList
        self.targetDir = targetDir
        for xFile in fileList:
            with zipfile.ZipFile(xFile,'r') as zipf:
                zipf.extractall(targetDir)

    def _extractTar(self, fileList, targetDir):
        self.fileList = fileList
        for xFile in fileList:
            with tarfile.open(xFile) as tar:
                tar.extractall(targetDir)

    def make(self, args):
        self.root = args.root
        self.output = args.output
        self.ext = args.ext
        print('Reading directory {} \nFor files with extension {}'.format(self.root, self.ext))
        outList = self._findFiles(self.root, self.ext)
        if self.ext == ".zip":
            self._extractZip(outList, self.output)
        elif self.ext == ".tar.gz" or self.ext == ".tar.bz2":
            self._extractTar(outList, self.output)
        else:
            print("Desired compression format not recognized")
        print('Writing output to {} '.format(self.output))

if __name__ == "__main__":
    # start the clock
    start = time.time()
    parser = argparse.ArgumentParser()
    # define workspace directory
    parser.add_argument("-r", "--root", help="directory that contains compressed files", default="C:/temp")
    # define output directory
    parser.add_argument("-o", "--output", help="directory for output of script",default="C:/temp/output")
    # define file extension to search for
    parser.add_argument("-x", "--ext", help="file extension to be used", default=".zip")
    args = parser.parse_args()
    # call function and pass args
    ExtractTool().make(args)
    # stop the clock
    end = time.time()
    runTime = end - start
    print('Batch process took {}'.format(runTime))
