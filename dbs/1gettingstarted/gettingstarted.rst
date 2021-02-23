.. _getting_started:

---------------
Getting Started
---------------

This workshop will demonstrate precisely how utilizing Era in these environments grants BCDR functionality they were unable to realize previously.

Within each scenario, we'll open with the environment specifics, and (red/green both before and after?) what they are, and are not, able to do achieve today, contrasted by what Era can bring to these environments. Implementing Era in an afternoon quickly and easily make them robust and resilient, all without requiring a typical DBA skillset, and Nutanix support standing by their side should the need arise.

Random ideas
++++++++++++
[memes? pics? videos?]

Licensing implications

SQL Standard/Enterprise

Re-platforming - old OS/SQL

Good/better/best

Simple recovery mode -> Full

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

#. David Teague video

   - SQL - 2008 R2 -> 2019
   - Old DB & 2019 DB VM already registered

   - Go to old DB TM, authorize 2019 DB VM
   - Clone old DB to 2019 DB VM
   - Log catchup on cloned DB
   - 2008 Compatability mode. If testing successful, proceed.
   - Open TM for cloned DB, do snapshot or log catch-up
   - Asked David: If I snapshot and then stop old DB, isn't there a gap where data could be written? Wouldn't it be better to do read-only mode on old server to avoid this?
   - Refresh new DB
   - Unregister old DB in Era
   - Register new DB on 2019
   - Change recovery model of new DB on 2019 to Full
   - Time Machines -> DAM -> Add (backups to any registered Nutanix cluster)

Bonus Labs
++++++++++

- Monitoring Applications with Prism Ultimate
- Hammer DB
