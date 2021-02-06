.. _snow_gettingstarted:

---------------
Getting Started
---------------

This lab track is designed to showcase Nutanix as an ideal platform for delivering a true hybrid cloud for Database workloads, leveraging both the flexibility of AWS and Nutanix Clusters and new multi-cluster support in Nutanix Era.

In these exercises, you'll be playing the part of Widget Inc.'s IT admin extraordinaire, Alex. Alex...

- On-prem environment with limited capacity
- Currently database architecture does not follow SQL best practices
- Overcrowded database servers creating performance and maintenance issues, failure domain concerns
- Lacking database high availability for key apps
- Manual processes for patching existing database VMs
- interested in an integrated monitoring platform

Your Environment
++++++++++++++++

To let you experience the most fun and interesting parts of the lab, as well as accommodate the large number of simultaneous users, multiple components have already been staged for you. *Read on to learn more!*

Source Database and App Servers
...............................

Using a Calm Blueprint, each on-premises (HPOC) cluster has been pre-staged with the following VMs for each **USER**:

   .. figure:: images/1.png

   - **USER**\ *##*\ **-MSSQL-Source**

      A single instance SQL Server 2016 database server on Windows Server 2019, containing the following 3 databases: **Fiesta, SampleDB, tpcc**. Each of these databases will be used in the lab track.

   - **USER**\ *##*\ **-FiestaWeb**

      A CentOS 7 VM running a Node-based web application used to access the Fiesta database. You can validate your Fiesta application is capable of reaching your source database by browsing to \http://*USER##-FiestaWeb-IP-ADDRESS*\ /

   .. figure:: images/3.png

Nutanix Era
...........

Each shared environment has been pre-staged with a Nutanix Era server, configured as follows:

   - Era multi-cluster support enabled, with both **EraCluster** (HPOC) and **AWS-Cluster** Nutanix clusters registered. When enabling multi-cluster, an Era Cluster Agent VM (4vCPU/4GB) is automatically deployed to each registered cluster, including the cluster running the Era server.

      .. figure:: images/4.png

      The Era Service VM is responsible for...

   - **Era Managed** networks were configured for a subset of the available IP range for both **EraCluster** (HPOC) and **AWS-Cluster**. While external IPAM solutions (including AHV IPAM) can be used for single instance database deployments, Era must control the IP pool for provisioning highly available database clusters, such as SQL Always-On Availability Groups.

      .. figure:: images/6.png

   - **MSSQL_19_SYNCED** Software Profile pre-created using a vanilla Windows Server 2019/SQL Server 2019 VM, and replicated across both **EraCluster** and **AWS-Cluster**.

      Software Profiles are...

   - **MSSQL_19_USER**\ *##* Software Profiles pre-created using the same VM, but located only on **AWS-Cluster**.

      .. figure:: images/5.png

      You will each require your own Software Profile to complete the :ref:`db_patching` exercise. These individual profiles were not replicated across clusters to reduce time and bandwidth consumption during the lab staging process (*~19GiB per profile \* Hundreds of Users, yikes!*).
