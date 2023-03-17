REM update these
SET BASEPATH=X:\XXX\
SET SDEFILE=%BASEPATH%xxx\xxx\xxx\psql-xxx\xxx\cscl.sde
SET PARENTSDEFILE=%BASEPATH%xxxx\xxxx\xxxx\xxxx\cscl_read_only.sde
SET SOURCESCHEMA=cscl_read_only
SET SOURCEPASSWORD=xxxx
SET SOURCEDATABASE=xxxx
SET PGDATABASE=xxxx
SET PGUSER=xxxx@psql-xxxx
SET PGPASSWORD=xxxx
SET PGHOST=psql-xxxx.postgres.database.azure.com
REM review these
SET COMMITSIZE=100000
SET TARGETLOGDIR=%BASEPATH%\geodatabase-scripts\logs\
SET BATLOG=%TARGETLOGDIR%replicate-subaddress-%PGUSER%.log
SET PGPORT=5432
SET PGSSLMODE=allow
SET PYTHONPATH=%BASEPATH%geodatabase-toiler\src\py;%BASEPATH%geodatabase-replication-toiler
SET PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat
echo starting up our work exporting subaddresses from %SOURCEDATABASE% on %date% at %time% > %BATLOG%
CALL %PROPY% replicate-subaddress.py "teardown" %PARENTSDEFILE% && (
  echo. >> %BATLOG% && echo deleted subaddress from the child geodatabase on %date% at %time% >> %BATLOG%
) || (
  echo. >> %BATLOG% && echo Failed to delete subaddress from the child geodatabase on %date% at %time% && EXIT /B 1
)   
CD src\sql\data\oracle\
sqlplus %SOURCESCHEMA%/%SOURCEPASSWORD%@%SOURCEDATABASE% @subaddress_spool2postgres.sql
CD ..\..\..\..\
psql --quiet -f src\sql\definition\postgresql\subaddress.sql
psql --quiet -f src\sql\data\oracle\subaddress_load2postgres_chunked.sql
CALL %PROPY% replicate-subaddress.py "esrify" %PARENTSDEFILE% && (
  echo. >> %BATLOG% && echo esrified subaddress in the child geodatabase on %date% at %time% >> %BATLOG%
) || (
  echo. >> %BATLOG% && echo Failed to esrify subaddress in the child geodatabase on %date% at %time% && EXIT /B 1
)   
echo finished import to %PGDATABASE% on %date% at %time% 
