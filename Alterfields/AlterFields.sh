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
