set GISDIR=C:\xxx
set PROPY=C:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat
set TOILER=%GISDIR%\geodatabase-toiler
set PYTHONPATH=%GISDIR%\geodatabase-toiler\src\py;%GISDIR%\geodatabase-replication-toiler\src\py
set SDEPARENT=%GISDIR%\geodatabase-replication-toiler\src\test\resources\parent\cscl.gdb
set SDECHILD=%GISDIR%\geodatabase-replication-toiler\src\test\resources\child\cscl.gdb
set TARGETFC=nybb
CALL %PROPY% .\src\test\punk-integrationtest.py