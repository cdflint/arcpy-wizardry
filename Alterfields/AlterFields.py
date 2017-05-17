#! python 3
# -*- coding: utf-8 -*-
#

__author__  = "Carl Flint"

import arcpy, argparse
import os, time, csv

# Save file in C:\python27\ArcgisX.X
#
# help function
# python AlterField.py -h
#
# example run
# python AlterField.py -w path/to/gdb-or-shapefile -f name-of-shapefile -c /path/to/csv

class AlterField(object):

    def _recursive(self, workspace, shapefile, csvFile):
        fc = shapefile
        csvFile = csvFile
        arcpy.env.workspace = workspace
        # generate a list of filed names from the feature class
        fields = [f.name for f in arcpy.ListFields(fc)]
        #print('list of field names generated')
        #
        n = 0
        #
        # if getYear is not needed comment out line 31, and remove variable/{value} from line 48
        getYear = fc[4:8]
        # open the csv file for read mode
        with open(csvFile, 'r') as csvfile:
            # skip the header of the columns
            #header = next(csv.reader(csvfile))
            # define csv reader
            spamReader = csv.reader(csvfile, delimiter=',')
            # iterate over all rows in the lookup table
            for row in spamReader:
                # only change the alias name if the field name is in the list of original names
                if row[0] in fields: # index positions may change from time to time
                    # get field name
                    field = row[0]
                    # get name of new alias
                    alias = row[1]
                    # confirm the change is taking place
                    n += 1
                    print('changing field name of {0} to a new alias of {1} {2}'.format(field, getYear, alias))
                    arcpy.AlterField_management(fc, field, field, getYear +' '+ alias)
                    print('fields changed: {0}'.format(n))
                    # break

    def make(self, args):
        self.workspace = args.workspace
        self.shapefile = args.shapefile
        self.csv = args.csv
        print('reading {0} from directory {1}'.format(self.shapefile, self.workspace))
        print('using lookup table {0}'.format(self.csv))
        self._recursive(self.workspace, self.shapefile, self.csv)

if __name__ == "__main__":
    # start global clock
    start = time.time()
    parser = argparse.ArgumentParser()
    # define workspace for function to grab shapefile/featureclass from
    parser.add_argument("-w", "--workspace", help="specify path to shapefile or gdb", default="")
    # define function to specify the shapefile
    parser.add_argument("-f", "--shapefile", help="shapefile in path or gdb", default="")
    # define function to specify the lookup table
    parser.add_argument("-c", "--csv", help="specify path to csv lookup table", default="")
    args = parser.parse_args()
    # call function and pass arguments
    AlterField().make(args)
    # end global clock and calculate run time
    end = time.time()
    runTime = end - start
    # print it just for kicks
    print('Batch process took {0} '.format(runTime))
