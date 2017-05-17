#! python 3
# -*- coding: utf-8 -*-
#

__author__  = "Carl Flint"

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
