.. _getting_started:

---------------
Getting Started
---------------

This workshop will demonstrate precisely how utilizing Era in these environments grants BCDR functionality they were unable to realize previously.

Within each scenario, we'll open with the environment specifics, and (red/green both before and after?) what they are, and are not, able to do achieve today, contrasted by what Era can bring to these environments. Implementing Era in an afternoon quickly and easily make them robust and resilient, all without requiring a typical DBA skillset, and Nutanix support standing by their side should the need arise.

[memes? pics? videos?]

Scenarios
+++++++++

#. One name

   - Single instance on-prem app (Fiesta webserver/MSSQL DB VM/extra DBs in it)
   - Customer wants to build in more resiliency for app
   - Register source DBs (Fiesta)
   - Use Era to provision AAG across on-prem (2 sync copies) and AWS (1 async copy) - SE would manually import data afterwards ~60 minutes

#. Two name

   - Register Sample DB from same source VM
   - Add AWS-Cluster to Sample.DB time machine data access management
   - Clone Sample.db to another single instance VM (provisioned on AWS)

#. Three name

   - Use pre-provisioned source DB to do hammer DB stuff

#. Four name

   - Once AAG is done, update Fiesta webserver to point to AAG VIP
   - Fail primary AAG VM, confirm web app still works
   - Fail remaining on-prem AAG VM, log into AWS copy and make active - potential for data loss, but still have up time, need to speak to other considerations for webserver level HA (replicas/load balancers)

#. Five name

   - Once sample.db clone is done, patch that VM

Bonus Labs
++++++++++

- Monitoring Applications with Prism Ultimate
- Hammer DB
