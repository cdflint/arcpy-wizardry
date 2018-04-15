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

import arcpy, os, sys

# in development
#
# example run
# python forFCinGDB.py path/to/gdb

def listFcsInGDB(gdb):
  ''' list all feature classes in a geodatabase, including inside feature datasets '''
  arcpy.env.workspace = gdb
  print('Processing ', arcpy.env.workspace)

  fcs = []
  for fds in arcpy.ListDatasets('','feature') + ['']:
    for fc in arcpy.ListFeatureClasses('','',fds):
      fcs.append(os.path.join(fds, fc))
  return fcs

gdb = sys.argv [1]
fcs = listFcsInGDB(gdb)
for fc in fcs:
  print(fc)
