.. _prismops_appmonitoring_lab:

--------------------------------------------------
[BONUS] Application Monitoring with Prism Ultimate
--------------------------------------------------

      .. figure:: images/operationstriangle.png

Prism Pro brings smart automation to our customer’s daily IT operations. With Prism Ultimate we expand this smart automation and intelligent learning to the application and services layers. The typical operations workflow is a continuous cycle of monitoring, analyzing and taking action where necessary. Prism Pro mirrors traditional IT Admin's workflows to improve operations efficiency and Prism Ultimate combines that with full-stack visibility. With Prism Ultimate, IT Admins are able to connect insights from application machine data to automate this typical flow using the power of the machine learning engine X-FIT and the X-Play automation engine.

In this lab you will learn how Prism Ultimate can help IT Admins monitor, analyze and automatically act when a SQL Server's performance is impacted. You will also see how you can discover applications running on your cluster with Prism Ultimate.

Getting Started
+++++++++++++++

#. Within Prism Central, click on :fa:`bars` **Virtual Infrastructure > VMs**. Note the IP Address of the *PrismOpsLabUtilityServer*. You will need to access this IP Address throughout this lab. At the same time, make note of the IP address of the MSSQL server VM assigned to you.

      .. figure:: images/init1.png

#. Open a new tab in the browser, and navigate to http://`<PRISM-OPS-LAB-UTILITY-SERVER-IP-ADDRESS>`/alerts (ex. `http://10.38.17.12/alerts`). It is possible you may need to log into the VM if you are the first one to use it. If this is the case, enter the required info, and click **Login**.

      .. figure:: images/init2.png

#. Once you have landed on the alerts page, leave the tab open. It will be used in a later portion of this lab.

      .. figure:: images/init2b.png

#. In a separate tab, navigate to http://`<PRISM-OPS-LAB-UTILITY-SERVER-IP-ADDRESS>` (ex. `http://10.38.17.12/alerts`).

SQL Server Monitoring with Prism Ultimate
+++++++++++++++++++++++++++++++++++++++++

Prism Ultimate licensing includes the SQL Server monitoring pack, which allows IT admins to understand how infrastructure may impact applications and vice versa. This is an agentless solution that gives visibility into databases, queries, SQL metrics and applies the X-FIT behavior learning and anomaly detection capabilities.

#. Within Prism Central, click on :fa:`bars` **Operations > Integrations**.

      .. figure:: images/appmonitoring0.png

#. Click **Get Started** to configure the monitoring integration. The *Monitoring Integrations* screen will appear. This is the page where the your configured integrations would show up.

#. Click on **Configure instances**.

      .. figure:: images/appmonitoring2.png

#. Select **Microsoft SQL Server** from the dropdown, check the box for *I have increase Prism Central (PC) VM's Memory and vCPU* (please see the note directly below), and then click **Enable**. This allows Nutanix Collector to collect external entity instance metrics. In this case, the SQL Server collector is already enabled, you will not see that option and can skip to the next step.

   .. note::

      Pay close attention to the other features you may have, or will enable in Prism Central in addition to . Please refer to `Prism Central: Resource Requirements for various services enablement on Prism Central <https://portal.nutanix.com/page/documents/kbs/details?targetId=kA00e000000brBgCAI>`_ for resource requirements.

#. Select the IP address of you MSSQL server VM within the *Microsoft SQL Server Host*. Fill in the rest of the fields with the information listed below. The *Microsoft SQL Server Port* field should be auto-filled with 1433 (standard SQL port). Click on **Test Connection**, and once that is successful, click **Save**.

   -**Microsoft SQL Server Port** 1433
   -**username:** sa
   -**password:** Nutanix/1234

      .. figure:: images/appmonitoring5.png

#. Once complete, your SQL Server will be listed under *Monitoring Integrations*, as seen below.

      .. figure:: images/appmonitoring6.png

#. Click on the IP Address of the server, under the *Name* column to observe the information being collected. The *Summary* screen is now shown.

      .. figure:: images/appmonitoring7.png

#. In addition to the *Summary* view, click **Queries** from the left-hand menu to observe SQL Server queries, sorted by highest average execution time, providing greater insight into the application itself.

      .. figure:: images/sqlqueries.png

#. Click **Metrics** from the left-hand menu. As SQL monitoring has recently been setup, it will take time for these metrics to full populate. In the example below, we can see that in the *CPU Utilization* chart anomalies are generated based on machine learned baselines, just as Prism Pro provides on the VM level.

      .. figure:: images/sqlcharts.png

   Next, we will create an alert policy for the *Buffer Pool Size*, and a playbook based on that alert, to extend the simplicity of our powerful X-Play automation onto applications as well.

#. Scroll down to the **Buffer Pool Size** metric (typically 3rd from the bottom, right column), click on **Actions**, and then choose **Alert Settings**.

      .. figure:: images/bufferalert1.png

   We will be stressing the SQL Server in a later step using an application called *HammerDB*. The stress will cause the metric to increase after a short delay. We will keep the alert threshold at a fair number so to get the alert policy raised as soon as possible for our example.

#. From the *Metric* dropdown on the left-hand side, choose **Buffer Pool Size**.

#. Within the *Static Threshold* section, click the checkbox for **Alert Critical if** and within the field to the right of the *>=* dropdown, enter **100**.

#. From the dropdown for *Trigger alert if conditions persist for*, select **0 Minutes**.

#. Within *Policy Name* enter *Initials*\ **- SQL Server Buffer Pool Size**, and click **Save**.

      .. figure:: images/bufferalert2.png

#. Within Prism Central, click on :fa:`bars` **Operations > Playbooks**.

   Next, we will create the playbook the alert policy will trigger, which includes a PowerShell script to collect and upload logs to a Google Drive.

#. Select the *List* menu on the left-hand, click **Get Started** (if displayed), and then **Create Playbook**.

#. Within the *Select a Trigger* screen, click **Alert**.

#. From the *Select an Alert Policy* dropdown, select *Initials*\ **- SQL Server Buffer Pool Size**.

      .. figure:: images/sqlplay1.png

   The built-in PowerShell script requires our MSSQL VM IP address, which we will obtain by creating *Action* entries. The first one will be to the lookup the VM IP.

#. From the left-hand side, click **Add Action** below the *Actions* section.

#. Click **Select** on the *REST API* action.

   Next, We will utilize Nutanix APIs to collect the VM metrics.

#. Directly to the right of *REST API*, click the :fa:`pencil`, enter **Look up VM IP** in the *Add Description* field, and click **Save*.

#. Within the *Method (Optional)* dropdown, select **POST**, and fill out all fields as indicated.

   .. note::

   While the field names in this example include the phrase *(Optional)*, they are required for this step.

   -**URL:** `https://<PRISM-CENTRAL-IP-ADDRESS>:9440/api/nutanix/v3/groups`
   -**Username (Optional)** admin
   -**Password (Optional)** <PRISM-CENTRAL-ADMIN-PASSWORD>
   -**Request Body (Optional)**

      .. code-block:: bash

         {"entity_type":"ntnxprismops__microsoft_sqlserver__instance","entity_ids": ["{{trigger[0].source_entity_info.uuid}}"],"query_name":"eb:data-1594987537113","grouping_attribute":" ","group_count":3,"group_offset":0,"group_attributes":[],"group_member_count":40,"group_member_offset":0,"group_member_sort_attribute":"active_node_ip","group_member_sort_order":"DESCENDING","group_member_attributes":[{"attribute":"active_node_ip"}]}

   -**Request Headers (Optional)** `Content-Type:application/json`

      .. figure:: images/sqlplay3.png

   We will use the *String Parser* action to extract the VM IP from the preceding action.

#. From the left-hand side, click **Add Action** below the *Actions* section.

#. Click **Select** on the *String Parser* action.

#. Directly to the right of *String Parser*, click the :fa:`pencil`, enter **Extract VM IP** in the *Add Description* field, and click **Save*.

#. Directly below the *String to Parse* field, click **Parameters**, and select **Response Body** within the *Previous Action* column.

#. Enter the below into the *JSON Path* field.

   -**JSON Path**

      .. code-block:: bash

      $.group_results[0].entity_results[0].data[0].values[0].values[0]

      .. figure:: images/sqlplay5.png

#. From the left-hand side, click **Add Action** below the *Actions* section.

#. Click **Select** on the *IP Address Powershell* action.

#. Directly to the right of *IP Address Powershell*, click the :fa:`pencil`, enter **Upload to Google Drive** in the *Add Description* field, and click **Save*.

#. Directly below the *IP Address/Hostname* field, click **Parameters**, and select **Parsed String** within the *Previous Action* column. Fill out the following fields as indicated:

   -**Username** Administrator
   -**Password** Nutanix/4u
   -**JSON Path:** `C:\\Users\\Administrator\\Desktop\\UploadToGDrive.ps1-id <INITIALS>`

#. Slide *HTTPS* to the left (disabled).

      .. figure:: images/sqlplay7.png

#. From the left-hand side, click **Add Action** below the *Actions* section.

#. Click **Select** on the *Email* action.

   The e-mail will serve as notification that an alert has been raised, that a log file has been uploaded to Google Drive (with  link). Fill out the following fields as indicated:

   -**Recipient** Your e-mail address (ex. `first.last@nutanix.com`).
   -**Subject** ``X-Play notification for {{trigger[0].alert_entity_info.name}}``
   -**Message** ``This is a message from Prism Pro X-Play. Logs have been collected for your SQL server due to a high buffer pool size event and are available for you at https://drive.google.com/drive/folders/1e4hhdCydQ5pjEKMXUoxe0f35-uYshnLZ?usp=sharing``

      .. figure:: images/sqlplay9.png

#. Click **Save & Close**.  button and save it with a name *Initials*\ **- High Buffer Pool Size**. Slide the *Playbook Status* to **d**.

  .. figure:: images/sqlplay10.png

#. Now we will trigger the workflow, launch the console for your VM where the SQL Server is running using the credentials listed below. There is a *HammerDB* application already installed on the VM. In order to cause a spike in the metrics we will run a powershell script to create some users on the Server, Go to **Local Disk(C:) > Program Files > HammerDB** and right-click on the file **workload.ps1** and select **Run with Powershell** as shown in the figure below. You could also click on **HammerDB** on the left side as one of the quicklinks.

- **Username: Administrator**
- **Password: Nutanix/4u**.

 .. figure:: images/hammerdb.png

#. It may take up to 5 minutes for the metrics to spike on the Server, you can skip to the **Appplication Discovery** section below in the meantime which should take roughly the same amount of time in which the policy is raised and the playbook is executed.

#. You should recieve an email to the email address you put down in the first playbook. It may take up to 5-10 minutes.

  .. figure:: images/sqlemail.png

#. Click on the URL in the email to go to the google drive or go directly to https://drive.google.com/drive/folders/1e4hhdCydQ5pjEKMXUoxe0f35-uYshnLZ?usp=sharing and confirm that the log file has been uploaded.

  .. figure:: images/sqllogfile.png

#. Switch back to the previous tab with the Prism Central console open. Open up the details for the **`Initials`- High Buffer Pool Size** Playbook that you created and click the **Plays** tab towards the top of the view to take a look at the Plays that executed for this playbook. The sections in this view can be expanded to show more details for each item. If there were any errors, they would also be surfaced in this view.

 .. figure:: images/sqlplay11.png


Importing/Exporting Playbooks
+++++++++++++++++++++++++++++++++++++++++++

X-Play now has the ability to import and export playbooks across Prism Centrals. In the example below we will show how to import the playbook that is created in the preceding steps. The user will still need to create the alert policies and go through the workflow to trigger the alert as listed in the steps in the previous section. We recommend reading through the steps to create the playbook and understanding them properly.

#. Download the following file which is an export of the playbook you will need. https://drive.google.com/file/d/1lyVoKI0Xf0lJgC4k9aAfMTdztWD0fVMT/view?usp=sharing

#. Go to Playbooks page and click on **Import**

 .. figure:: images/import0.png

#. You will need to choose the Binary file that you downloaded as the playbook to import.

 .. figure:: images/import1.png

#. You will see some validation errors since the certain fields such as credentials and URLs will be different for your environment. Click on **Import**, we will resolve these errors in the next step.

 .. figure:: images/import2.png

#. Click on the playbook that has just been imported for you- there will be a time stamp in the playbook name. Once opened the you will see that the actions that have validation errors have been highlighted. Even for actions that have not been highlighted make sure to confirm that the information such as **Passwords**, **URLs** and **IP Addresses** for each of the Actions is correct according to your environment. Click on **Update** to change fields in the playbook. Refer to the playbook creation steps above to confirm these fields.

#. First you will need to make sure the alert policy is correct for your playbook. Click on the trigger and choose the Alert Policy you created for the Buffer Pool Size metric above.

#. Then you will need to change the **Password** in the **REST API** action to lookup the VM IP. Change the **Password** field to your Prism Central password.

 .. figure:: images/import5.png

#. Next you need to change the **Password** in the **IP Address Powershell** action to the SQL VM password- **Nutanix/4u** and the name of the user in path to the script to your name(ABC in the figure below).

 .. figure:: images/import6.png

#. Last, make sure the email address in the **Email** action is updated to your email address.

 .. figure:: images/import7.png

#. Once you have changed these fields click on **Save & Close**. If validation errors are still present, the pop-up will say so. otherwise remember to click **Enable** and add your Initials to the playbook name before clicking **Save**

 .. figure:: images/import8.png


Application Discovery with Prism Ultimate
+++++++++++++++++++++++++++++++++++++++++++

Prism Ultimate gives the capability to discover applications running on your ESXi cluster to identify applciation to VM dependency and get a view of the full stack.

#. Using the hamburger menu navigate to **Operations > App Discovery**

 .. figure:: images/appdiscovery1.png

#. Once on the **App Discovery** page click on **Discover** to start discovering the apps running on your cluster.

 .. figure:: images/appdiscovery2.png

#. Discovery will run and give you a summary of the apps discovered and identified. Click on **View App Instances** to view the list. You can run **Discover** periodically by coming to this page to identify new apps.

 .. figure:: images/appdiscovery3.png

#. Going through the list of apps, you will see there are some Unidentified apps in the list. Select any of these Unidentified apps and click on **Actions** to setup a policy to identify the app.

 .. figure:: images/appdiscovery4.png

#. You can identify this app by the Ports that will be auto-filled by Discovery. Name this app, example **Initials- My Special App** and click on **Save and Apply**.

 .. figure:: images/appdiscovery5.png

#. Now you can see the identified app in your list and check that the new identification policy you created has been added to the **Policies** list. Any future apps with these ports will be identified under the same policy.

 .. figure:: images/appdiscovery6.png

#. Delete your policy so that the other users may setup their own. Go back to the apps list and confirm that the app you had idenitified is now **Unknown** again.

 .. figure:: images/appdiscovery7.png

Takeaways
.........

- Prism Ultimate is our solution to being the gap between infrastructure and application and services layers. It covers the IT OPS process ranging from intelligent detection to automated remediation.

- X-Play, the IFTTT for the enterprise, is our engine to enable the automation of daily operations tasks, making it so easy that automation can be built by every admin.

- Prism Ultimate allows the admin to understand the relationship between their applications and infrastructure with broader visibility and intelligent insights learning.

- X-Play can be used seamlessly with the Application data monitored via Prism Ultimate to build smart automation that can alert and remediate issues both on the infrastructure and on applications
