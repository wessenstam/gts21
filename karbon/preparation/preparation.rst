.. _environment_setup:

----------------
Deploying Karbon
----------------

.. note::
   Estimated time **45 minutes**

Prepare your environment
++++++++++++++++++++++++

For this workshop to be run, we need to prepare the environment. Follow the next steps to make your environment ready. They are in high level:

- Enable Karbon
- Download the Karbon needed OS
- Deploy a Kubernetes Development cluster

Enable Karbon
.............

Follow these steps to enable Karbon

#. Open your Prism Central and click :fa:`bars` -> Services -> Karbon

#. If Karbon has not been enabled yet, click the Enable button. This will take a few seconds.

   .. note::

      This is a one-time operation, which may have been completed by another person already on this cluster.

#. To deploy a Kubernetes cluster we need to have an operating system ready. If you see the Download button, click this button to have the OS downloaded.

#. Click the **+Create Kubernetes Cluster** button to start creating a cluster

#. Select the Development Cluster as the Recommended Configuration, and click **Next**

   .. figure:: images/2.png

#. Provide a name for the Kubernetes cluster. Recommended *Initials*-karbon

#. Select your cluster in the **Nutanix CLuster** field. Leave the rest of the fields default.

#. Click **Next**

#. Select your Primary network in the **Network Resources** and leave the **Worker Resources** to 1. Click **Next**

    .. figure:: images/3.png

#. Under the Network Provider, click **Next**
#. In the **Storage Class** screen provide the following information:

   - **Nutanix Cluster** - your assigned cluster
   - **Cluster Username** - admin
   - **Cluster Password** - corresponding password
   - Leave the rest of the fields default

   .. figure:: images/4.png

#. Click on the **Create** button to have the system create the Development cluster. This process takes approx. 5-10 minutes.

   .. figure:: images/5.png

Now that the pre-requirements are ready, we can proceed.

.. |proj-icon| image:: ../../../images/projects_icon.png
.. |bp_icon| image:: ../../../images/blueprints_icon.png
.. |mktmgr-icon| image:: ../../../images/marketplacemanager_icon.png
.. |mkt-icon| image:: ../../../images/marketplace_icon.png
.. |bp-icon| image:: ../../../images/blueprints_icon.png
