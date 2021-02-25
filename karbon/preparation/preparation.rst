.. _karbon_environment_setup:

----------------
Deploying Karbon
----------------

In this exercise you will deploy a Nutanix Karbon Kubernetes cluster.

Deploying Your Cluster
++++++++++++++++++++++

To get the full experience of the simplicity of using Karbon to host cloud native applications on Nutanix, you will first deploy your own Karbon Kubernetes cluster through Prism Central.

#. Refer to :ref:`clusterdetails` for your **Prism Central** IP and **admin** credentials.

#. In **Prism Central**, select :fa:`bars` **> Services > Karbon**.

#. Select **OS Images** left-hand menu and verify the **ntnx-1.0** image is **Downloaded**, as shown below.

   .. figure:: images/1.png

   Otherwise, click **Download**.

   .. note::

      This is a one-time operation per Prism Central instance. This is the CentOS-based disk image, provided by Nutanix, used to provision node VMs within the Karbon cluster.

#. Once the **ntnx-1.0** is **Downloaded**, select **Clusters** from the left-hand menu.

#. Click **+ Create Kubernetes Cluster** to begin deployment.

   .. figure:: images/1a.png

#. To conserve memory and IP resources, select the **Development Cluster** configuration.

   .. raw:: html

      <br><strong><font color="red">If you select Product Cluster, your shared cluster is guaranteed to run out of memory and/or IP addresses while other users are trying to complete their labs. Don't be a reason we can't have nice things.</font></strong><br><br>

#. Click **Next**.

#. On **Name and Environment**, fill out the following fields:

   - **Kubernetes Cluster Name** - USER\ *##*\ -karbon (ex. USER01-karbon)
   - **Nutanix Cluster** - *Select your HPOC cluster* (NOT AWS-Cluster)
   - **Kubernetes Version** - *Leave Default*
   - **Host OS** - ntnx-1.0

   .. figure:: images/6.png

#. Click **Next**.

#. On **Node Configuration**, fill out the following fields:

   - **Kubernetes Node Network** - Primary
   - **Number of Workers** - 1

   .. figure:: images/7.png

#. Click **Next**.

#. On **Network Provider**, keep the default selections and click **Next**.

   .. note::

      Something about Flannel and Calico and Pod CIDR Range/ Service CIDR range

#. On **Storage Class**, fill out the following fields:

   - **Storage Class Name** - *Leave Default*
   - **Nutanix Cluster** - *Select your HPOC cluster* (NOT AWS-Cluster)
   - **Cluster Username** - admin
   - **Cluster Password** - *Your Prism admin password*
   - **Storage Container Name** - Default
   - **Reclaim Policy** - *Leave Default*
   - **File System** - *Leave Default*

   .. figure:: images/8.png

#. Click **Create**.

   This process will take approximately 10 minutes to complete. During this time, Karbon will deploy a non-highly available (development) Kubernetes cluster consisting of the following components:

      - **1x Master Node** - The **master** node acts as the API front-end of the Kubernetes cluster and manages workloads provisioned on **worker** nodes.
      - **1x Worker Node** - The **worker** nodes run the Pods (or containers)
      - **1x etcd Node** - **etcd** is a distributed (in multi-node configurations), key-value store used to store Kubernetes cluster data.

#. Once your **Cluster Status** reaches **Healthy**, you can proceed to the next exercise.

   .. figure:: images/9.png

Connecting to Your Kubernetes Cluster
+++++++++++++++++++++++++++++++++++++

By default, Kubernetes uses a file for authentication instead of username and password. This file, called **kubeconfig.cfg** has to be downloaded and stored locally from the host from which you will access your Kubernetes cluster.

We will use this file to interact with the cluster using the Kubernetes command line utility ``kubectl``, which is pre-installed in your **USER**\ *##*\ **-WinToolsVM** VM.

#. Connect to your **USER**\ *##*\ **-WinToolsVM** VM via RDP using the **NTNXLAB\\Administrator** credentials.

#. Within your **USER**\ *##*\ **-WinToolsVM** VM, open **Prism Central** in Google Chrome.

#. In **Prism Central**, select :fa:`bars` **> Services > Karbon**.

#. Select your **USER**\ *##*\ **-karbon** cluster and click **Actions > Download Kubeconfig**.

   .. figure:: images/10.png

#. Click **Download**.

   .. figure:: images/11.png

   .. note::

      If prompted in Google Chrome with a **This type of file can harm your computer** warning, click **Keep** to download the file.

#. Open the **Downloads** folder in **File Explorer** and note the complete **kubectl.cfg** filename.

   .. figure:: images/12.png

   The file should be named *YOUR-KARBON-CLUSTER-NAME*\ **-kubectl.cfg**. You'll need this in an upcoming step.

   By default, ``kubectl`` will look for a **User Environment Variable** named **KUBECONFIG** to point to your **kubectl.cfg** file. Rather than faff around in the Windows UI, this variable can be easily added from the command line.

#. Open **PowerShell**.

   Do you feel powerful yet? Good, me too.

#. Run ``SETX KUBECONFIG "C:\Users\Administrator\Downloads\YOUR-KARBON-CLUSTER-NAME-kubectl.cfg"`` using your specific **kubectl.cfg** filename.

   .. figure:: images/13.png

   This will create the **User Environment Variable** such that it will persist across command line sessions, however it will not be available within this command line session.

   Windows, can't live with it, can't live without it.

#. Close **PowerShell**.

#. Open **PowerShell**.

   What a rollercoaster ride, huh?

#. Run ``$env:KUBECONFIG`` and verify the path to your **kubectl.cfg** file is returned.

#. Finally, run ``kubectl get nodes`` to list the nodes in your Kubernetes cluster.

   If you have added the path to your **kubectl.cfg** file correctly, the output should resemble the image below.

   .. figure:: images/14.png


.. raw:: html

    <H1><font color="#B0D235"><center>Congratulations!</center></font></H1>

I'm going to bed. We'll add a wrap-up for this tomorrow, yay!
