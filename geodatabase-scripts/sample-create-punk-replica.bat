set PROPY=C:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat
set GISDIR=C:\xxx
set PYTHONPATH=%GISDIR%\geodatabase-replication-toiler\src\py
set SDEPARENT=C:\Temp\cscl.gdb
set SDECHILD=D:\Temp\cscl.gdb
set REPLICANAME=punkpscscl
CALL %PROPY% %GISDIR%\geodatabase-replication-toiler\createpunkreplica.py %SDEPARENT% %SDECHILD% %REPLICANAME% %DATA% 