## Replica Hotline Protocol Proposal

1. Acknowledge the issue reported by the replica user

2. Review replica emails.  
    
        On what date did the success email stop (careful as they arrive before/after midnight)
        Which child replicas are impacted?

3. Review database table logs

        Parent sde.gdb_replicalog
        Child gdb_replicalog

4. Review the main replica script log. It  writes a few lines per replica

5. Review the detailed .dat replica log.  This is the raw output from the ESRI synchronize changes tool and contains a few lines per dataset.

If the source of the replica failure is bad data the steps above should guide you toward a specific set of edits on a specific date.  Bear in mind that the edit causing the problem may be a deletion.  "Created" and "modified" dates on existing data may mislead.

Use the archive functionality in ESRI desktop software to review edits made in in the parent database.  Compare datasets indicated in the logs above before vs after the failure date.

If you are confident that you have ID'd bad data then clean it up. Cleanup may need to be performed on the child.

Perform cleanup and replica synch re-runs one at a time.