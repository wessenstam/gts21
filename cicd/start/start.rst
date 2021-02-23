.. _environment_start:

---------------
Getting Started
---------------

You will learn the basic steps to migrate [IS THAT RIGHT?] an existing 2-tier application to a containerized application.

During this workshop, you will learn how to:

   - Build and test the new containers [ARE WE BUILDING, IF THESE ARE DEPLOYED FROM CALM?]

   - Upload the containers to Docker hub registry [WHY?]

   - Deploy the new containers [SOMETHING MORE DESCRIPTIVE?]

Before you begin
++++++++++++++++

   - Docker Hub account is needed for saving/uploading the images for the Fiesta application. Create an account using http://hub.docker.com.

   - Open a Notepad (or similar text editor) to store credentials, keys, and passwords.

Description of the blueprint
++++++++++++++++++++++++++++

The deployed blueprint provides the following automated steps:

   - Deploys (3) CentOS VMs with the *UserXX* prefix.

   - Updates CentOS on all 3 VMs.

   - (VM1) Installs Docker. [DESCRIPTION?]

   - (VM2) Deploys the MariaDB database and registers the MariaDB VM to Era. This VM houses the database we utilize for storing the Fiesta app's data.

   - (VM3) Deploys the Fiesta app. This creates a dynamic webpage based on the data within the MariaDB database.

.. |proj-icon| image:: ../../../images/projects_icon.png
.. |bp_icon| image:: ../../../images/blueprints_icon.png
.. |mktmgr-icon| image:: ../../../images/marketplacemanager_icon.png
.. |mkt-icon| image:: ../../../images/marketplace_icon.png
.. |bp-icon| image:: ../../../images/blueprints_icon.png
