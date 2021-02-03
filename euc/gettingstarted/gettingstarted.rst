.. _snow_gettingstarted:

---------------
Getting Started
---------------

This lab track is designed to showcase Nutanix as an ideal platform for delivering a true hybrid cloud for EUC workloads, leveraging both the flexibility of AWS and Nutanix Clusters and integration with Citrix Virtual App and Desktops.

In these exercises, you'll be playing the part of Widget Inc.'s IT admin extraordinaire, Alex. Alex...

On-prem environment with limited capacity
Due to global events, you've seen a significant increase in demand for virtual desktops
Also have seasonal usage spikes, short term consultants, etc.
Have an established on-prem golden image
want security that follows your users
want to provide service desk operators with the ability to easily add new desktops to the least loaded cluster dynamically


Your Environment
++++++++++++++++

To let you experience the most fun and interesting parts of the lab, as well as accommodate the large number of simultaneous users, multiple components have already been staged for you. *Let's explore!*

Refer to :ref:`clusterassignments` for the details required to access your environment.

Open **Prism Central** in your browser and log in with the provided credentials.

   .. figure:: images/1.png

Citrix Desktop Delivery Controller
..................................

A Citrix Desktop Delivery Controller (DDC) has been deployed on each shared environment via Calm Blueprint, which can be viewed in **Prism Central > Services > Calm > Blueprints > CitrixBootcampInfra**.

   .. figure:: images/2.png

The DDC is responsible for...

Tools VM
........

The Windows Tools VM provides a number of different applications used across multiple Nutanix Bootcamps. Filter for your **USER**\ *##* in **Prism Central > Virtual Infrastructure > VMs** and take note of the IP of your tools VM, as you will be connecting to this VM via RDP (using **NTNXLAB** Administrator credentials).

   .. figure:: images/3.png

In the following labs you will use the Tools VM to access the Citrix DDC using the **Desktop Studio** application. You will also install the **Citrix Workspace** client on this VM to test the connection to your virtual desktops.

Gold Image
..........

One of the benefits of using Clusters to expand your EUC environment is not having to build, optimize, and test a whole new master image for your desktop pools - so to save you time in the lab, you'll use the Gold Image VM that Alex has already provisioned.

This VM already has the Citrix Virtual Desktop Agent (VDA) installed and optimizations applied. **There is no need to power on this VM.**

   .. figure:: images/4.png
