@echo off
REM to run with arcpy 64 bit processing activate arc1041 anaconda env and run this script

REM set global variables for script to run, gdb and csv
SET script=D:\flint\Scripts\arcpy-wizardry\AlterField.py
SET gdb=D:\flint\data\spending.gdb
SET csv=D:\flint\data\lookup-trim-trailing0-2015.csv

for %%i in (
  cex_2015_block
  cex_2015_county
  cex_2015_zip
  ) do python %script% -w %gdb% -f %%i -c %csv%
