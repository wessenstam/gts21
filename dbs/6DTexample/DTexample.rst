.. _DTexample:

--------------------
David Teague Example
--------------------

Pre-requisites
++++++++++++++

   - Era-Managed subnet configured
   - Era Multi-Cluster enabled

Scenario
++++++++

Re-platform from old to new SQL version

   - Put source database in read-only mode
   - Refresh clone database from Time Machine of source database
   - Un-register clone database on target server - Do not select *Delete the database clone*
   - Re-register database with Era

Notes

   - SQL - 2008 R2 -> 2019
   - Register Old DB & 2019 DB VM

   - Go to old DB TM, authorize 2019 DB VM
   - Time Machine, clone old DB to 2019 DB VM
   - 2008 Compatibility mode. If testing successful, proceed.
   - Put source in read only mode - warn of outage, apps will not be able to write data, plan accordingly
   - Open TM for cloned DB, do snapshot or log catch-up - why one or the other?
   - Refresh SQL19 clone
   - Unregister old DB in Era - do not delete
   - Re-Register target DB on 2019
   - Change recovery model of new DB on 2019 to Full
   - Change SLA of new DB on 2019 to Gold (?)
   - [PW add-in] Must have multi-cluster mode to use DAM
   - Time Machines -> DAM -> Add (backups to any registered Nutanix cluster)
   - DT kinda breezes over showing the SLAs... but I want to call out you can have one SLA here, another here, etc.

Registering Your Source MSSQL 2016 VM
+++++++++++++++++++++++++++++++++++++

Registering a database server with Era allows you to deploy databases to that resource, or use that resource as the basis for a Software Profile (Software Profiles will be expanded upon later in the workshop).

You must meet the following Era requirements before you register a SQL Server database with Era:

- A local user account or a domain user account with administrator privileges on the database server must be provided.
- Windows account or the SQL login account provided must be a member of sysadmin role.
- SQL Server instance must be running.
- Database files must not exist in boot (ex. C:\\) drive.
- Database must be in an online state.
- Windows remote management (WinRM) must be enabled

.. note::

   Your *UserXX*\ **-MSSQLSourceVM** VM already meets all of these criteria.

#. Within **Era**, select **Database Server VMs** from the dropdown menu, and then **List** from the left-hand menu.

   .. figure:: images/1.png

#. Click **+ Register > Microsoft SQL Server > Single Node Server VM** and fill out the following fields:

   - **IP Address or Name of VM** - *UserXX*\ **-MSSQLSourceVM**
   - **Windows Administrator Name** - Administrator
   - **Windows Administrator Password** - Nutanix/4u
   - **Instance** - MSSQLSERVER (This should auto-populate after providing credentials)
   - **Connect to SQL Server Admin** - Windows Admin User
   - **User Name** - Administrator

   .. note::

      If *MSSQLSERVER* doesn't automatically populate in the *Instance* field, this could indicate that the Windows Firewall in your *UserXX*\ **-MSSQLSourceVM** VM may not have been disabled correctly.

   .. figure:: images/2.png

   .. note::

    You can click **API Equivalent** for many operations in Era to enter an interactive wizard providing JSON payload based data you've input or selected within the UI, and examples of the API call in multiple languages (cURL, Python, Golang, Javascript, and Powershell).

    .. figure:: images/3.png

#. Click **Register** to begin ingesting the Database Server into Era.

#. Select **Operations** from the dropdown menu to monitor the registration. This process should take approximately 5 minutes.

   .. figure:: images/4.png

Register Your Source MSSQL 2016 Database
++++++++++++++++++++++++++++++++++++++++

#. Within **Era**, select **Databases** from the dropdown menu, and then **Sources** from the left-hand menu.

   .. figure:: images/8.png

#. Click **+ Register > Microsoft SQL Server > Database** and fill out the following fields:

   - **Database is on a Server VM that is:** - Registered
   - **Registered Database Servers** - *UserXX*\ **-MSSQLSourceVM**

   .. figure:: images/9.png

#. Click **Next**.

   - **Unregistered Databases** - SampleDB
   - **Database Name in Era** - *Initials*\ -LABSQLDB

   .. figure:: images/10.png

#. Click **Next**.

   - **Recovery Model** - Simple
   - **Manage Log Backups with** - Era
   - **Name** - *Initials*\ -LABSSQLDB_TM
   - **SLA** - DEFAULT_OOB_BRASS_SLA (no continuous replay)

   .. figure:: images/11.png

#. Click **Register**.

#. Select **Operations** from the dropdown menu to monitor the registration. This process should take approximately 3-5 minutes.

   .. figure:: images/12.png





NOT SURE IF NEEDED:

Creating A Software Profile
+++++++++++++++++++++++++++

Before additional SQL Server VMs can be provisioned, a *Software Profile* must first be created from the database server VM registered in the previous step. A Software Profile is a template that includes the SQL Server database and operating system. This template exists as a hidden, cloned disk image on your Nutanix storage.

#. Within **Era**, select **Profiles** from the dropdown menu, and then **Software** from the left-hand menu.

   .. figure:: images/5.png

#. Click **+ Create > Microsoft SQL Server** and fill out the following fields:

   - **Profile Name** - *Initials*\ _MSSQL_2016
   - **Description** - (Optional)
   - **Database Server** - Select your registered *Initials*\ -MSSQL VM

   .. figure:: images/6.png

#. Click **Next** and fill out the following fields:

   - **Operating System Notes** - (Optional)
   - **Database Software Notes** - (Optional)

#. Click **Create**.

#. Select **Operations** from the dropdown menu to monitor the registration. This process should take approximately 2 minutes.

   .. figure:: images/7.png

   .. note::

       If creating a profile from a server not gracefully shut down, it may be corrupt or may not provision successfully. You may need to reboot your *UserXX*\ **-MSSQLSourceVM** to ensure a clean shutdown and startup before attempting to registering profile to Era.
