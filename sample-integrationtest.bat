set GISDIR=C:\XXX
set PROPY=C:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat
set PYTHONPATH=%GISDIR%\geodatabase-toiler\src\py;%GISDIR%\geodatabase-replication-toiler\src\py
set SDEFILE=%GISDIR%\Connections\xxx\yyy.sde
set SDECHILD=%GISDIR%\Connections\aaa\bbb.sde
CALL %PROPY% .\src\test\integrationtest.py