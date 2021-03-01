.. _environment_day2:

---------------------------
Performing Day 2 Operations
---------------------------

We've now deployed our initial infrastructure and application, but there are a number of other Day 2 considerations for running Kubernetes infrastructure that we'll explore, including:

   - Monitoring
   - Logging
   - Cluster Expansion
   - Cluster Upgrades
   - Backup

Monitoring With Prometheus And Grafana
++++++++++++++++++++++++++++++++++++++

Monitoring is one of the most important parts of administrating a Kubernetes Cluster, especially when most services are running in a network that can not be reached from the outside world. The solution to this is to run the monitoring stack within the cluster and, similar to **Fiesta**, expose the web frontend.

`Prometheus <https://prometheus.io/>`_ and `Grafana <https://grafana.com/>`_ are the peanut butter and jelly of Kubernetes monitoring solutions. Prometheus is an open source platform used for event monitoring and alerting, and Grafana provides rich visualizations from multiple data source backends.

   .. figure:: images/52.png
      :align: center

Deploying Prometheus
.....................

#. *You're already done.* Nutanix Karbon deploys Prometheus as part of the cluster automatically, including persistent storage backed by Nutanix Volumes.

#. In **Lens > Workloads > Pods**, select **All Namespaces** from the dropdown menu.

   .. figure:: images/53.png

#. Select **prometheus-k8s-0** from the list.

#. Under **Volumes**, select the name of the **persistentVolume Claim**

   .. figure:: images/54.png

   This is the 30GiB volume which has been attached to the Pod using the **Nutanix Container Storage Interface (CSI)** plugin. As Pods are stateless sessions, it is critical for certain types of Pods to be able to store data that can persist across Pod deployments - *like when you're trying to store monitoring data!*

   The **Nutanix CSI** can provide persistent Kubernetes storage using either Nutanix Volumes or Nutanix Files.

Deploying Grafana
..................

#. In **PowerShell** on your **USER**\ *##*\ **-WinToolsVM**, run ``kubectl create ns monitoring`` to create the namespace in which we'll deploy Grafana.

#. In **Visual Studio Code**, create a new file and paste the following:

   .. code-block:: yaml

      apiVersion: apps/v1
      kind: Deployment
      metadata:
        name: grafana
        namespace: monitoring
      spec:
        replicas: 1
        selector:
          matchLabels:
            app: grafana
        template:
          metadata:
            name: grafana
            labels:
              app: grafana
          spec:
            containers:
            - name: grafana
              image: grafana/grafana:latest
              ports:
              - name: grafana
                containerPort: 3000
              resources:
                limits:
                  memory: "2Gi"
                  cpu: "1000m"
                requests:
                  memory: "1Gi"
                  cpu: "500m"
              volumeMounts:
                - mountPath: /var/lib/grafana
                  name: grafana-storage
                - mountPath: /etc/grafana/provisioning/datasources
                  name: grafana-datasources
                  readOnly: false
            volumes:
              - name: grafana-storage
                emptyDir: {}
              - name: grafana-datasources
                configMap:
                    defaultMode: 420
                    name: grafana-datasources
      ---
      apiVersion: v1
      kind: Service
      metadata:
        name: grafana
        namespace: monitoring
        annotations:
            prometheus.io/scrape: 'true'
            prometheus.io/port:   '3000'
      spec:
        selector:
          app: grafana
        ports:
          - port: 3000

#. Save the file as **grafana-deploy.yaml** in your **Downloads** folder.

   Note that the **grafana** service is running on port 3000, the same port as your **fiesta-web** service. This is not an issue as each Pod has a unique IP address within the cluster.

#. Run ``kubectl apply -f grafana-deploy.yaml`` to install.

   You can verify Grafana was installed in **Lens > Workloads > Pods**.

   .. figure:: images/55.png

   Next we need to add a route to the **Traefik** configuration in order to access **Grafana**.

#. In **Visual Studio Code**, open your existing **traefik-routes.yaml** file.

#. Paste the following to the end of your file:

   .. code-block:: yaml

       ---
       apiVersion: traefik.containo.us/v1alpha1
       kind: IngressRoute
       metadata:
         name: simpleingressroute
         namespace: monitoring
       spec:
         entryPoints:
           - web
         routes:
         - match: Host(`grafana.lab.local`)
           kind: Rule
           services:
           - name: grafana
             port: 3000

   .. figure:: images/56.png

#. Save the file and run ``kubectl apply -f traefik-routes.yaml`` to update **Traefik**.

   .. figure:: images/57.png

#. Replace *<TRAEFIK-EXTERNAL-IP>* and run the following command in **PowerShell**:

   .. code-block:: powershell

      Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "<TRAEFIK-EXTERNAL-IP>`tgrafana.lab.local" -Force
      cat C:\Windows\System32\drivers\etc\hosts

   Similar to **fiesta-web**, this will add your **hosts** file record mapping **grafana.lab.local** to your **Traefik** external IP address.

#. Open http://grafana.lab.local in your **USER**\ *##*\ **-WinToolsVM** VM.

   .. figure:: images/58.png

#. Log in using the following credentials:

   - **Username** - admin
   - **Password** - admin

#. Set **nutanix/4u** as the **New password** and click **Submit**.

   Before we can build a monitoring dashboard, we first need to add our cluster's **Prometheus** deployment as a data source in **Grafana**. To do so, we'll need the internal Kubernetes network IP for **Prometheus**.

#. In **Lens**, open **Network > Endpoints** and search for **prometheus-operated**.

   .. figure:: images/59.png

   .. note::

      There is also a **prometheus-operator** service, make sure you're looking at **prometheus-operated**!

#. Take note of the **prometheus-operated** Endpoint IP address.

#. In **Grafana**, select the :fa:`cog` **Configuration** icon from the left-hand toolbar.

   .. figure:: images/7.png

#. Under **Data Sources**, click **Add data source** and select **Prometheus**.

   .. figure:: images/60.png

#. Set **URL** to \https://*<prometheus-operated-Endpoint-IP>*:9090

   .. figure:: images/61.png

#. Click **Save & Test** at the bottom of the page.

   .. figure:: images/9.png

   If you do not receive a message indicating the **Data source is working**, double check you have the correct **prometheus-operated** Endpoint IP, and have typed the **URL** correctly.

   *Time to take the first bite of our peanut butter and jelly sandwich!*

Building Grafana Dashboards
...........................

In this exercise we'll build our own, simple chart to display our Karbon cluster's CPU utilization average over the past 5 minutes.

#. Select **Dashboards > Manage** from the left-hand toolbar in **Grafana**.

   .. figure:: images/62.png

#. Click **New Dashboard** then **+ Add new panel**.

#. In the **Enter a PromQL query** field, type **cpu**.

   .. figure:: images/63.png

   You should be provided with a drop-down menu of many different metrics related to **cpu**.

#. Select **cluster:node_cpu:sum_rate5m** and press **Shift+Return** to begin populating data.

#. Click **Apply** to save the chart to your dashboard.

   .. figure:: images/64.png

#. Click the :fa:`floppy-o` icon to **Save** your dashboard. Provide a name and click **Save**.

   To see a more sophisticated example of the type of visualization **Grafana** can provide, we can easily import publicly available, pre-built dashboards.

#. Select **Dashboards > Manage** from the left-hand toolbar and click **Import**.

#. Under **Import via grafana.com**, specify **1621** and click **Load**.

#. Under **Prometheus**, select your **Prometheus** data source and click **Import**.

   .. figure:: images/65.png

#. Kick up your feet and relax while the open source community does your job for you.

   .. figure:: images/66.png

   You can `browse the Grafana Labs site for user submitted dashboards <https://grafana.com/grafana/dashboards>`_ that target all types of platforms and workloads.

   By leveraging the built-in **Prometheus** deployment and persistent container storage provided by Karbon, you can deploy a full Kubernetes monitoring solution in minutes.

Logging With ELK Stack
++++++++++++++++++++++

Similar to monitoring, a robust logging solution for your Kubernetes environment is critical to quickly diagnosing issues with services. Karbon provides a complete **ELK** deployment as part of your cluster for logging related to the Kubernetes cluster infrastructure. The **ELK** stack consists of **Elasticsearch**, **Logstash**, and **Kibana**. `Elasticsearch <https://www.elastic.co/elasticsearch/>`_ is a distributed, full-text search engine responsible for indexing log data to provide quick searches. `Logstash <https://www.elastic.co/logstash>`_ is a data processing pipeline responsible for filtering data and sending to different outputs, including Elasticsearch. `Kibana <https://www.elastic.co/kibana>`_ provides the front end to the stack, letting you explore and visualize data.

   .. figure:: images/67.png

#. In **Prism Central**, select :fa:`bars` **> Services > Karbon**.

#. Click on *your* **USER**\ *##*\ **-karbon** cluster.

#. Select **Add-on** from the left-hand menu and click **Logging** to launch the built-in **Kibana** interface.

   .. figure:: images/68.png

   .. note::

      If prompted to **Try our sample data**, click **Explore on my own**.

#. Select :fa:`cog` **Management** from the left-hand toolbar.

#. Under **Kibana**, click **Index Patterns**.

   .. figure:: images/69.png

#. Under **Index Pattern**, type **\*** to select all indices.

   .. figure:: images/70.png

#. Click **> Next Step**.

#. Under **Time Filter field name**, select **@timestamp** from the dropdown menu.

   This will allow you to filter your data based on the time events were logged.

#. Click **Create Index Pattern**.

#. Click :fa:`compass` **Discover** from the left-hand menu to be able to search your log data.

   .. figure:: images/71.png

   In the example above you can see ~1500 events are being logged every 30 seconds.

#. Search for **ntnx-csi-plugin** to see log entries related to Nutanix persistent container storage.

   This logging deployment only captures logs related to the Kubernetes infrastructure. As demonstrated in previous exercises, Karbon is based on standard Kubernetes and can leverage all the tools in the broad Kubernetes ecosystem. This includes deploying an additional ELK stack for capturing user space loggings.


..
   User space logging environment
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   As we need to see the logs from our pods, at the current release of Karbon, we have to build our own logging Stack. This part of the Module will show you how to use the internal only logging stack and how to install, configure and use another Stack that can be used for the user pods like our MetalLB, Traefik, Fiesta, Grafana and Prometheus Pods.

   This part is all about creating our own Logging Stack.

   We are going to do the following:

   - Create a namespace for the logging
   - Create Elasticsearch environment
   - Create Kibana environment
   - Create Fluentd environment
   - Configure Traefik to alow access to the Kibana Pod

   Namespace
   *********

   To have a logical separation of the Pods we are going to create a new namespace in which we will deploy the full new stack

   #. In the terminal or Powershell session run the following command

      .. code-block:: yaml

           kubectl apply -f https://raw.githubusercontent.com/wessenstam/gts2021-prep/main/Karbon/yaml%20files/EFK%20session/kube-logging-ns.yaml

   #. This will create the Namespace **kube-logging**

      .. figure:: images/14.png

   Elacsticsearch environment
   **************************

   To get this working we need to install a service and the deployment of the Elasticsearch environment

   #. Run the following commands [WHERE?] to get the Elasticsearch environment ready

      .. code-block:: yaml

           kubectl apply -f https://raw.githubusercontent.com/wessenstam/gts2021-prep/main/Karbon/yaml%20files/EFK%20session/elasticsearch_svc.yaml
           kubectl apply -f https://raw.githubusercontent.com/wessenstam/gts2021-prep/main/Karbon/yaml%20files/EFK%20session/elasticsearch_statefulset.yaml

   #. This will create the Namespace **Service and Deployment**

      .. figure:: images/15.png

   Kibana environment
   ******************

   To get this working we need to install a service and the deployment of the Kibana environment

   #. Run the following commands to get the Kibana environment ready

      .. code-block:: yaml

           kubectl apply -f https://raw.githubusercontent.com/wessenstam/gts2021-prep/main/Karbon/yaml%20files/EFK%20session/kibana.yaml

   #. This will create the Namespace **Service and Deployment**

      .. figure:: images/16.png


   Fluentd environment
   *******************

   To get this working we need to install a RBAC, Service account and the Daemonset (pods that are running on all Nodes of the Cluster) of the Fluentd environment

   #. Run the following commands to get the Fluentd environment ready

      .. code-block:: yaml

           kubectl apply -f https://raw.githubusercontent.com/wessenstam/gts2021-prep/main/Karbon/yaml%20files/EFK%20session/fluentd.yaml

   #. This will create the Namespace **Service and Deployment**

      .. figure:: images/17.png

   Total overview
   **************

   #. To get a full overview of the Pods, in Lens change the *Namespace:* to **kube-logging**

      .. figure:: images/18.png

   #. Now only the pods that are part of that namespace. All should have the **Running** status

      .. figure:: images/19.png

   #. When clicking the Network -> Services you would also see the services for the same Namespace

      .. figure:: images/20.png

   Now that we have the EFK logging environment ready, let tell Traefik to route http://kibana.gts2021.local to the Kibana interface so we can administer the logging externally from the Kubernetes cluster.

   Traefik configuration
   *********************

   #. Open the traefik-routes.yaml file and add the following to the end  of the file

      .. code-block:: yaml

           ---
           apiVersion: traefik.containo.us/v1alpha1
           kind: IngressRoute
           metadata:
             name: simpleingressroute
             namespace: kube-logging
           spec:
             entryPoints:
               - web
             routes:
             - match: Host(`kibana.gts2021.local`)
               kind: Rule
               services:
               - name: kibana
                 port: 5601

   #. Save the file
   #. Make the changes to the **hosts** file so kibana.gts2021.local points to the External IP address of Traefik
   #. Use ``kubectl apply -f traefik-routes.yaml`` to tell Traefik to start routing the URL to the Kibana service
   #. Open the Traefik page to see that the route has been aded and is green

      .. figure:: images/21.png

   #. Open a browser and point it to http://kibana.gts2021.local/ . The Kibana page will open

      .. figure:: images/22.png

   #. Click the **Explore on my own** button to proceed

   #. Click the **No** button at the top of the screen

   #. Click on **Index Patterns** under the *Manage and Administer the Elastic Stack* section.

   [CLOSE PANEL ON RIGHT SIDE]

   [ADD INSTRUCTION TO CREATE INDEX PATTERN]

   #. In the **Index pattern** field, type **logstash\*** and click the **> Next step** button

      .. figure:: images/23.png

   #. In the **Time Filter field name** select **@timestamp** [FROM THE DROPDOWN] and click the **Create index pattern** button

      .. figure:: images/24.png

   #. After a few seconds, when you see the total overview of all possible fields, click on the Discover (compass :fa:`compass`) icon on the left hand side of the screen
   #. This should show you all the logs from the system as well as our deployed pods (traefik, fiesta).

   [I DON'T KNOW WHAT I'M LOOKING AT, SO I DON'T KNOW!]

   #. In the Filters field, type ``kubernetes.pod_name : traefik*`` and hit the enter key to filter just on that. Now you would see all logs lines that have the line **kubernetes.pod_name : traefik\*** in them

      .. figure:: images/25.png

   #. There is much more you can do with Kibana, but that is outside of this workshop.


Expanding The Cluster
+++++++++++++++++++++

Based on the insights provided by **Lens**, **Grafana**, or any number of monitoring solutions, you will be able to determine when the Kubernetes cluster is in need of expansion to support running all of your Pods. With Nutanix Karbon, cluster expansion can be performed through **Prism Central** in just a few clicks.

#. In **Prism Central**, select :fa:`bars` **> Services > Karbon**.

#. Click your **USER**\ *##*\ **-karbon** cluster.

#. Select **Nodes > Worker** from the left-hand menu and click **+ Add Worker**.

   .. figure:: images/72.png

   .. note::

      In a **Production** Karbon deployment, you are also able to scale the number of **Master** and **etcd** nodes in the cluster. This is not supported for **Development** clusters.

#. Set **Number of Nodes** to **1** and click **Create**.

   .. figure:: images/73.png

   .. raw:: html

      <BR><font color="#FF0000"><strong>Do not increase your cluster by more than 1 Worker node. There is not enough memory/IP addresses available in the shared lab environment.</strong></font><BR>

   Karbon will begin provisioning an addition Worker Node VM, this process will take ~5-15 minutes to complete. Progress can be monitored in **Prism Central > Activities > Tasks**.

   .. figure:: images/74.png

#. Once your expansion is completed, confirm in **Lens** your new Worker is **Ready**.

   .. figure:: images/75.png

   Next we'll take advantage of the additional Worker by provisioning additional replica Pods to scale performance for our **Fiesta** web service.

#. In **Visual Studio Code**, open **fiesta_app.yaml**.

#. Increase the number of **replicas** to **4** and save your file.

#. In **PowerShell**, run ``kubectl apply -f fiesta_app.yaml`` to apply the change.

#. In **Lens > Workloads > Pods**, observe the new Pods being provisioned. Select each of the 4 Pods and observe they're automatically distributed across the two available worker nodes.

   .. figure:: images/76.png

   This is what allows Cloud Native applications to be so responsive to changes in demand. In this exercise we've manually increased the number of **Workers** and **replicas**, but using a **CI/CD** pipeline the scaling could be fully automated.

   With Nutanix's API first development model you're also able to `scale your Karbon cluster programmatically <https://www.nutanix.dev/reference/karbon/api-reference/cluster/addnodes/>`_, which would allow you to automate cluster growth based on criteria like Pod performance. *Neat!*

Upgrading The Cluster
+++++++++++++++++++++

Currently Nutanix Karbon supports a 1-Click process for upgrading the underlying OS used by the Node VMs, with Kubernetes lifecycle management on the roadmap. Your environment is using the latest available Karbon OS image, but you can view an example of the upgrade process below.

   .. raw:: html

      <br><iframe width="600" height="337" src="https://www.youtube.com/embed/IucbVL8lECk" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe><br>

Backing Up Cloud Native Apps
++++++++++++++++++++++++++++

Even though many container workloads are stateless, backup matters in Kubernetes! Think about it, with a single ``kubectl`` command you could wipe out an entire namespace containing multiple applications. Restoring workloads to a specific point in time needs to be equally as easy. In addition, backup can also be a critical component of regulatory compliance.

In this exercise we will deploy **Kasten K10**, a **Veeam** solution that integrates with **Nutanix Objects** to provide Kubernetes backup capabilities.

Configuring Objects Storage
...........................

In order to provide a storage target for our backup solution, we first need to configure access permissions and provision a **Bucket** within our pre-staged **Nutanix Objects Object Store**.

#. In **Prism Central**, select :fa:`bars` **> Services > Objects**.

#. Under **Access Keys**, select **+ Add People**.

   .. figure:: images/77.png

#. Select **Add people not in a directory service**.

#. Fill out the following fields:

   - **Email Address** - user\ *##*\ \-k10@lab.local (ex. \user01-k10@lab.local)
   - **Name** - user\ *##*\ -k10 (ex. user01-k10)

   .. figure:: images/78.png

#. Click **Next**.

#. Click **Generate Keys**.

#. Click **Download Keys** *before* clicking **Close**, otherwise you will be unable to access your keys.

   .. figure:: images/79.png

   This will download a file containing the **Access Key** and **Secret Key** you will need to access your S3 storage in an upcoming exercise.

#. Under **Object Stores**, click **ntnx-objects** to open your existing Object Store in a new tab.

   .. figure:: images/80.png

#. Click **Create Bucket**.

#. Fill out the following fields:

   - **Name** - user\ *##*\ -k10-bucket (ex. user01-k10-bucket)
   - **Object Versions** - *Leave default*
   - **Lifecycle Policies** - *Leave default*

   .. figure:: images/81.png

#. Click **Create**.

   Now that the bucket exists, we must allow our **user**\ *##*\ **-k10** account to access it.

#. Click your **user**\ *##*\ **-k10-bucket** and select **User Access** from the left-hand menu.

#. Click **Edit User Access**.

#. Fill out the following fields:

   - **People** - user\ *##*\ \-k10@lab.local
   - **Permissions** - Read; Write

   .. figure:: images/82.png

#. Click **Save**.

Configuring DNS
...............

In order for our **K10** application to connect to our Objects bucket as a storage target, it needs to be able to access the bucket via DNS, not IP address. To do this we will need to add the appropriate DNS record for our bucket to the **NTNXLAB.local** DNS server, and update our Karbon cluster to use that DNS server.

#. In **Prism Central**, select :fa:`bars` **> Services > Objects**.

#. Note your **Objects Public IP**. This is the IP used to create client connections to your bucket via S3 APIs.

   .. figure:: images/83.png

   You will need this IP in the following steps.

#. Paste the following into your **USER**\ *##*\ **-WinToolsVM** and replace *<YOUR-BUCKET-NAME>* and *<OBJECTS-PUBLIC-IP>* with your values:

   .. code-block:: powershell

      Invoke-Command -ComputerName dc.ntnxlab.local -ScriptBlock {Add-DnsServerResourceRecordA -Name "ntnx-objects" -ZoneName "ntnxlab.local" -AllowUpdateAny -IPv4Address "<OBJECTS-PUBLIC-IP>"}
      Invoke-Command -ComputerName dc.ntnxlab.local -ScriptBlock {Add-DnsServerResourceRecordA -Name "<YOUR-BUCKET-NAME>.ntnx-objects" -ZoneName "ntnxlab.local" -AllowUpdateAny -IPv4Address "<OBJECTS-PUBLIC-IP>"}

#. Run the commands in **PowerShell**.

   .. figure:: images/84.png

   This will create a **ntnx-objects** subdomain, which corresponds to the name of your Object Store, and a DNS A record for your bucket.

   .. note::

      If the command fails to authenticate to **dc.ntnxlab.local**, you are likely logged into your **USER**\ *##*\ **-WinToolsVM** VM as the **local** Administrator account. You need to be logged in as **NTNXLAB\\Administrator**.

      If the first command fails with **Failed to create resource record ntnx-objects in zone ntnxlab.local on server DC**, this is OK. It means that someone else on your cluster has already run the command to create the subdomain.

#. Run ``ping <YOUR-BUCKET-NAME>.ntnx-objects.ntnxlab.local`` to verify you can resolve the name.

   Next we'll update the DNS configuration for the Kubernetes cluster.

   .. raw:: html

      <BR><font color="#FF0000"><strong>Pay close attention to the following steps. You will be editing network configuration for your Kubernetes cluster and a mistake could leave you unable to access the cluster.</strong></font><BR><BR>

#. Run ``kubectl -n kube-system edit configmap coredns``.

   This will open the cluster DNS **ConfigMap** in **Notepad**.

#. Insert the following *before* the line **kind: ConfigMap** in the file:

   .. code-block:: yaml

      ntnxlab.local:53 {
         errors
         cache 30
         forward . <AUTO AD Server>
      }

#. Replace *<AUTO AD Server>* with the IP of your **NTNXLAB.local** Domain Controller. See :ref:`clusterdetails`.

#. Ensure the indentation of the **YAML** file is correct. After pasting the contents into the file, each line should be indented by 4 spaces from the left edge, as shown below.

   .. figure:: images/85.png

#. Save the file and close **Notepad**.

   .. note::

      If you formatted the file incorrectly, the file will re-open. Refer to the screenshot above to correct your indentation.

#. Run ``kubectl -n kube-system describe configmap coredns`` to verify the configuration has been updated.

   .. figure:: images/86.png

   This will tell the DNS service in Kubernetes to forward DNS requests **ntnxlab.local** (and any subdomains) to your Domain Controller's IP address, allowing the **K10** application to resolve the name of your bucket.

   *Isn't networking fun?!*

Installing K10
..............

Up to this point, we have used manually created manifest files to deploy our applications. For **K10** we will look at a more user friendly way to deploy apps using **Helm**. `Helm <https://helm.sh/>`_ is a community built and maintained package management tool for Kubernetes, similar to **yum** in CentOS or **npm** in Node.

#. In **PowerShell**, run the following:

   .. code-block:: bash

      kubectl create namespace kasten-io
      helm repo add kasten https://charts.kasten.io/
      helm repo update
      helm install k10 kasten/k10 --namespace=kasten-io

   This will define a namespace on the **Kubernetes** cluster in which to manage and monitor the app, add the repository to **Helm** in order to download **K10**, and then install the application.

#. Monitor the deployment in **Lens > Workloads > Pods**.

   .. figure:: images/89.png

   Select the **kasten-io** namespace and wait until all Pods are in a **Running** state, this should take < 5 minutes.

   .. note::

      You may need to close/re-open **Lens** in order to see the new **kasten-io** namespace.

   Similar to our other deployments, we will use Traefik to enable external access to the **K10** frontend. However, we can first quickly verify the app is up and running ``kubectl`` as a temporary proxy.

#. In **Powershell**, run ``kubectl --namespace kasten-io port-forward service/gateway 8080:8000``

#. Open http://127.0.0.1:8080/k10/#/ in your **USER**\ *##*\ **-WinToolsVM** browser.

   .. figure:: images/91.png

   If your deployment was successful, you will be prompted with the EULA.

#. Press **Ctrl+C** in **PowerShell** to stop the proxy.

Adding K10 Traefik Route
........................

#. In **Visual Studio Code**, open your existing **traefik-routes.yaml** file.

#. Paste the following to the end of your file:

   .. code-block:: yaml

      ---
      apiVersion: traefik.containo.us/v1alpha1
      kind: IngressRoute
      metadata:
        name: simpleingressroute
        namespace: kasten-io
      spec:
        entryPoints:
          - web
        routes:
        - match: Host(`k10.lab.local`)
          kind: Rule
          services:
          - name: gateway
            port: 8000

#. Save the file and run ``kubectl apply -f traefik-routes.yaml`` to update **Traefik**.

   .. figure:: images/92.png

#. Replace *<TRAEFIK-EXTERNAL-IP>* and run the following command in **PowerShell**:

   .. code-block:: powershell

      Add-Content -Path C:\Windows\System32\drivers\etc\hosts -Value "<TRAEFIK-EXTERNAL-IP>`tk10.lab.local" -Force
      cat C:\Windows\System32\drivers\etc\hosts

   Similar to **fiesta-web** and **Grafana**, this will add your **hosts** file record mapping **k10.lab.local** to your **Traefik** external IP address.

#. Open http://k10.lab.local/k10/#/ in your **USER**\ *##*\ **-WinToolsVM** VM.

Configuring K10
...............

Now that we have prepared our storage target and deployed **K10**, we're ready to configure **K10** to use our Objects storage and create our first backup policy.

#. In your browser, **Accept** the **K10** EULA.

   .. note::

      If prompted to **Take a Quick Tour**, click **No**.

   You should now see the **K10** dashboard, including multiple applications that have already been discovered on your cluster.

#. Click **Cluster Settings**.

   .. figure:: images/93.png

#. Under **Location Profiles**, click **+ New Profile**.

#. Fill out the following fields:

   - **Profile Name** - nutanix-objects
   - **Cloud Storage Provider** - S3 Compatible
   - **S3 Access Key** - *From your user##-k10@lab.local-keys-<DATE>.txt file downloaded from Objects*
   - **S3 Secret** - *From your user##-k10@lab.local-keys-<DATE>.txt file downloaded from Objects*
   - **Endpoint** - https://ntnx-objects.ntnxlab.local
   - Select **Skip certificate chain and hostname verification**
   - **Region** - *Leave blank*
   - **Bucket Name** - user\ *##*\ -k10-bucket

   .. figure:: images/95.png

   .. note::

      Don't worry Sebastien, these keys aren't valid.

#. Click **Save Profile**.

   You should see a green dialog indicating the connection was successful. Otherwise, ensure your profile inputs are accurate and try saving again.

   Next we'll configure a backup policy.

#. Click **< Dashboard** to return to the **K10** dashboard.

   .. figure:: images/96.png

#. Under **Applications**, select **Unmanaged**.

#. Under **default**, click **Create Policy**.

   .. figure:: images/97.png

   Each of the boxes map to a specific Namespace in your Kubernetes cluster.

#. In the **New Policy** window, leave all of the default snapshot frequency settings.

#. Select **Enable Backups via Snapshot Exports** and ensure **Export Location Profile** is set to your **nutanix-objects** profile.

   .. figure:: images/98.png

   This will export the snapshots created by K10 to your S3 bucket.

#. Click **Create Policy**.

   Instead of waiting for the next scheduled snapshot to take place, we'll force the first backup.

#. Click **Run Once** and **Run Policy**.

   .. figure:: images/99.png

#. Click **< Dashboard**.

#. Under **Activity**, you should see your backup job complete after a few seconds. Select it and view the resources that were exported as part of the backup.

   .. figure:: images/100.png

Restoring K10 Backups
.....................

Now that we have a successful backup, we can restore "clones" of your applications to a separate namespace on the cluster.

#. Select **Applications** from the **K10** dashboard.

#. Under the **default** namespace, click **Restore**.

   .. figure:: images/101.png

#. Select your **default-backup** restore point and then click the **EXPORTED** version.

   .. figure:: images/102.png

   This will ensure we're restoring the data from the Nutanix Objects bucket, and not a local snapshot.

#. Under **Restore Point > Application Name**, click **+ Create A New Namespace**:

   - **New Namespace** - default-restore

   .. figure:: images/103.png

   This will update the **Application Name** to your new namespace.

#. Under **Restore Point > Artifacts**, click **Deselect All Artifacts**.

#. Select only your **fiesta-web-pods** Deployment and your **fiesta-web-svc** Service.

   .. figure:: images/104.png

#. Click the **Restore > Restore** button to start the restore process.

   .. note::

      You may see a *Slow Connection* message pop up. This can be safely ignored.

#. Click **< Dashboard** to return to the dashboard.

   Under **Activity**, you should see your restore operation either **Running** or **Completed**.

   .. figure:: images/105.png

#. In **Lens > Workloads > Pods**, filter for your **default-restore** namespace and observe your Fiesta pods running.

   .. figure:: images/106.png

   *Based on what you've learned so far in the lab, can you build a Traefik route to connect to your default-restore version of your app?*

#. Return to **Prism Central >** :fa:`bars` **> Services > Objects > ntnx-objects** and click your bucket.

   Here you can view the number of objects stored within the bucket and the storage being consumed.

#. Select **Performance** from the left-hand menu to view the load your backup policy has applied to the bucket.

   .. figure:: images/107.png

#. You can also view the bucket contents using the built-in Objects Browser by opening \http://*<OBJECT-STORE-PUBLIC-IP>*:7200 in your browser and logging in with the keys assigned to your **user**\ *##*\ **-k10** user.

   .. figure:: images/108.png

   .. note::

      The snapshot exports from **K10** aren't human readable, so don't expect to find your original **YAML** files!

.. raw:: html

    <H1><font color="#B0D235"><center>You made it!</center></font></H1>

After completing these exercises you should now be more familiar with the infrastructure considerations for production Kubernetes environments.

Nutanix Karbon provides significant value in the deployment and management of your Kubernetes infrastructure, while still providing an open platform capable of integrating with other stack components for logging, monitoring, backup, and more.
