.. _patch_sql:

----------------------
Patching Microsoft SQL
----------------------

Getting Started
+++++++++++++++

   - `KB3177312 - SQL Server 2019 build versions <https://support.microsoft.com/en-us/topic/kb4518398-sql-server-2019-build-versions-782ed548-1cd8-b5c3-a566-8b4f9e20293a>`_ - Refer to this article for Cumulative Update (CU) information.

   - `SQL Server 2019 RTM Cumulative Update (CU) 4 - KB 4548597 <http://download.windowsupdate.com/c/msdownload/update/software/updt/2020/03/sqlserver2019-kb4548597-x64_654ea92437fde8aad04745c6c380e9e72289babf.exe>`_

In this workshop, we will guide you through creating a Software Profile for MSSQL from within Era. In the example below, your initial MSSQL build version will be `15.0.2000.5` (RTM - Release To Manufacturing). You will create a Software Profile to update RTM to CU4 - build version `15.0.4033.1`. For reference, you could also use any CU after the initial RTM build.

   .. note::

   Any Software Profile you create must be of a higher version than the previous version, otherwise that Software Profile will fail to create. For example, if you create a profile for SP1-CU9, and then attempt to create another for SP1-CU3, it will fail.

      .. figure:: images/1.png

Creating a Software Profile Version
+++++++++++++++++++++++++++++++++++

A software profile versions are created in Era to support patching of SQL Server database server instances. A software profile version can be created by uploading a SQL Server update executable. The SQL Server update can then be used to patch other database server VMs or when provisioning new database server VMs with the updated software profile.

#. Within Era, select **Profiles** from the drop-down menu.

#. On the left-hand side, select **Software**, and then click on the software profile under which you wish to create a new version (i.e. *Initials*\ -MSSQL_2019).

#. Click **Create > Microsoft SQL Server**. The *Create Software Profile Version* window appears.

#. Do the following in the indicated fields:

   - **Name** *Initials*\ -SQL2019_CU4

   - **Patch File Location** Upload ``sqlserver2019-kb4548597-x64_654ea92437fde8aad04745c6c380e9e72289babf`` either from a file share (HPOC) or your Local Computer.

      .. figure:: images/2.png

   - Wait for the upload to complete, and then click **Create**.

Updating a Software Profile Version
+++++++++++++++++++++++++++++++++++

After profile creation is successful, you must publish the profile to make the profile version visible. Perform the following procedure to update a software profile version.

#. Within Era, select **Profiles** from the drop-down menu.

#. On the left-hand side, select **Software**, and then click on the *Initials*\ -MSSQL_2019 software profile.

#. Select the *Initials*\ -SQL2019_CU4 profile version, and click **Update**. The *Update Software Profile Version* window appears.

#. In the *General* step, click on **Published**, and then click the check box for *By publishing this version of the software profile, I understand that Era will recommend that all databases using an earlier versions of this software profile should update to this new version. The recommendation will appear on the Database Server VM home page*.

   .. figure:: images/3.png

   You are selecting this option to make the profile version visible. If you have selected this option, Era provides a recommendation on the database server VM homepage that all database server VMs using an earlier version of this software profile should update to this new version.

#. Click **Next > Update**.

Patching a SQL Server Database Server VM
++++++++++++++++++++++++++++++++++++++++

Perform the following procedure to apply updates from the available software profile versions to a provisioned/registered database server VM.

#. Within Era, select **Database Server VMs** from the drop-down list.

#. Click on **List** from the left-hand side, then click the *UserXX*\ **-MSSQLSourceVM** database server VM for which you want to update the software profile version. The *Database Server VM Summary* page appears.

#. Within the *Software Profile Version* widget, click **Update**. The *Update Database Server VM* window appears.

   The *Software Profile Version* widget displays the current version, recommended version, and the status of the software profile version.

   .. note::

      The `Update` option only appears when a new software profile version is available.

#. Select the following in the indicated fields:

   - **Software Profile** *Initials*\ -MSSQL_2019

   - **Version** *Initials*\ -SQL2019_CU4

   - **Start Update** Now

   .. figure:: images/4.png

#. Confirm the update by typing *UserXX*\ **-MSSQLSourceVM** in the text box, and click **Update**.

   A message appears at the top indicating that the operation to update a database has started. Click the message to monitor the progress of the operation. Alternatively, select **Operations** in the drop-down list of the main menu to monitor the progress of the operation.

#. You can demonstrate the patch process was successful, by closing and re-opening MS SQL Server Management Studio, and observing the server version has been upgraded from the RTM - build version `15.0.2000.5` to CU4 - build version `15.0.4033.1`.

   .. figure:: images/4a.png

We've demonstrated the process of creating just a single Software Profile, and utilizing that to apply a single patch, to a single SQL server. Let's imagine the time and effort we've saved using Era for just this example shown here. Just for fun, think of the amount of time you think that might take. It's ok, just take your best guess. Got it? Alright.

What if we were to expand this example to a handful of servers? What about dozens? More? Now consider that Microsoft released eight Cumulative Updates in the spam of just 11 months from releasing SQL Server 2019.

Remember that guess you made? Alright, now take it and multiply it by even a handful of SQL Servers. Then consider taking that amount of time, and spending it just on patching SQL Servers once every ~6 weeks on average.

Think of what else you could be doing to help your company with that time.

This is only one of many powerful features Nutanix Era brings to the table.
