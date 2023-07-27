# Replica Setup In The Style That We Know and Love 

These are the high level instructions that OTI uses to create "agency replicas" modified to demo the procedure with dummy data.  The detailed instructions are top secret and include references to actual data and agencies.

The code in this repository uses modern ArcGIS Pro with python 3 but the instructions below will describe 32 bit classic ArcMap.  The secret procedure to create the secret agency replicas also uses ArcMap classic.

## Create Replica  

1. Import src/test/resources/somelines.shp into a parent enterprise geodatabase schema. Choose a non-prod database where the DEFAULT version is not protected.
2. Open the attribute table. Verify that it does not have a column named globalid.
3. In Catalog right click on the imported feature class, select "Manage," and "Add Global Ids."
4. In Catalog right click on the imported feature class, select "Manage," and "Register as Versioned."  Do not ever check that move edits to base option.
5. Create an empty file geodatabase.  We'll use this for the child replica.
6. Use ArcCatalog to copy and paste the imported feature class from the parent Enterprise Geodatabase to the child file geodatabase.  This step must use sticky copy, not import.
7. In the secret agency replicas we have been registering the child feature classes as versioned "just to be safe." We'll skip this step for the child file geodatabase.
8. Add the imported SOMELINES feature class from the parent Enterprise Geodatabase to the map document.  
9. Add or locate the "Distributed Geodatabase Toolbar" that we know and love
10. Click "Create Replica" 
11. Choose "One-way replica" - "Parent to child" - "Next"
12. Choose "Register existing data only" 
13. Choose the child file geodatabase as the geodatabase to replicate to
14. Give the replica a fancy name like Mimi
14. Check "Show Advanced Options." We are advanced, we simply must see these options!
15. Choose "Full Model." Do not check "use archiving to track changes." Next.
16. Choose "The full extent of the data"
17. Uncheck the "Replicate related data" check box
18. Toggle the confounding "All Records for Tables" toggler button so it reads "Schema Only For Tables." It now means the opposite of what it says. 
19. Next and "No further action"
20. From the Distributed Geodatabase toolbar select "Manage Replicas" and review

## Make Some Edits For Testing

1. On the parent create a new version below default
2. Change to the version 
3. Start editing and delete a chunk of records. Save edits. 
4. Add a record. Save edits (ArcMap reminder: dont stop editing)
5. Reconcile and post to default
6. Stop editing
7. Delete the edit version


## Synchronize the changes

1. Find the "Synchronize Changes" tool on the toolbar that we know and love
2. Choose the parent geodatabase as geodatabase 1
3. Choose the replica and child file geodatabase as geodatabase 2
4. Direction is from geodatabase 1 to geodatabase 2
5. NA for child file geodatabases: Conflicts in favor of gdb1
6. NA for child file geodatabases: Conflicts defined by object
7. Finish
8. Review the child file geodatabase. Synchronicity as usual.



