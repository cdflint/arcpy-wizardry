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
import csv

# Save file in C:\python27\ArcgisX.X
#
# help function
# python AlterField.py -h
#
# example run
# python AlterField.py -w path/to/gdb-or-shapefile -f name-of-shapefile -c /path/to/csv

class AlterField(object):

    def _recursive(self):
        arcpy.env.workspace = self.workspace
        # generate a list of filed names from the feature class
        fields = [f.name for f in arcpy.ListFields(self.shapefile)]
        #print('list of field names generated')
        #
        n = 0
        #
        # if getYear is not needed comment out line 31, and remove variable/{value} from line 48
        getYear = self.shapefile[4:8]
        # open the csv file for read mode
        with open(self.csv, 'r') as csvfile:
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
                    arcpy.AlterField_management(self.shapefile, field, field, getYear +' '+ alias)
                    print('fields changed: {0}'.format(n))
                    # break

    def make(self, args):
        self.workspace = args.workspace
        self.shapefile = args.shapefile
        self.csv = args.csv
        print('reading {0} from directory {1}'.format(self.shapefile, self.workspace))
        print('using lookup table {0}'.format(self.csv))
        self._recursive()

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
