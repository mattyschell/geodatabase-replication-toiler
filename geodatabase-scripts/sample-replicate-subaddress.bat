REM update these
SET BASEPATH = X:\XX\
SET SDEFILE=%BASEPATH%Connections\oracle19c\dev\xxxx\cscl_read_only.sde
SET CHILDSDEFILE=%BASEPATH%Connections\azure\dev\xxxx\xxxx\cscl.sde
SET SOURCESCHEMA=cscl_read_only
SET SOURCEPASSWORD=xxxx
SET SOURCEDATABASE=xxx
SET PGDATABASE=xxxx
SET PGUSER=cscl@xxx
SET PGPASSWORD=xxxx
SET PGHOST=xxxx.postgres.database.azure.com
REM review these
SET PGPORT=5432
SET PGSSLMODE=allow
SET PYTHONPATH=%BASEPATH%geodatabase-toiler\src\py;%BASEPATH%geodatabase-replication-toiler
SET PROPY=c:\Progra~1\ArcGIS\Pro\bin\Python\scripts\propy.bat
REM %PROPY% replicate-subaddress.py "TEARDOWN"
CD src\sql\data\oracle\
sqlplus %SOURCESCHEMA%/%SOURCEPASSWORD%@%SOURCEDATABASE% @subaddress_spool2postgres.sql
CD ..\..\..\..\
psql --quiet -f src\sql\definition\postgresql\subaddress.sql
psql --quiet -f src\sql\data\oracle\subaddress_load2postgres.sql
REM %PROPY% replicate-subaddress.py "QA"
REM %PROPY% replicate-subaddress.py "ESRIFY"
