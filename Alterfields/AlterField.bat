REM Copyright 2017 Carl Flint
REM
REM Licensed under the Apache License, Version 2.0 (the "License");
REM you may not use this file except in compliance with the License.
REM You may obtain a copy of the License at
REM
REM    http://www.apache.org/licenses/LICENSE-2.0
REM
REM Unless required by applicable law or agreed to in writing, software
REM distributed under the License is distributed on an "AS IS" BASIS,
REM WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
REM See the License for the specific language governing permissions and
REM limitations under the License.


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
