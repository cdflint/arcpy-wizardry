#! python 3
# -*- coding: utf-8 -*-
#

__author__ = "Carl Flint"

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
import zipfile
import tarfile
import time
import os


# Save file in C:\python27\ArcgisX.X
#
# help function
# python ExtractTool.py -h
#
# example run
# python ExtractTool.py -w path/to/workspace -o /path/to/output/folder -x .zip

class ExtractTool(object):

    def _findFiles(self):
        findList = []
        for root, dirs, files in os.walk(self.root):
            for file in files:
                if file.endswith(self.ext):
                    foundFile = os.path.join(root, file)
                    findList.append(foundFile)
                    print(foundFile)
            return findList

    def _extractZip(self):
        for xFile in self.fileList:
            with zipfile.ZipFile(xFile,'r') as zipf:
                zipf.extractall(self.output)

    def _extractTar(self):
        for xFile in self.fileList:
            with tarfile.open(xFile) as tar:
                tar.extractall(self.output)

    def make(self, args):
        self.root = args.root
        self.output = args.output
        self.ext = args.ext
        print('Reading directory {} \nFor files with extension {}'.format(self.root, self.ext))
        self.fileList = self._findFiles()
        if self.ext == ".zip":
            self._extractZip()
        elif self.ext == ".tar.gz" or self.ext == ".tar.bz2":
            self._extractTar()
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
