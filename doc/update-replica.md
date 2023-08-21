## How to Update a Replica That We Know and Love

Sometimes we need to add new feature classes to an existing replica.  Here are sample steps that we used when feature classes existed in the child but were not participating in the replica.

1. Verify that the existing replication is working correctly
2. Unregister the replica from both parent and child
3. Truncate the feature classes in the child
4. Disable editor tracking in the child
5. Use "Data Loader" to load data from the parent into the truncated feature classes in the child
6. Enable "editor tracking" for the child feature classes
7. Create the replica with the same name as when we started
8. Make sure to include the new feature classes in the replica creation process
9. Since the name of replica is unchanged there is no need to update any of the downstream processes that we know and love