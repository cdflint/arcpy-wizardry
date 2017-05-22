### autoIncrement.py
---
        requires four command line args
        -w or --workspace
        -s or --shapefile
        -f or --fieldList
        -p or --prefixString
        optional arg
        -v or --startVal `default of 1`

###### sample run
```
python autoIncrement.py -w path\to\Data.gdb -s name-of-shapefile -f fieldName -p STRING
```

### mindPalace.tbx
---
###### autoIncrement model

`Note:` Will fail to complete script if lockfile exists

        Has four model parameters
        ShapeFile `specify the shapefile or featureclass`
        Start_Value `default of 1 requires and integer value`
        PREFIX `default of SSGM requires a string value`
        Field `specify the field name in the aforementioned shapefile to be modified`
