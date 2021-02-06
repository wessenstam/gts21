.. _euc_expand:

------------------
Provision & Expand
------------------

In this exercise...

Provisioning On-Prem Desktops
+++++++++++++++++++++++++++++

Snapshotting Your Gold Image
............................

#. Refer to :ref:`clusterassignments` for the details required to access your environment.

#. Log into your **HPOC Prism Element** ex. (X.X.X.37) using the provided credentials.

#. Click the **Home** dropdown menu and select **VM**.

#. Within the **Table**, search for the **CitrixGoldImage** VM.

#. Right-click the **CitrixGoldImage** VM and select **Take Snapshot**.

   .. figure:: images/1.png

#. Specify a name for your snapshot that includes your **USER**\ *##* ID, as shown in the screenshot below.

   .. figure:: images/2.png

#. Click **Submit**.

Creating Your On-Prem Machine Catalog
.....................................

#. Connect to your **USER**\ *##*\ **-WinTools** VM via an RDP client using the **NTNXLAB\\Administrator** credentials.

   .. note::

      You can also use the VM console through Prism to access the WinTools VM, but RDP will provide a more user friendly experience for the lab.

#. Inside your **USER**\ *##*\ **-WinTools** VM, click the Start button and type **Citrix**. Open **Citrix Studio**.

   .. figure:: images/3.png

#. To connect to your Citrix DDC, specify **DDC.ntnxlab.local** and click **Connect**. The console will use the credentials of the currently logged-in user to connect.

   .. figure:: images/4.png

#. Under **Citrix Studio > Configuration > Hosting**, observe that the pre-staged environment has already added your on-prem HPOC cluster as an available location for desktop provisioning. No further action is required here. This is made possible by the....

   The first step in providing desktops for users is to provision a pool, referred to as a Machine Catalog,
   based on your Gold Image snapshot.

#. Under **Citrix Studio > Machine Catalogs**, click **Create Machine Catalog** from the Actions menu. Click **Next**.

   .. figure:: images/5.png

#. Select **Single-session OS** to create a VDI pool. Click **Next**.

#. Select **Machines that are power managed** and **Citrix Machine Creation Services**. Ensure **NutanixResources (Zone: Primary)** is set for **Resources**, this is what will allow you to select from available snapshots on your on-prem HPOC cluster.

   .. figure:: images/6.png

#. Click **Next**.

#. Select **I want users to connect to a new (random) desktop each time they log on** to configure a non-persistent desktop pool.

#. Select the **Default** storage container to place the VM identity disks. Click **Next**.

#. Select the Nutanix snapshot you created in **Steps 5-7** to be used in provisioning your desktop pool.

   .. figure:: images/7.png

#. Click **Next**.

#. Use the default **1 VM, 4096MB memory, 2 vCPU, 2 Cores per vCPU** configuration. This will apply to all VMs provisioned as a part of this catalog, regardless of configuration of the Gold Image VM.

   .. figure:: images/8.png

#. Click **Next**.

#. Select **Create new Active Directory accounts** for your desktops, and specify **USER**\ *##*\ **-ONPREM##** (ex. USER01-ONPREM##) as your **Account naming scheme**.

   The final **##** signs act as an automatic enumerator as you continue to add desktops to the pool (ex. 01, 02, 03, etc.).

   .. figure:: images/9.png

#. Click **Next**.

#. Specify **USER**\ *##* **ONPREM Windows 10** as your **Machine Catalog name** and optionally provide a description as seen in the screenshot below.

   .. figure:: images/10.png

#. Click **Finish** to begin provisioning your desktop pool.

   MCS will now create a clone from the snapshot of **CitrixGoldImage**. When using MCS, the Delivery Controller copies the gold image to each configured datastore in the Host Connection. In a traditional SAN scenario (or using MCS with local storage) this can be a time consuming event, as the Machine Catalog may be spread over several volumes to achieve the desired performance. In a Nutanix cluster you would typically have a single datastore (Storage Container) servicing all desktops, simplifying the configuration and improving the time to provision a Machine Catalog.

   .. figure:: images/12.png

   Observe the Preparation clone booting in **Prism** briefly before shutting down and being removed automatically. Attached to this VM is a separate disk that walks through multiple steps to ensure the VM is ready to be used for the Machine Catalog.

   The preparation stage will enable DHCP, perform a Windows licensing "rearm" to ensure it is reported to the Microsoft KMS server as a unique VM, and similarly perform an Office licensing "rearm". Studio will automatically create a snapshot of the VM in this state once it has completed preparation and shut down.

   .. figure:: images/13.png

   MCS will now create the VMs for our Machine Catalog. This involves the creation of the VMs and the cloned base vDisk, as well as the creation of a small (16MB maximum) vDisks called the Identity (ID) disks. The ID disk contains information unique to each VM that provides its hostname and Active Directory Machine Account Password. This information is ingested automatically by the Citrix Machine Identity Service and allows the VM to appear as unique and allowing it to join the domain.

   .. figure:: images/14.png

   Observe the clone exists in **Prism Element** but is not powered on. Select your  and observe both the OS vDisk and ID disk attached to the VM on the **Virtual Disks** tab below the VMs table in **Prism Element**. Each VM appears to have its own unique read/write copy of the gold image. With VMs in a Machine Catalog spanning several Nutanix nodes, data locality for VM reads is provided inherently by the Unified Cache.

   .. figure:: images/15.png

   This MCS implementation is unique to AHV. For non-persistent Machine Catalogs, other hypervisors link to the base golden image for reads and apply writes to a separate disk, referred to as a differencing disk. In these scenarios, Nutanix Shadow Clones are used to provide data locality for VM reads. Shadow Clones is a feature that automatically provides distributed caching for multi-reader vDisks.

   .. note:: To learn about MCS provisioning in greater detail, see the following articles:

     - `Citrix MCS for AHV: Under the hood <http://blog.myvirtualvision.com/2016/01/14/citrix-mcs-for-ahv-under-the-hood/>`_
     - `Citrix MCS and PVS on Nutanix: Enhancing XenDesktop VM Provisioning with Nutanix  <http://next.nutanix.com/t5/Nutanix-Connect-Blog/Citrix-MCS-and-PVS-on-Nutanix-Enhancing-XenDesktop-VM/ba-p/3489>`_

     To learn more about how Nutanix implements Shadow Clones, see the `Shadow Clones <https://nutanixbible.com/#anchor-book-of-acropolis-shadow-clones>`_ section of the Nutanix Bible.

Creating Your Delivery Group
............................

#. Once the catalog has been provisioned, in **Citrix Studio**, select **Delivery Groups** and click **Create Delivery Group**.

   Delivery Groups are collections of machines from one or more Machine Catalogs. The purpose of a Delivery Group is to specify what users or groups can access the machines.

#. Click **Next**.

#. Select your **USER**\ *##* **ONPREM Windows 10** machine catalog and click **Next**.

   Observe you also have the ability to control how many machines you want to make available for delivery.

   .. figure:: images/16.png

#. Select **Restrict use of this Delivery Group to the following users** and click **Add**.

#. Specify **user**\ *##*\ **;devuser**\ *##* (ex. user01;devuser01) in the open field and click **Check Names**.

   .. figure:: images/17.png

   This will allow only the two assigned AD accounts to access desktops published as part of this Delivery Group.

#. Click **OK**. Click **Next**.

#. On the **Applications** page, click **Next**. In this scenario you will be publishing the full desktop rather than seamless applications hosted by a desktop.

#. On the **Desktops** page, click **Add**.

#. Specify **Windows 10** as a **Display name**. As you are restricting the Delivery Group to only your users, there is no need to identify the desktop name that the end user sees with your **USER**\ *##* ID.

   .. figure:: images/18.png

#. Click **OK**. Click **Next**.

#. Specify **USER**\ *##* **Windows 10** as your **Delivery Group name**.

   This is the value shown to manage the Delivery Group within Citrix Studio, and should be unique.

   .. figure:: images/19.png

#. Click **Finish**.

#. Following creation of the Delivery Group, observe in **Prism** that your **USER**\ *##*\ **-ONPREM01** VM been has powered on.

#. In **Citrix Studio**, right-click your Delivery Group and click **View Machines**. Alternatively you can double-click on the name of the Delivery Group.

   Observe the powered on desktop soon appears as **Registered** with the Delivery Controller, indicating the desktop is ready for user connection.

   .. figure:: images/20.png

Testing Your Desktop
....................

#. Within your **USER**\ *##*\ **-WinTools** VM, open **Google Chrome** and browse to http://ddc.ntnxlab.local/Citrix/NTNXLABWeb/.

#. When prompted, click **Detect Receiver**.

   As the Citrix Workspace client app is not installed with the WinTools VM, detection will fail.

#. Click **Download**.

   .. figure:: images/21.png

#. Launch **CitrixWorkspaceApp.exe** and click **Run**.

#. Complete the installation using the default settings and click **Finish**.

#. Return to **Chrome** and click **Continue** or refresh http://ddc.ntnxlab.local/Citrix/NTNXLABWeb/.

   .. figure:: images/22.png

   .. note::

      If prompted by the browser, click **Open Citrix Workspace Launcher**.

#. Log in using your **NTNXLAB\\user**\ *##* (ex. NTNXLAB\\user01) credentials.

#. If your desktop does not automatically launch, select **Desktops** from the toolbar and click your **Windows 10** desktop.

   .. figure:: images/23.png

   You should now be logged into a fresh, optimized Windows 10 virtual desktop running on Nutanix AHV.

   .. figure:: images/24.png

Expanding Into The Cloud
++++++++++++++++++++++++

The bad news is that you're running low on resources in your on-prem cluster, the good news is that you've already done all the hard work in order to rapidly expand your desktop resources to meet user need.

Replicating Your Gold Image
...........................

Typically when...

In order to conserve time and allow you to complete additional labs, we have pre-staged a copy of the CitrixGoldImage VM to your **AWS-Cluster**.

#. Refer to :ref:`clusterassignments` for the details required to access your environment.

#. Log into your **AWS-Cluster Prism Element** using the provided credentials.

#. Click the **Home** dropdown menu and select **VM**.

#. Within the **Table**, search for the **CitrixGoldImage** VM.

#. Right-click the **CitrixGoldImage** VM and select **Take Snapshot**.

#. Specify a name for your snapshot that includes your **USER**\ *##* ID, as shown in the screenshot below.

   .. figure:: images/2.png

#. Click **Submit**.

Adding Clusters to Citrix Studio
................................

#. Within your **USER**\ *##*\ **-WinTools** VM, open **Citrix Studio** and select **Configuration > Hosting**.

#. Click **Add Connection and Resources** from the Actions menu.

   .. figure:: images/25.png

#. Select **Create a new Connection** and fill out the following fields:

   - **Connection  type** - Select **Nutanix AHV**
   - **Connection address** - *Your AWS Cluster Prism Element VIP*
   - **User name** - admin
   - **Password** - Refer to :ref:`clusterassignments`
   - **Connection name** - USER\ *##* Clusters (ex. USER00 Clusters)
   - **Create virtual machines using** - Select **Studio Tools**

   .. figure:: images/26.png

#. Click **Next**.

   The Nutanix AHV plugin will attempt to connect to your cluster to retrieve available networks.

#. Specify **USER**\ *##*\ **Clusters** as the **Name for these resources** and select the default network for your virtual desktops.

   .. figure:: images/27.png

Creating Your Cloud Machine Catalog
...................................

#. In **Citrix Studio > Machine Catalogs**, click **Create Machine Catalog**.

#. Complete the **Machine Catalog Setup** with the following configuration changes:

   - On **Machine Management**, select your **USER**\ *##* **Clusters** as **Resources**

      .. figure:: images/28.png

   - On **Desktop Experience**, select **I want users to connect to a new (random) desktop each time they log on**

   - Select your **default-container** and the snapshot you created from the **CitrixGoldImage** VM

   - On **Virtual Machines**, increase the number of virtual machines from **1** to **4**

   - On **Computer Accounts**, specify **USER**\ *##*\ **-CLOUD##** (ex. USER01-CLOUD##) as your **Account naming scheme**

   - On **Summary**, specify **USER**\ *##* **CLOUD Windows 10** (ex. USER01 CLOUD Windows 10) as your **Machine Catalog name** and optionally provide a description.

#. Click **Finish** to begin provisioning your desktop pool.

   This will follow the same preparation and cloning process as your on-prem Machine Catalog and should complete within approximately 2-3 minutes.

   .. figure:: images/29.png

   Observe that regardless of the number of virtual machines being provisioned, the amount of time it takes to prepare and clone the desktop pool is the roughly the same, due to AHV's fast metadata VM cloning.

Adding Cloud Desktops to Your Delivery Group
............................................

#. In **Citrix Studio > Delivery Groups**, right-click your **USER**\ *##* **Windows 10** Delivery Group and select **Add Machines**.

   .. figure:: images/30.png

   Despite having been created using your **ONPREM** Machine Catalog, you now have the ability to add desktops from other Machine Catalogs into the same delivery group.

#. Select your **USER**\ *##* **CLOUD Windows 10** Machine Catalog and add all 4 desktops you provisioned in the previous exercise.

   .. figure:: images/31.png

#. Click **Next**. Click **Finish**.

#. Double-click your **Delivery Group** to view all of the included machines and verify one of your CLOUD desktops soon appears as **On** and **Registered**.

   .. figure:: images/32.png

#. Log in to http://ddc.ntnxlab.local/Citrix/NTNXLABWeb/ as **NTNXLAB\\devuser**\ *##* (ex NTNXLAB\\devuser01) and verify you're able to connect to the Clusters-hosted desktop.

   That's literally it. It's that easy.

Takeaways
+++++++++

- Combo of Clusters/MCS/AHV plugin makes for super simple scaling
- Keep your own image
- Keep your own Citrix infrastructure
- How could we build on this? Files + Peer for active/active user profiles and shares across on-prem and cloud; native AOS data replication for persistent desktop DR and syncing gold image changes; adding in Citrix HA infra (including multi-cluster SQL managed by Era)
