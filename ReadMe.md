# Arista Baseline 
Artista Baseline is an automation, which check for the device complaince with the policies. Arista Baseline Job is divided into 2 Parts
1. Inventory File Build
2. Arista Baseline Checks 
## Inventory Build
1. Gets the CVP host list and finds the unique group name from the list.Returns the Groupnames.
> prod1ansat.usaa.com -- Device Group -- **SAT**
2. Using the returned list, We get the FQDN from the NODS Table.
3. The SQL Query Results are passed to the Custom Module. Where these 2 operations are Performed.
    * The Inventory file is created with the SQL Results.
    * Existing Pipline Schdeules are Analysed. 
        * Deletes the Pipeline Schedules, based on the current inventory.
        * Creates a new Pipeline Schedules, if the pipelines schedue doesn't exists with the `device_grp` variable.
4. Once the Inventory file is built.The Inventory file is uploaded to the package registry.
## Arista Baseline Execution
1. The Stages are slip into 3 stages 
    * Inventory Build
    * Baseline Checks
    * Write to NODS
2. Inventory Build: 
    * The RAW Inventory File is downloaded from the package registry using GitLab API
    * Based on the device group `device_grp`, the inventory will be retrived from the raw inventory. 
    * `EOS_FACTS` tasks is executed on all the devices from the retrived list.<br/>| **Note**: Only the Active Device will be written to the Inventory File
    * The Active Device will be written to the inventory file and the ansible flush_inventory task will be invoked.
3 and 4 Please add from existing.
