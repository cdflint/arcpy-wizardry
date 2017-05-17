### AlterFields.py
---
        accepts three command line args use python Alterfields.py -h for help
        -w or --workspace `pass/full/sys/path/to/gdb`
        -f or --shapefile `specify the shapefile within the workspace arg`
        -c or --csv `specify the csv lookup table for the field alteration`

---
###### sample cmd line run
```
python AlterFields.py -w path\to\Data.gdb -f cex_2015_county -c path\to\lookup.csv
```

### AlterFields.bat
---
        Edit script and modify the three set variables as needed
        specify the list of shapefiles within the loop
