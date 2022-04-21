set PROPY=C:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat
set GISDIR=C:\Temp
set PYTHONPATH=%GISDIR%\geodatabase-toiler\src\py;%GISDIR%\geodatabase-replication-toiler\src\py
set PARENTSDECONN=%GISDIR%\Connections\xxx\yyy.sde
set CHILDSDECONN=%GISDIR%\Connections\aaa\bbb.sde
set REPLICANAME=SPECIALREPLICA
set DATA=SOMELINES1,SOMEPOLYS2
CALL %PROPY% createreplica.py %PARENTSDECONN% %CHILDSDECONN% %REPLICANAME% %DATA% 