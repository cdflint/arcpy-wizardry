#! python 3
# -*- coding: utf-8 -*-
#

__author__ = "Carl Flint"

import argparse
import os, csv, time
import urllib, json

# Save file in C:\python27\ArcgisX.X
#
# help function
# python SingleLineAddress.py -h
#
# example run
# python SingleLineAddress.py -r path/to/workspace -c input.csv -j output.json

class SingleLineAddress(object):
    def _CSVtoJson(self, workSpace, csvFile):
        csvFile = csvFile
        rootDir = workSpace
        # json template where data is to be appended
        records = {'records':[]}
        # read the csv file that contains addresses in column with name address
        with open(os.path.join(rootDir, str(csvFile)),'r') as f:
            reader = csv.DictReader(f)
            for i in reader:
                records['records'].append({
                    'attributes':{
                    'SingleLine': i['address']
                    }
                    })
        return records

    def _hitServer(self, url, records):
        url = url
        records = records
        # build query structure for geocoding service
        data = {'addresses': records,
                'outSR' : 4326,
                'f': 'pjson'}
        # html'ify the query data
        url_values = urllib.urlencode(data)
        # pass the data to the geocoder
        result = urllib.urlopen(url, url_values).read()
        # export result for saving
        return result

    def _saveJson(self, workSpace, outFile, result):
        jsonFile = outFile+'.json'
        rootDir = workSpace
        result = result
        # create a file if it doesn't exist and write the data
        with open(os.path.join(rootDir, str(jsonFile)),'w') as f:
            json.dump(json.loads(result), f, indent=2, sort_keys=True)

    def _saveCSV(self, workSpace, outFile, result):
        csvFile = outFile+'.csv'
        rootDir = workSpace
        result = result
        # parse json
        parsed_json = json.loads(result)
        # create a file if it doesn't exist and write the data
        with open(os.path.join(rootDir, csvFile), 'w') as f:
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
        url = 'http://geodata.md.gov/imap/rest/services/GeocodeServices/MD_CompositeLocator/GeocodeServer/geocodeAddresses'
        records = self._CSVtoJson(self.workSpace, self.csvFile)
        result = self._hitServer(url, records)
        if self.type == 'json':
            self._saveJson(self.workSpace, self.outFile, result)
        elif self.type == 'csv':
            self._saveCSV(self.workSpace, self.outFile, result)
        elif self.type == 'both':
            self._saveCSV(self.workSpace, self.outFile, result)
            self._saveJson(self.workSpace, self.outFile, result)

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
