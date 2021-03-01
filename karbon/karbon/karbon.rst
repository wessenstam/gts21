.. _environment_karbon:

------------------------------------
Adding Network Services & Dashboards
------------------------------------

As Karbon is simply providing a streamlined means of provisioning and managing Kubernetes infrastructure, Karbon clusters are able to take advantage of the best of breed tools available in the Kubernetes ecosystem.

In this exercise we will deploy a **MetalLB Load Balancer** and a **Traefik Ingress Controller** for our Kubernetes cluster. Once these are configured, we will evaluate two different Kubernetes dashboard options to provide visualization of operations within the Kubernetes cluster.

If you are already familiar with basic Kubernetes networking, you can skip ahead to `Deploying A Load Balancer`_ to begin the lab. Otherwise, review the primer below.

.. _karbon_networking:

Kubernetes Networking In 5 Minutes
...................................

*I built a container in the last lab, so I'm basically a Docker expert now. How is Kubernetes different?*

   While Kubernetes uses Docker containers, Kubernetes networking is significantly different than what we saw in the **Containerizing Apps and CI/CD** lab. Docker uses host-private networking, so containers can talk to other containers only if they are on the same machine. In order for Docker containers to communicate across nodes, there must be allocated ports on the machine's own IP address, which are then forwarded or proxied to the containers. This obviously means that containers must either coordinate which ports they use very carefully or ports must be allocated dynamically - difficult to coordinate at scale!

   Kubernetes assumes that Pods can communicate with other Pods, regardless of which host they land on. Kubernetes gives every Pod its own cluster-private IP address, so you do not need to explicitly create links between Pods or map container ports to host ports. This means that containers within a Pod can all reach each other's ports on localhost, and all Pods in a cluster can see each other without NAT. In our Karbon cluster, this is implemented using **Flannel** and is automatically configured as part of the cluster deployment.

*But what about parts of our applications, like front end interfaces, that we want to expose to external clients?*

   Kubernetes offers two methods to expose a service, **NodePort** and **LoadBalancer**.

   **NodePort**

   **NodePort** is the simpler, but more primitive, means of getting external access to your service. As shown in the diagram below, the **NodePort** service opens a specific port across all Worker Nodes and any traffic sent to any Worker Node IP on that port would be forwarded to the service.

   .. figure:: images/32.png

   This approach is not recommended for production deployments as it limits you to only one service per port and changes to Node VM IPs create additional work.

   **LoadBalancer**

   A **LoadBalancer** functions similar to an application load balancer you'd find on your network. The **LoadBalancer** service is responsible for assigning a single, external IP to your service and forwarding traffic.

   .. figure:: images/33.png

   The **LoadBalancer** service is not natively implemented by Kubernetes, and will depend on the environment in which you are running. Providers like AWS, Azure, GCP, OpenStack, Tencent Cloud and Alibaba Cloud provide implementations for **LoadBalancers** (*and will charge you for every IP*).

   For our Karbon environment, we will deploy **MetalLB** to act as our **LoadBalancer**.

   .. note::

         Technically, you can also access ports within your Kubernetes cluster using the ``kubectl proxy`` but this would typically only be used for debugging or non-production scenarios as it requires you to run as an authenticated user. *Not something you'd want to expose to the internet, yikes!*

*So if the LoadBalancer service provides external access for Kubernetes services, what does the Ingress Controller do?*

   While the **LoadBalancer** is capable of getting external traffic to our services, it is not capable of providing any filtering or routing that traffic. An **Ingress Controller** fills this void by sitting in front of multiple services and acting as an intelligent entry point for the Kubernetes cluster.

   .. figure:: images/33.png

   Using **Ingress** is common when you want to expose multiple services using the same IP address and multiple services are using the same Layer 7 protocol, like HTTP or HTTPS.

*Matt, I love reading, can you give me more to read?*

   Kubernetes networking is **a lot** to wrap your head around. If you're interested in learning more, `the official Kubernetes.io documentation <https://kubernetes.io/docs/concepts/>`_ has an entire section dedicated to **Concepts** that provides more in-depth explanations and examples. *More reading!*

Deploying A Load Balancer
+++++++++++++++++++++++++

In order to provide network access to any future services you will deploy to your Karbon cluster, you will first need to deploy a **LoadBalancer** solution that Kubernetes will use to provide external IPs.

#. Connect to your **USER**\ *##*\ **-WinToolsVM** VM via RDP using the **NTNXLAB\\Administrator** credentials.

#. Open **PowerShell** and run ``cd ~\Downloads``.

#. Run the following commands to download the YAML files used to install **MetalLB**:

   .. code-block:: powershell

      [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls, [Net.SecurityProtocolType]::Tls11, [Net.SecurityProtocolType]::Tls12, [Net.SecurityProtocolType]::Ssl3
      [Net.ServicePointManager]::SecurityProtocol = "Tls, Tls11, Tls12, Ssl3"
      wget https://raw.githubusercontent.com/metallb/metallb/v0.9.5/manifests/namespace.yaml -OutFile namespace.yaml -UseBasicParsing
      wget https://raw.githubusercontent.com/nutanixworkshops/gts21/master/karbon/yaml%20files/001-metallb.yaml -OutFile metallb.yaml -UseBasicParsing

#. Run the following commands to install **MetalLB**.

   .. code-block:: bash

      kubectl apply -f namespace.yaml
      kubectl apply -f metallb.yaml

   .. figure:: images/9.png

   ``kubectl apply`` creates and updates applications using YAML files, referred to as Manifests, that define Kubernetes resources.

#. Run ``kubectl create secret generic -n metallb-system memberlist --from-literal=secretkey="$(openssl rand -base64 128)"``

   This command creates a **secret** in Kubernetes used to encrypt communications between **MetalLB** Pods.

#. Run ``kubectl get pods -n metallb-system`` to verify your **MetalLB** Pods are **Running**.

   .. figure:: images/10.png

   The Service has two components. The **controller** Pod is lcuster-wide and handles IP address assignments. The **speaker** is a per-Node daemon that advertises services with assigned IPs.

   .. note::

      If your **STATUS** of either Pod is not **Running**, you can run the following to investigate the cause:

         - Note the **NAME** of the Pod that has an error
         - Run ``kubectl describe pods <POD NAME> -n metallb-system``
         - Run ``kubectl logs pod <POD NAME> -n metallb-system``

#. Refer to :ref:`clusterdetails` and note the IP range provided for **Karbon Network for MetalLB**.

   .. figure:: images/35.png

   Before **MetalLB** can be used, we need to provide a **ConfigMap** file that defines the IP address pool available for assignment to services.

#. Open **Visual Studio Code** in your **USER**\ *##*\ **-WinToolsVM** VM.

#. Select **File > New File** and paste the following into the blank file:

   .. code-block:: yaml

     apiVersion: v1
     kind: ConfigMap
     metadata:
       namespace: metallb-system
       name: config
     data:
       config: |
         address-pools:
         - name: metal-lb-ip-space
           protocol: layer2
           addresses:
           - <START IP RANGE>-<END IP RANGE>

#. Replace **<START IP RANGE>-<END IP RANGE>** with *your* **Karbon Network for MetalLB** values.

   .. raw:: html

      <BR><font color="#FF0000"><strong> Make 100% sure you are using only YOUR 2 assigned IP addresses otherwise you could cause unexpected issues for others sharing your cluster. Be kind.</strong></font>

   .. figure:: images/36.png

   Note the **namespace** metadata provided in the manifest, this is how Kubernetes understands the relationship between the configuration file and the Pods we installed earlier in the exercise.

#. Save the file as **metallb-config.yaml** in your **Downloads** folder.

   .. figure:: images/37.png

#. Return to **PowerShell** and run ``kubectl apply -f metallb-config.yaml`` to apply your configuration file.

   Your Karbon cluster can now provide Kubernetes **LoadBalancer** services similar to public cloud providers. We'll take advantage of this in the next exercise to expose our **Ingress Controller** to allow traffic into the cluster.

Deploying An Ingress Controller
+++++++++++++++++++++++++++++++

There are `many open source and commercial Ingress Controllers <https://kubernetes.io/docs/concepts/services-networking/ingress-controllers/>`_ that can be used with Kubernetes. In this exercise, we will deploy the open source variant of `Traefik <https://traefik.io/>`_ to route inbound network traffic.

#. In **PowerShell**, run the following commands:

   .. code-block:: bash

      kubectl apply -f https://raw.githubusercontent.com/nutanixworkshops/gts21/master/karbon/yaml%20files/01-traefik-CRD.yaml
      kubectl apply -f https://raw.githubusercontent.com/nutanixworkshops/gts21/master/karbon/yaml%20files/02-traefik-svc.yaml
      kubectl apply -f https://raw.githubusercontent.com/nutanixworkshops/gts21/master/karbon/yaml%20files/03-traefik-Deployment.yaml

   .. figure:: images/38.png

   Applying these manifests does the following:

   - Create a **Custom Resource Definition** (CRD) which defines RBAC capabilities for **Traefik**. CRDs `extend the API of Kubernetes <https://kubernetes.io/docs/concepts/extend-kubernetes/api-extension/custom-resources/>`_ with specific definitions.
   - Create a service of the Type **LoadBalancer** (using **MetalLB**) to expose the **Traefik** web interface on Port 8080.
   - Create the Pods for Traefik

   .. note::

      If interested, you can open the YAML manifests for any of these files using the URL in the ``kubectl apply`` commands.

#. Run ``kubectl get svc`` to list advertised services on the cluster.

   .. figure:: images/39.png

   You should see one of your **MetalLB** IPs assigned as the **EXTERNAL-IP** for **Traefik**.

   .. note::

      If your **EXTERNAL-IP** is listed as **Pending**, this indicates an issue with your **MetalLB ConfigMap** file.

      - Run ``kubectl describe configmap config -n metallb-system`` to verify your IP addresses are correct
      - Fix your **metallb-config.yaml** file and run ``kubectl apply -f metallb-config.yaml`` again

#. Open **Google Chrome** in your **USER**\ *##*\ **-WinToolsVM** VM, browse to \http://*<TRAEFIK-EXTERNAL-IP>*:8080.

   .. figure:: images/40.png

   Before we move on to deploying our Fiesta application on the Karbon cluster and exposing it to our external network using **MetalLB** and **Traefik**, let's look at two different options for providing informational dashboard visualization of the workloads running on our Kubernetes cluster.

Using Dashboards
++++++++++++++++

As we saw in :ref:`karbon_environment_setup`, the Karbon dashboard currently provides us with information about the infrastructure that makes up our cluster, but doesn't provide any insight into our Services or Pods.

There are approximately as many Kubernetes dashboard solutions as there are stars in the sky, so we'll narrow our focus to the official **Kubernetes Dashboard**, and **Lens**.

Kubernetes Dashboard
....................

For the installation and exposure of this dashboard we are going to use the Load Balancer so we can access it even when Traefik, the ingress controller has some issues. This is not the most secure way of working, as we can do a lot from the dashboard with respect to manipulating the environment.

#. Run ``kubectl apply -f https://raw.githubusercontent.com/nutanixworkshops/gts21/master/karbon/yaml%20files/05-k8s-dashboard.yaml`` to install the **Kubernetes Dashboard**.

#. Run ``kubectl get svc -n kubernetes-dashboard`` to get the **EXTERNAL-IP** value of the **kubernetes-dashboard** service.

   .. figure:: images/41.png

#. Open \https://*<KUBERNETES-DASHBOARD-EXTERNAL-IP>* in **Google Chrome**. Ignore the certification warning.

#. Select **Kubeconfig**.

#. Click **...** and select the **USER**\ *##*\ **-karbon-kubectl.cfg** file you previously downloaded from Karbon.

   .. figure:: images/42.png

#. Click **Sign in**.

   .. figure:: images/43.png

   You can now browse around the built-in Kubernetes dashboard. Observe that while this UI provides some helpful visualizations, it's clearly not intended for managing your Kubernetes cluster.

   Click **Cluster > Persistent Volumes** and see if you recognize anything - we'll make use of this persistent storage attached to your Kubernetes cluster via Nutanix Volumes in a later exercise!

.. _lens:

Lens
....

Rather than running on the Kubernetes cluster, **Lens** can be installed on a Windows, Linux, or macOS host and communicate with your cluster via API.

#. In your **USER**\ *##*\ **-WinToolsVM** VM, open **Lens** in the **Tools** folder on the desktop.

   .. note::

      Lens is a quick, 1 step installation process - but it's also a 200MB download, and I value you're time. *High five!*

#. Click **+** to add your cluster.

#. Click :fa:`folder` and browse to your **USER**\ *##*\ **-karbon-kubectl.cfg** file.

   .. figure:: images/44.png

#. Click **Add cluster**.

   Similar to the **Kubernetes Dashboard**, **Lens** provides you with (arguably better looking) visualizations of cluster health and performance.

   .. figure:: images/46.png

#. Under **Workloads**, click **Pods** and select your **Traefik** Pod.

   .. figure:: images/45.png

   **Lens** will give you per Pod configuration, performance, and logs, as well as the ability to open a terminal session into that specific Pod to execute commands.

   ..   #. Click **Apps**.

      .. figure:: images/47.png

      **Lens** provides a GUI for **Helm**, a popular command line package management tool for Kubernetes, making it easy for users to deploy new services. *This might be useful later!*

   .. raw:: html

       <H1><font color="#B0D235"><center>Congratulations!</center></font></H1>

So far you have provisioned a Kubernetes cluster with Karbon, added the necessary network services to provide production level access to services from external networks, and can easily visualize operations within the cluster.

In the next exercise we will provision the **Fiesta** application as a Kubernetes service.
