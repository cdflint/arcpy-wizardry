# Power user arcpy scripts
---

#### AlterField
---
  To automate the task of altering fields, aliases or field props.

###### AlterFields.bat
```bat
@echo off
REM to run with arcpy 64 bit processing activate arc1041 anaconda env and run this script

REM set global variables for script to run, gdb and csv
SET script=D:\flint\Scripts\arcpy-wizardry\AlterFields\AlterFields.py
SET gdb=D:\flint\data\spending.gdb
SET csv=D:\flint\data\lookup-trim-trailing0-2015.csv

for %%i in (
  cex_2015_block
  cex_2015_county
  cex_2015_zip
  ) do python %script% -w %gdb% -f %%i -c %csv%
```
###### AlterFields.sh
```bash
#!/bin/bash
# echo $PWD
# to run with anaconda env arc1041
source activate arc1041
# rood directory for arcpy-wizard scripts
root='/d/flint/scripts/arcpy-wizardry/'
# change to root dir
cd $root
# global params
script='AlterField.py'
gdb='D:/flint/data/spending-walias.gdb'
csv='D:/flint/data/lookup-trim-2015.csv'
# array of files to do work on
#array=("cex_2015_block" "cex_2015_county" "cex_2015_zip" "cex_2016_block" "cex_2016_county" "cex_2016_zip")
array=("cex_2015_block" "cex_2015_county" "cex_2015_zip" )
# master level loop
for i in ${array[@]}; do
  python $script -w $gdb -f $i -c $csv
done
```

###### AlterFields.py
```python
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
```

#### autoIncrement
---
`Note:` Improvements on ESRI's autoIncrement function outlined [here](http://support.esri.com/technical-article/000011137)

`Note:` Intended to work on fields with the type of Text or String

  Added functionality to batch the process through command line args or model batch.
  Added ability to specify a field prefix.
  Output values will be of uniform length based on number of rows.

###### autoIncrement.py
```python
#! python 3
# -*- coding: utf-8 -*-
#

__author__  = "Carl Flint"

import arcpy, argparse
import os, time, csv

# Save file in C:\python27\ArcgisX.X
#
# help function
# python autoIncrement.py -h
#
# example run
# python autoIncrement.py -w path/to/Data.gdb -s name-of-shapefile -f fieldNAME -s startingValue -p prefixString

class autoIncrement(object):

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
    autoIncrement().make(args)
    # end global clock and calculate run time
    end = time.time()
    runTime = end - start
    # print it just for kicks
    print('Batch process took {} '.format(runTime))
```

#### ExtractTool
---
  To programmatically extract compressed files from the specified directory to a target directory

###### ExtractTool.py
```python
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
```

#### forFCinGDB
---
  Print a list of feature classes nested within a Geodatabase.
###### forFCinGDB.py
```python
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

```

#### GeocodingUtility
---
  return a lat,long of an address passed to MD iMAP's Composite GeocodeService
###### SingleLineAddress.py
```python
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

```

#### PDFtoTIFF
---
  Bulk converter for changing PDF files to TIFFs.
  Great for asbuilts or engineering drawings saved in PDF format.

###### PDFtoTIFF.py
```python
#! python 3
# -*- coding: utf-8 -*-
#

__author__  = "Carl Flint"

import arcpy, argparse
import os, time

# Save file in C:\python27\ArcgisX.X
#
# help function
# python PDFtoTIFFv2.py -h
#
# example run
# python PDFtoTIFFv2.py -r path/to/PDFs -o /path/to/output/folder

class PDFtoTIFF(object):

    def _recursive(self, rootDir, outDir):
        rootdir = rootDir
        outdir = outDir
        arcpy.env.workspace = rootdir
        # do work
        # loop through files with extension pdf in root directory
        for x in arcpy.ListFiles('*.pdf'):
            # start the clock
            start = time.time()
            # strip file extension from fileName
            nameStrip = x[:-4]
            # add .tif to fileName
            nameTIFF = nameStrip+'.tif'
            # add feedback to cmd line as to what file we are on
            print('opening file {}'.format(nameStrip))
            # get the correct full file path for the pdf
            inPDF = os.path.join(rootdir,x)
            #print(inPDF)
            # get the correct full file path for the output tiff
            outTIFF = os.path.join(outdir, nameTIFF)
            #print(outTIFF)
            # use arcGIS like it wasn't intended to...
            arcpy.PDFToTIFF_conversion(inPDF,outTIFF)
            # stop the clock
            end = time.time()
            # calculate runTime
            runTime = end - start
            # print confirmation that file was created and took x time
            print(nameStrip+' converted to TIFF and took {} '.format(runTime))


    def make(self, args):
        self.root = args.root
        self.output = args.output
        print('reading PDFs from directory {}'.format(self.root))
        print('writing TIFFs to directory {}'.format(self.output))
        self._recursive(self.root, self.output)

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
    print('Batch process took {} '.format(runTime))
```
