.. _snow_gettingstarted:

---------------
Getting Started
---------------

This lab track is designed to showcase Nutanix as an ideal platform for delivering a true hybrid cloud for self-service IaaS, leveraging both the flexibility of AWS and Nutanix Clusters and integration with IT service management platform, ServiceNow.

In these exercises, you'll be playing the part of Widget Inc.'s IT admin extraordinaire, Alex. Alex...

Have on-prem environment with limited capacity
Looking at add self-service for end users, with ability to easily add capacity
Need control over approvals
Want an active/active approach with automatic DR between sites
Portability of security between sites
interested in autonomous DC operations with approval control

- Application automation with Calm
- DC automation with Prism X-Play
- Self-service, business workflows, alert management, and CMDB with ServiceNow
- easily scale capacity with Clusters

Your Environment
++++++++++++++++

To let you experience the most fun and interesting parts of the lab, as well as accommodate the large number of simultaneous users, multiple components have already been staged for you. *Let's explore!*

Clusters on AWS
...............

#. Refer to :ref:`clusterassignments` for the details required to access your environment.

#. Open **Prism Central** in your browser and log in with the provided credentials.

   .. figure:: images/1.png

   *The most significant component which has been pre-staged is the single node Nutanix Cluster running on AWS. If you have not already viewed the Clusters walk through, refer to that now to understand how this environment is deployed.*

   .. figure:: images/2.png

   *By leveraging Clusters, Alex has overcome Widget Inc.'s inability to quickly procure and deploy new infrastructure in their datacenter, and can now address the growth, spikes, and seasonality that have caused workload disruptions in the past.*

   <MORE TO COME>

ServiceNow
..........

ServiceNow is a SaaS platform that began as an IT Service Management (ITSM) tool that has evolved into an all-encompassing enterprise service management tool, powering service desks, customer service, HR service delivery, business app store, and even resolving security threats.

To simplify and accelerate developing new apps and integrations for the platform, ServiceNow `provides free developer instances of its entire platform <https://developer.servicenow.com/>`_ to users - *these instances are great for labs and demos too!*

In addition to your on-prem and AWS Nutanix clusters, each group of users will share a **pre-staged** ServiceNow Developer Instance. We'll cover more about the environment throughout the labs.

   .. figure:: images/3.png
