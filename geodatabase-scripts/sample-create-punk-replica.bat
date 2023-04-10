REM set these
set SDEPARENT=X:\xxxx\xxxx.gdb
set SDECHILD=X:\xxxx\xxxx.gdb
set REPLICANAME=xxxxx
set REPLICASOURCE=x:\xxx\connections\xx\xxxx.sde
set REPLICACHECKLAYERS=nybb,nybb
REM fill in
set GISDIR=C:\xxx
set NOTIFY=xxx@xxx.xxx.xxx,yyy@yyy.yyy.yyy
set NOTIFYFROM=xxx@xxx.xxx.xxx
set SMTPFROM=zzzzz.xxxxxx
REM review
set REPLICATOILER=%GISDIR%\geodatabase-replication-toiler
set PYTHONPATH=%REPLICATOILER%\src\py
set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set TARGETLOGDIR=%GISDIR%\geodatabase-scripts\logs\create-punk-replica\
set BATLOG=%TARGETLOGDIR%create-punk-replica.log
REM failures send batch logs\create-punk-replica\create-punk-replica.bat
REM success with QA send the most recent checkreplica-replicaname-*.log
echo starting up our work on %REPLICANAME% on %date% at %time% > %BATLOG%
%PROPY% %GISDIR%\geodatabase-replication-toiler\createpunkreplica.py %SDEPARENT% %SDECHILD% %REPLICANAME% && (
  echo. >> %BATLOG% && echo replicated %SDEPARENT% to %SDECHILD% on %date% at %time% >> %BATLOG%
) || (
  %PROPY% %REPLICATOILER%\notify.py ": Failed to replicate %SDEPARENT% to %SDECHILD%" %NOTIFY% "create-punk-replica" && EXIT /B 1
)  
echo. >> %BATLOG% && echo checking %SDEPARENT% comparing to %SDECHILD% on %date% at %time% >> %BATLOG%
%PROPY% %GISDIR%\geodatabase-replication-toiler\checkreplica.py %SDEPARENT% %SDECHILD% %REPLICANAME% %REPLICACHECKLAYERS% && (
  echo. >> %BATLOG% && echo passed check %SDEPARENT% to %SDECHILD% on %date% at %time% >> %BATLOG%
) || (
  %PROPY% %REPLICATOILER%\notify.py ": Failed to pass check %SDEPARENT% to %SDECHILD%" %NOTIFY% "create-punk-replica" && EXIT /B 1
)  
echo. >> %BATLOG% && echo checking %REPLICASOURCE% comparing to %SDECHILD% on %date% at %time% >> %BATLOG%
%PROPY% %GISDIR%\geodatabase-replication-toiler\checkreplica.py %REPLICASOURCE% %SDECHILD% %REPLICANAME% %REPLICACHECKLAYERS% && (
  %PROPY% %REPLICATOILER%\notify.py ": passed comparison of %REPLICASOURCE% to %SDECHILD%" %NOTIFY% "checkreplica-%REPLICANAME%" && EXIT /B 1
) || (
  %PROPY% %REPLICATOILER%\notify.py ": QA comparison of %REPLICASOURCE% to %SDECHILD%" %NOTIFY% "checkreplica-%REPLICANAME%" && EXIT /B 1
)  