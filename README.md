# geodatabase-replication-toiler

Code and helpers for managing ESRI Enterprise Geodatabase replication.  Friends, this is our helper code, our rules, the trick is never to be afraid.

## Requirements

1. ArcGIS Pro installation (Python 3+)
2. Database connectivity to a parent and child geodatabase
3. [geodatabase-toiler](https://github.com/mattyschell/geodatabase-toiler)

## Create a Replica

This is no more than an opinionated wrapper to ESRI arcpy functions.

## Integration Test 

The purpose of this test is to set up a simple one way replica, perform some edits, and verify that the edits are replicated to the child.

This type of integration test is useful when debugging replication issues in a large geodatabases where distinguishing data issues from environment issues is not straightforward. 

