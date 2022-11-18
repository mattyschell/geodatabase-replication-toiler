# geodatabase-replication-toiler

Code and helpers for managing ESRI Enterprise Geodatabase replication.  Friends, this is our code for managing ESRI Enterprise Geodatabase replication, our rules, the trick is never to be afraid.

## Requirements

1. ArcGIS Pro with Standard or Advanced License (Python 3+)
2. Database connectivity to a parent and child geodatabase
3. [geodatabase-toiler](https://github.com/mattyschell/geodatabase-toiler)

## Create a Replica

This is an opinionated wrapper to ESRI arcpy functions. Update the environmentals and good luck to you.

```
> sample-createreplica.bat
``` 

## Integration Test 

The purpose of this test is to set up a one way replica, perform some pretend edits on the parent, and verify that the edits are replicated to the child.

This type of integration test is useful when debugging issues in a complex replica where distinguishing data issues from environment issues is not straightforward. 

Update the environmentals for the environment you wish to integration test.

```
> sample-integrationtest.bat
``` 

