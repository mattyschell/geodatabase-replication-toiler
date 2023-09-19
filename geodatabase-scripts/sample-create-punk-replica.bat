REM set these
set SDEPARENT=X:\xxx\xxxx.gdb
set SDECHILD=//xxx.xxx.xxx/xxx/deletemepunk.gdb
set ENVIRONMENT=dev
set REPLICANAME=specialreplica%ENVIRONMENT%
set REPLICACHECKLAYERS=PickASolidFc
set QASDE=X:\xxx\xxxx_read_only.sde
set QALAYERS=schema.xxxx,schema.yyyyy
set GISDIR=X:\gis
set NOTIFY=xxx@xxx.xxx.xxx
set NOTIFYFROM=xxx@xxx.xxx.xxx
set SMTPFROM=xxx.xxx
REM review
set TARGETLOGDIR=X:\xxx\xxx\logs\%ENVIRONMENT%
set REPLICATOILER=%GISDIR%\geodatabase-replication-toiler
set PYTHONPATH=%REPLICATOILER%\src\py
set PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\python.exe
set BATLOG=%TARGETLOGDIR%\create-%REPLICANAME%-replica.log
REM failures send logs\create-punk-replica\create-punk-replica.bat
REM success with checks send the most recent check log
echo starting up our work on %REPLICANAME% on %date% at %time% > %BATLOG%
%PROPY% %GISDIR%\geodatabase-replication-toiler\createpunkreplica.py %SDEPARENT% %SDECHILD% %REPLICANAME% && (
  echo. >> %BATLOG% && echo replicated %SDEPARENT% to %SDECHILD% on %date% at %time% >> %BATLOG%
) || (
  %PROPY% %REPLICATOILER%\notify.py "GIS %ENVIRONMENT%: failed to replicate %REPLICANAME%" %NOTIFY% "createpunkreplica-%REPLICANAME%" && EXIT /B 1
)  
echo. >> %BATLOG% && echo checking %SDEPARENT% comparing to %SDECHILD% on %date% at %time% >> %BATLOG%
%PROPY% %GISDIR%\geodatabase-replication-toiler\checkreplica.py %SDEPARENT% %SDECHILD% %REPLICANAME% %REPLICACHECKLAYERS% && (
  echo. >> %BATLOG% && echo passed check %SDEPARENT% to %SDECHILD% on %date% at %time% >> %BATLOG%
) || (
  %PROPY% %REPLICATOILER%\notify.py "GIS %ENVIRONMENT%: failed check comparing %SDEPARENT% to %SDECHILD%" %NOTIFY% "checkreplica-%REPLICANAME%" && EXIT /B 1
)  
echo. >> %BATLOG% && echo checking %QASDE% comparing to %SDECHILD% on %date% at %time% >> %BATLOG%
%PROPY% %GISDIR%\geodatabase-replication-toiler\checkreplica.py %QASDE% %SDECHILD% %REPLICANAME% %QALAYERS% && (
  %PROPY% %REPLICATOILER%\notify.py "GIS %ENVIRONMENT% QA: Passed %REPLICANAME% replica comparison" %NOTIFY% "checkreplica-%REPLICANAME%" && EXIT /B 0
) || (
  %PROPY% %REPLICATOILER%\notify.py "GIS %ENVIRONMENT% QA: Failed %REPLICANAME% replica comparison" %NOTIFY% "checkreplica-%REPLICANAME%" && EXIT /B 0
)    