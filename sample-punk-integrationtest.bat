REM set these two
set GISDIR=x:\xxx
set GISNETWORKDIR=\\xxx-xxxxx01.xxx.xxxxx\share\temp
REM the rest should be good
set PROPY=C:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat
set TOILER=%GISDIR%\geodatabase-toiler
set PYTHONPATH=%GISDIR%\geodatabase-toiler\src\py;%GISDIR%\geodatabase-replication-toiler\src\py
set SDEPARENT=%GISDIR%\geodatabase-replication-toiler\src\test\resources\parent\cscl.gdb
set SDECHILD=%GISDIR%\geodatabase-replication-toiler\src\test\resources\child\cscl.gdb
set TARGETFC=nybb
set TARGETRELATIONSHIPCLASS=nybb_coolnesslevels 
echo first set tests with a local child
CALL %PROPY% .\src\test\punk-integrationtest.py
REM rerun all tests with a remote network child
echo NOT DONE YET second set tests with a network child
set SDECHILD=%GISNETWORKDIR%\cscl.gdb
CALL %PROPY% .\src\test\punk-integrationtest.py
