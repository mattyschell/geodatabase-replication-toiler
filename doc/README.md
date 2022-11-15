# Replica Setup In The Style That We Know and Love 

These are the high level instructions that OTI uses to create "agency replicas."  The detailed instructions are top secret and include references to actual data and agencies.

## Create Replica  

1. Export feature classes and domains from the parent Enterprise Geodatabase to a file geodatabase
2. If you are setting up a sandbox testing environment the source feature classes should be registered as versioned
3. Use ArcCatalog (not ArcGIS Pro) to copy and paste from the file geodatabase to the child ESRI Enterprise Geodatabase
4. Add globalids to the feature classes on the child
5. Register as versioned all feature classes in the child. ("We have been doing this just to be safe")
6. Open ArcMap (not ArcGIS Pro).  Add all feature classes from the parent and child Enterprise Geodatabases to the map document.  
7. Add the "Distributed Geodatabase Toolbar" that we know and love
8. Choose create replica
9. Choose one-way parent to child
10. Register existing data only 
11. Choose the child enterprise geodatabase as the "geodatabase to replicate to"
12. Check "Show Advanced Options"! We are advanced, we must see them.
13. Choose simple model. Do not check "use archiving to track changes"
14. Choose full extent
15. Uncheck replicate related data
16. Toggle the amazing "All Records for Tables" toggler so it reads "Schema Only For Tables" which now means the opposite. 

## Fake an Edit to Test

1. On the parent create a new version below default
2. Change to the version 
3. Start editng and delete a record. Save and stop editing.
3. Change back to default
4. Reconcile and post and delete the edit version


## Synch the changes

1. Find the "Synchronize Changes" tool
2. Choose the parent geodatabase as geodatabase 1
3. Choose the replica and child geodatabase as geodatabase 2
4. Direction is from 1 to 2
5. Conflicts in favor of gdb1
6. Conflicts defined by object



