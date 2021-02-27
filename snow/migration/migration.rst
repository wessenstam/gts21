.. _snow_migration:

------------------------------
Cross-Cluster DR and Migration
------------------------------

Using the already configured Data Protection Plan for your self-service provisioned VMs, and Nutanix Leap runbook orchestration capabilities, you can demonstrate how PTE can achieve Disaster Recovery for their active/active datacenter deployment - and also how this same approach can be leveraged to migrate workloads across different clouds.

In this scenario, we'll target a VM that was provisioned on your AWS cluster to migrate back on-premises in order to reduce the latency between the VM and a backend database.

.. note::

   As of AOS 5.19, it is also possible to perform VM Live Migration across multiple Nutanix clusters. This feature requires synchronous replication between clusters, meaning that round trip latency needs to be very low (<5ms RTT). Additionally, the clusters must be in separate Nutanix Availability Zones, each with their own Prism Central instance. This is to ensure management plane availability in the result of a site failure.

Creating A Recovery Plan
++++++++++++++++++++++++

#. In **Prism Central**, select :fa:`bars` **> Policies > Recovery Plans**.

#. Click **Create Recovery Plan**.

#. Fill out the following fields:

   - **Recovery Plan Name** - **USER**\ *##*\ -DR (ex. XYZ-DR)
   - **Primary Location** - Local AZ
   - **Recovery Location** - Local AZ
   - **Primary Clusters** - AWS-Cluster
   - **Recovery Clusters** - Your *PHX###* Cluster

   .. figure:: images/1b.png

#. Click **Next**.

#. Click **+ Add Entities** to define which VMs should be included in the Recovery Plan.

#. Observe that only VMs with recovery points shared between the Primary and Recovery clusters are shown. Select your *Initials*\ -**CentOS####** VM and click **Add**.

   .. figure:: images/2.png

#. Select your VM and observe the available options.

   .. figure:: images/3.png

   AHV Recovery Plans, also referred to as Leap, make it incredibly simple to manage multi-VM failovers, including power-on sequences, delays, and executing scripts on VMs to perform tasks such as updating configuration files or starting services.

#. Click **Next** to begin configuring network mappings between the two sites.

   .. figure:: images/4.png

   Each Recovery Plan allows you to map both **Production** and **Test** networks. Failover tests can be performed to evaluate recovery plans without taking down production VMs by provisioning VM clones to an isolated network.

#. Fill out the following fields:

   - **AWS-Cluster (Primary) > Production** - User VM Network
   - **AWS-Cluster (Primary) > Test Failback** - *Leave blank*
   - **POC### (Recovery) > Production** - Secondary
   - **POC### (Recovery) > Test Failback** - *Leave blank*

   .. figure:: images/5.png

   Observe the default behavior for mapping VM IPs is to match the 4th octet value on the recovery location, making scripting and other updates predictable. Additionally, you can specify custom static IP mapping on a per-VM basis for VMs running Nutanix Guest Tools.

#. Click **Done > Continue** to save your Recovery Plan.

Executing A Failover
+++++++++++++++++++

#. After you are returned to the list of available **Recovery Plans**, right-click your **USER**\ *##*\ **-DR** plan and select **Failover** to begin your migration.

   .. figure:: images/6b.png

#. Fill out the following fields:

   - **Failover Type** - Planned Failover
   - **Failover From > Cluster** - AWS-Cluster
   - **Failover To > Cluster** - Your *PHX###* Cluster

   Under **Recovery Status** you should observe the plan discover all VMs that would be impacted by the failover. A planned failover is the suitable approach for our migration as this will ensure the VM is gracefully powered off and a final recovery point taken and synced between sites.

   .. figure:: images/7.png

#. Click **Failover**.

#. If prompted about an **unsupported license** warning, click **Execute Anyway**.

   .. note::

      For VMs with aggressive change rates or site-to-site connections with poor bandwidth that could result in extending downtime for the VM to allow the migration to take place, another approach would be to use the **Nutanix Move** tool.

      Move is a Nutanix supported tool that is typically used to migrate between hypervisors, but in the case of this AHV to AHV migration, is capable of taking and syncing snapshots continuously to this migration destination until a minimal cutover window is possible, and can be executed at the administrator's discretion.

#. Click on your **USER**\ *##*\ **-DR** plan, and select the **Tasks > Failover** tabs to view the live progress.

   .. figure:: images/8.png

   Due to the lack of proper licensing in the lab environment, it is expected that the **Validating Recovery Plan** task will fail.

Validating the Migration
++++++++++++++++++++++++

#. Once the Recovery Plan has completed, return to **Prism Central > Virtual Infrastructure > VMs** and select your *Initials*\ **-CentOS####** VM. Observe that it is now running on your **POC###** cluster.

   .. figure:: images/9.png

#. Under **Recovery Points > Current Protection Status**, observe that your data protection policy is still active, and snapshots are now scheduling to be replicated back to your **AWS-Cluster**, allowing for future migrations or DR events to seamlessly transition back to the public cloud.

   .. figure:: images/10.png

#. Log into **Prism Central** as your **user**\ *##*\ **@ntnxlab.local** account and verify your user still has the ability to manage their assigned resources post-migration.

   .. figure:: images/11.png

#. SSH into your VM or click **Launch Console** and re-attempt your pings to **USER**\ *##*\ **-FiestaWeb** and **USER**\ *##*\ **-MSSQL-Source** IP addresses. You should observe that you are still isolated from **USER**\ *##*\ **-FiestaWeb** and you now have minimal latency to connect to your **USER**\ *##*\ **-MSSQL-Source** database - goal achieved!

   .. figure:: images/12.png

Takeaways
+++++++++

- Native data replication functionality and Nutanix Leap allow you to easily migrate workloads between clouds with minimal downtime

- The same approach can be used to address Disaster Recovery in the event of site failure.

- Through the Nutanix API, you could further automate migrations based on alert or cost triggers
