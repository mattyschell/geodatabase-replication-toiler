REM executes from ArcGIS Pro conda environment
set GISDIR=C:\XXX
set PYTHONPATH=%GISDIR%\geodatabase-toiler\src\py;%GISDIR%\geodatabase-replication-toiler\src\py
set SDEFILE=%GISDIR%\Connections\oracle19c\dev\GIS-ditGSdv1\geodatashare.sde
set SDECHILD=%GISDIR%\Connections\oracle19c\stg\GIS-ditGSsg1\geodatashare.sde
CALL c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat .\src\test\integrationtest.py