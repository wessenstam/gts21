.. _snow_gettingstarted:

---------------
Getting Started
---------------

This lab track is designed to showcase Nutanix as an ideal platform for delivering a true hybrid cloud for self-service IaaS, leveraging both the flexibility of AWS and Nutanix Clusters and integration with IT service management platform, ServiceNow.

In these exercises, you'll be playing the part of a scrappy IT consultant attempting to win hearts and minds (and open wallets) inside of Party Time, Excellent Inc., by demonstrating solutions to some of PTE's most pressing challenges.

Founded by former public access television rock star duo, Wayne Campbell and Garth Algar, in 1992, Party Time, Excellent, Inc. has become an established name in both manufacturing and retail. Starting out of a two-bay garage in Aurora, Illinois, fashioned into a store selling balloons, streamers, and other "party accessories," PTE has grown to over 2,000 retail locations worldwide. Through acquisitions in the late 90's and early 00's, PTE vertically integrated into related industries, including manufacturing, helium distribution, and party planning. consultative services.

.. figure:: images/waynes_car2a.jpg
   :figwidth: image
   :align: center

   *Founders Campbell and Algar photographed for the 1996 Wall Street Journal article: PTE IPO FTW*

Despite the positive outlook from Chairman Wayne Campbell, PTE is facing significant challenges. The COVID-19 pandemic has slashed retail sales due to both lockdowns and the reduction of large gatherings. In order to survive, PTE has to take massive steps to re-invent itself - **and requires the right technologies and processes to support that transformation.**

.. figure:: https://media.giphy.com/media/y0IjNxdBMPJjG/giphy.gif
   :figwidth: image
   :align: center

   *Chairman Wayne Campbell after being informed that moving to the cloud does not involve airplanes.*

PTE looks pivot away from brick and mortar and ramp up their eCommerce offerings, including entertainment services to spice up Zoom parties, and planning services to re-invigorate safe and socially distant in-person gatherings. They are hiring new app developers and signing contracts with consultants daily. Unfortunately, the existing IT team has been unable to keep up with the demands of the growing team.

The primary datacenter, located outside of Chicago, Illinois, has reached capacity.

.. figure:: images/basement.jpg
   :figwidth: image
   :align: center

   *Primary datacenter location of Party Time, Excellent Inc.*

In addition to quickly providing more capacity for workloads, PTE must also provide self-service access for developers to maintain peak efficiency and bring new offerings to market quickly. As their business now solely depends on the uptime of their infrastructure, disaster recovery and active/active datacenters are critical design components - as is ensuring workloads remain secure regardless of where they run in the environment. Finally, automating infrastructure remediation for user issues will help the IT scale operations to support their new influx of internal customers.

A solution to all of that would be truly...

.. figure:: https://media.giphy.com/media/3oEjI8vagntG7EDxgQ/giphy.gif
   :align: center

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
