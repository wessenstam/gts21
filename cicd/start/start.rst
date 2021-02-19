.. _environment_start:

---------------
Getting Started
---------------

You will learn the basic steps to migrate (?) an existing 2-tier application to a containerized application.

During this workshop, you will learn how to:

- Build and test the new containers (locally?)
- Upload the containers to Docker hub registry
- Deploy the new containers (somewhere else than step 1?)

Before you begin
++++++++++++++++

   - Docker Hub account is needed for saving/uploading the images for the Fiesta application. Create an account using http://hub.docker.com.

Description of the blueprint
............................

The deployed blueprint provides the following automated steps:

#. Deploys (3) CentOS VMs with the *UserXX* prefix.
#. Updates CentOS with the latest packages.
#. Installs Docker.
#. Deploys the MariaDB database for storing data required by the Fiesta app.
#. Registers the MariaDB VM to Era.
#. Fiesta app, which creates a dynamic webpage based on the data within the MariaDB database.

.. |proj-icon| image:: ../../images/projects_icon.png
.. |bp_icon| image:: ../../images/blueprints_icon.png
.. |mktmgr-icon| image:: ../../images/marketplacemanager_icon.png
.. |mkt-icon| image:: ../../images/marketplace_icon.png
.. |bp-icon| image:: ../../images/blueprints_icon.png

Pete Notes
..........

CICD
====

Should we explain what NPM and similar things are, whether in appendix/glossary, or included in this workshop, with a brief description?

We don't explain what the fiesta app is, and I think we lose some impact when we create the docker container, as we don't understand what that docker container is replacing.

There's a fair bit of "if this happens" or "this may happen" or "you should see". I'd like us to be a bit more definitive. If that means running through it again from scratch, so be it.

When we are running commands, maybe do bash so folks can easily copy/paste without risk of not including everything (I noticed this here with a period).

Any way we can use variables in any of this stuff that uses <DOCKER-VM-IP-ADDRESS>?

I'm very concerned that some of this is so fiddly, if one thing is wrong, the entire workshop is blown up and is going to require a TON of effort to troubleshoot it.

[Phase 3] Are there any sections that will step on each other if the user doesn't use a unique name?

We should wipe all browser history, since I can see the previous Google searches performed by others.

Bit tedious to keep entering credentials to push to repo. Can we somehow save their info to prevent this?

Karbon
======

Can we add the environment piece to the Windows image, vs. having the user do it?

[Installation for Windows] Lots of fiddly copy/paste - especially worried about user error here. If you don't have everything in a single line, this will not execute (>>).

This whole process is not very "Nutanix"
