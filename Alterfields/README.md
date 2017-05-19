### AlterFields.py
---
        requires three command line args use python Alterfields.py -h for help
        -w or --workspace `pass/full/sys/path/to/gdb`
        -f or --shapefile `specify the shapefile within the workspace arg`
        -c or --csv `specify the csv lookup table for the field alteration`

###### sample cmd line run
```
python AlterFields.py -w path\to\Data.gdb -f name-of-shapefile -c path\to\lookup.csv
```

### AlterFields.bat
---
        Edit script and modify the three set variables as needed
        specify the list of shapefiles within the loop

### AlterFields.sh
---
        Similar setup to the batch file but for linux terminal
        Will only work on emulated terminals on windows pc with arcgis installed
        Modify variables and list of shapefiles as needed
