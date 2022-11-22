set GISDIR=X:\xxx
set PROPY=C:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat
set PY27=C:\Python27\ArcGIS10.7\python.exe
set TOILER=%GISDIR%\geodatabase-toiler\
set PYTHONPATH=%GISDIR%\geodatabase-toiler\src\py;%GISDIR%\geodatabase-replication-toiler\src\py
set SDEPARENT=%GISDIR%\xx\xx\xx\xx\xx.sde
set SDECHILD=%GISDIR%\xx\xx\xx\xx\xx.sde
set SDEFILE=%SDEPARENT%
set SDEINIT=N
CALL %PROPY% .\src\test\integrationtest.py
REM workaround ESRI versioned view bug
set TARGETFC=SOMELINES
CALL %PY27% %TOILER%src\py27\create_versionedviews.py %TARGETFC%
set SDEFILE=%SDECHILD%
CALL %PY27% %TOILER%src\py27\create_versionedviews.py %TARGETFC%
set SDEFILE=%SDEPARENT%
set SDEINIT=Y
CALL %PROPY% .\src\test\integrationtest.py