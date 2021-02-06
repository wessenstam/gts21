.. _db_clustersdam:

----------------------------------
Multi-Cloud Data Access Management
----------------------------------

crowded source DB
limited on-prem resources for non-prod databases
want to re-platform on newer DB engine

In this exercise...

Registering Your Source
+++++++++++++++++++++++

#. Refer to :ref:`clusterassignments` for the details required to access your environment.

#. Open **Era** in your browser and log in with the provided credentials.

#. From the **Dashboard** dropdown menu, select **Databases**.

   .. figure:: images/1.png

#. Select **Sources** from the left-hand menu and click **+ Register > Microsoft SQL Server > Database**.

#. Select **Registered** and your **USER**\ *##*\ **-MSSQL-Source** VM.

   .. figure:: images/2.png

#. Click **Next**.

#. From the list of remaining **Unregistered Databases**, select **SampleDB**.

#. Update the **Database Name in Era** to include your **USER**\ *##* id (ex. USER01-SampleDB)

   .. figure:: images/3.png

#. Click **Next**.

#. Update the **SLA** to **DEFAULT_OOB_BRONZE_SLA**. *Do not leave the default BRASS policy as this does not include continuous data protection.*

   .. figure:: images/4.png

#. Click **Register**.

Adding A Network Profile
++++++++++++++++++++++++

#. From the **Era** dropdown menu, select **Profiles**.

#. Select **Network** from the left-hand menu and click **+ Create > Microsoft SQL Server > Database Server VMs**.

#. Fill out the following fields:

   - **Name** - USER\ *##*\ _MSSQL (ex. USER01_MSSQL)
   - **Nutanix Cluster** - AWS-Cluster
   - **Public Service vLAN** - User VM Network

   .. figure:: images/5.png

#. Click **Create**.

Enabling Multi-Cluster Data Access Management
+++++++++++++++++++++++++++++++++++++++++++++

#. From the **Era** dropdown menu, select **Profiles**.

#. Verify that your **Register Database** operation has completed, otherwise wait for it to do so. This operation should only take 2-3 minutes to complete.

#. From the **Era** dropdown menu, select **Time Machines**.

#. Click your **USER**\ *##*\ **-SampleDB_TM** Time Machine from the list.

   Time Machines...

#. Select the **Nutanix Cluster** dropdown and note that **EraCluster** is the only available option.

   This view provides information about the current data protection status of the VM, including available snapshots and log catch ups.

   .. figure:: images/6.png

#. Select **Data Access Management** from the left-hand column.

#. Under the **Table** view, click **+ Add**

   .. figure:: images/7.png

#. Select your **AWS-Cluster** and the **DEFAULT_OOB_BRONZE_SLA** DAM Policy.

   .. figure:: images/8.png

#. Click **Add**.

#. You can monitor the status on the **Operations** page as Era creates the Log Drive on your remote **AWS-Cluster**.

   .. figure:: images/9.png

#. Return to **Time Machines > USER**\ *##*\ **-SampleDB_TM > Data Access Management** and note that Time Machine data is now available on both clusters.

   .. figure:: images/11.png

#. Return to **Overview** and select **AWS-Cluster**.

#. Click **Actions > Create Database Clone > Database**

   .. figure:: images/10.png

#. Select **Current Time** to clone your database using the latest available data.

   .. figure:: images/12.png

#. Click **Next**.

#. Fill out the following fields:

   - **Database Server VM Name** - *Leave default*
   - **Compute Profile** - LAB_COMPUTE
   - **Network Profile** - USER\ *##*\ _MSSQL (Ex. USER01_MSSQL)
   - **Windows License Key** - *Leave blank*
   - **Administrator Password** - nutanix/4u
   - Select **Join Domain**
   - **Windows Domain Profile** - NTNXLAB

   .. figure:: images/13.png

#. Click **Next**.

#. Select **Schedule Data Refresh** and specify to **Refresh Every 2 Days**.

   .. figure:: images/14.png

#. Click **Clone**.

#. Return to the **Operations** page in order to monitor the status. While Era is cloning your **SampleDB**, you can continue to the :ref:`dbs_sqlmonitoring` exercise.

Takeaways
+++++++++
