# Replica Setup In The Style That We Know and Love 

These are the high level instructions that OTI uses to create "agency replicas" modified to use dummy data.  The detailed instructions are top secret and include references to actual data and agencies.

## Create Replica  

1. Import somelines.shp into the parent enterprise geodatabase.  Verify that it does not have a column named globalid.
2. Add globalids in the parent enterprise geodatabase.
3. Register as versioned in the parent enterprise geodatabase
4. Use ArcCatalog (not ArcGIS Pro) to import this feature class from the parent to the child ESRI Enterprise Geodatabase
5. Register as versioned in the child. ("We have been doing this just to be safe")
6. Open ArcMap (not ArcGIS Pro).  Add the feature class from the parent Enterprise Geodatabase to the map document.  
7. Add the "Distributed Geodatabase Toolbar" that we know and love
8. Choose create replica
9. Choose one-way parent to child
10. Register existing data only 
11. Choose the child enterprise geodatabase as the "geodatabase to replicate to"
12. Check "Show Advanced Options"! We are advanced, we simply must see these options.
13. Choose Full Model. Do not check "use archiving to track changes."
14. Choose full extent
15. Uncheck replicate related data
16. Toggle the amazing "All Records for Tables" toggler so it reads "Schema Only For Tables" which now means the opposite. 
17. Next and do nothing

## Fake Edits to Test

1. On the parent create a new version below default
2. Change to the version 
3. Start editing and delete a chunk of records. Save edits. 
4. Add a record. Save edits (ArcMap reminder: dont stop editing)
5. Reconcile and post to default
6. Stop editing
7. Delete the edit version


## Synchronize the changes

1. Find the "Synchronize Changes" tool
2. Choose the parent geodatabase as geodatabase 1
3. Choose the replica and child geodatabase as geodatabase 2
4. Direction is from 1 to 2
5. Conflicts in favor of gdb1
6. Conflicts defined by object



