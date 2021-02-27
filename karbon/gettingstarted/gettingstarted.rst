.. _karbon_getting_started:

---------------
Getting Started
---------------

<STILL NEED TO PROVIDE OVERALL INTRO>

What is Kubernetes? Kubernetes v. Docker. Common term definitions.

..
   You will learn the basic steps to migrate (?) an existing 2-tier application to a containerized application.

   During this workshop, you will learn how to:

      - Build and test the new containers [ARE WE BUILDING, IF THESE ARE DEPLOYED FROM CALM?]

      - Upload the containers to Docker hub registry [WHY?]

      - Deploy the new containers [SOMETHING MORE DESCRIPTIVE?]

Your Environment
++++++++++++++++

To let you experience the most fun and interesting parts of the lab, as well as accommodate the large number of simultaneous users, multiple components have already been staged for you. *Let's explore!*

Tools VM
........

.. note::

   It is highly recommended to complete the entire lab within your **USER**\ *##*\ **WinToolsVM** session. Connect to a fullscreen RDP session, open your lab guide inside of the VM. You'll thank me later.

The Windows Tools VM provides a number of different applications used across multiple Nutanix Bootcamps. Filter for your **USER**\ *##* in **Prism Central > Virtual Infrastructure > VMs** and take note of the IP of your **USER**\ *##*\ **WinToolsVM** VM, as you will be connecting to this VM via RDP (using **NTNXLAB** Administrator credentials).

   .. figure:: images/3.png

In the following labs you will use the Tools VM to access the Kubernetes command line utilities, a graphical Kubernetes monitoring tool, and the **Visual Studio Code** text editor, which will be used to create and modify Kubernetes configuration files.

Nutanix Objects
...............

To conserve memory and IP resources, each cluster runs a pre-staged Nutanix Objects Object Store. During the :ref:`environment_day2` lab you will use this Object Store to provision your own S3 bucket.
