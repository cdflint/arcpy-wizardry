#! python 3
# -*- coding: utf-8 -*-
#

__author__  = "Carl Flint"

import arcpy, argparse
import os, time, csv

# Save file in C:\python27\ArcgisX.X
#
# help function
# python CalcField.py -h
#
# example run
# python CalcField.py -w path/to/Data.gdb -s name-of-shapefile -f fieldNAME -s startingValue -p prefixString

class CalcField(object):

    def _autoIncrement(self, workspace, shapefile, fieldList, startVal, prefixString):
        fc = shapefile
        updatefields = fieldList
        arcpy.env.workspace = workspace
        prefix = prefixString
        #print(prefixString)
        # get a count of rows in the feature class
        numberRows = arcpy.GetCount_management(fc)
        # get the length of the row count
        depth = int(len(numberRows.getOutput(0)))
        #print(depth)
        startVal = int(startVal)
        #print(startVal)
        x = ('{0}-{1:0{2}d}'.format(prefix,startVal,depth))
        print('Updating field/s {0} with autoIncrement values formatted as {1}'.format(updatefields, x))
        # define core requirements of arcpy.CalculateField_management
        py = "PYTHON"
        expression = "autoIncrement({0},'{1}',{2})".format(startVal,prefix,depth)
        # the code block looks like it should throw a python tab space error but its a multiline text block
        codeBlock = """
rec = 0
def autoIncrement(startValue, prefix, fieldDepth):
    global rec
    pStart = startValue
    pInterval = 1
    if (rec == 0):
        rec = pStart
    else:
        rec += pInterval
    return "{0}-{1:0{2}d}".format(prefix,rec,fieldDepth)"""
        # run to the hills
        # note some issues may be a result of lockfiles check to ensure all lockfiles are gone
        arcpy.CalculateField_management(fc, updatefields, expression, py, codeBlock)

    def make(self, args):
        self.workspace = args.workspace
        self.shapefile = args.shapefile
        self.fieldList = args.fieldList
        self.startVal = args.startVal
        self.prefixString = args.prefixString
        print('reading {0} from directory {1}'.format(self.shapefile, self.workspace))
        self._autoIncrement(self.workspace, self.shapefile, self.fieldList, self.startVal, self.prefixString)

if __name__ == "__main__":
    # start global clock
    start = time.time()
    parser = argparse.ArgumentParser()
    # define workspace for function to grab shapefile/featureclass from
    parser.add_argument("-w", "--workspace", help="specify path to shapefile or gdb", default="")
    # define function to specify the shapefile
    parser.add_argument("-s", "--shapefile", help="shapefile in path or gdb", default="")
    # define function to specify fields to update
    parser.add_argument("-f", "--fieldList", help="specify the field or fields to be updated", default="")
    # enter an integer for the auto numbering to begin from
    parser.add_argument("-v", "--startVal", help="specify an integer from which numbering begins", default="1")
    # enter field prefix
    parser.add_argument("-p", "--prefixString", help="specify field pretext if needed", default="")
    args = parser.parse_args()
    # call function and pass arguments
    CalcField().make(args)
    # end global clock and calculate run time
    end = time.time()
    runTime = end - start
    # print it just for kicks
    print('Batch process took {0} '.format(runTime))
