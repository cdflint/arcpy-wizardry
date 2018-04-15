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
import urllib
import json
import time
import csv
import os


# Save file in C:\python27\ArcgisX.X
#
# help function
# python SingleLineAddress.py -h
#
# example run
# python SingleLineAddress.py -r path/to/workspace -c input.csv -j output.json

class SingleLineAddress(object):
    def _CSVtoJson(self):
        # json template where data is to be appended
        records = {'records':[]}
        # read the csv file that contains addresses in column with name address
        with open(os.path.join(self.workSpace, str(self.csvFile)),'r') as f:
            reader = csv.DictReader(f)
            for i in reader:
                records['records'].append({
                    'attributes':{
                    'SingleLine': i['address']
                    }
                    })
        return records

    def _hitServer(self):
        # build query structure for geocoding service
        data = {'addresses': self.records,
                'outSR' : 4326,
                'f': 'pjson'}
        # html'ify the query data
        url_values = urllib.urlencode(data)
        # pass the data to the geocoder
        result = urllib.urlopen(self.url, url_values).read()
        # export result for saving
        return result

    def _saveJson(self):
        self.outFile = self.outFile + '.json'
        # create a file if it doesn't exist and write the data
        with open(os.path.join(self.workSpace, str(self.outFile)),'w') as f:
            json.dump(json.loads(self.result), f, indent=2, sort_keys=True)

    def _saveCSV(self):
        self.outFile = self.outFile + '.csv'
        # parse json
        parsed_json = json.loads(self.result)
        # create a file if it doesn't exist and write the data
        with open(os.path.join(self.workSpace, self.outFile), 'w') as f:
            writer = csv.writer(f, delimiter=',')
            for i in parsed_json['locations']:
                row = [i['address'],i['location']['y'],i['location']['x']]
                writer.writerow(row)

    def build(self, args):
        self.workSpace = args.workspace
        self.csvFile = args.csvFile
        self.type = args.type
        self.outFile = args.outFile
        # url for MD iMAP composite geocoding service
        self.url = 'https://geodata.md.gov/imap/rest/services/GeocodeServices/MD_CompositeLocator/GeocodeServer/geocodeAddresses'
        self.records = self._CSVtoJson()
        self.result = self._hitServer()
        if self.type == 'json':
            self._saveJson()
        elif self.type == 'csv':
            self._saveCSV()
        elif self.type == 'both':
            self._saveCSV()
            self._saveJson()
        else:
            err = 'Unsupported operation'
            raise Exception(err)

if __name__ == "__main__":
    # start the clock
    start = time.time()
    parser = argparse.ArgumentParser()
    # define workspace directory
    parser.add_argument('-r', '--workspace', help="directory to perform work in", default='C:/temp')
    # define input csv file
    parser.add_argument('-c', '--csvFile', help="csv file that contains an address field", default='input.csv')
    # define output type
    parser.add_argument('-t', '--type', help="specify output type [csv, json, both]", default='both')
    # define ouput file name
    parser.add_argument('-o', '--outFile', help="place to save the output and name of file", default='output')
    args = parser.parse_args()
    # call function and pass args
    SingleLineAddress().build(args)
    # stop the clock
    end = time.time()
    runTime = end - start
    print('Process took {}'.format(runTime))
