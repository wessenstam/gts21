STAGING

Creating User:1 - User:10 category values (Prepend U1, U2, etc. to Blueprint apps)

Enable App Discovery

Import Fiesta App BP, spin up 7 copies
ERA compute profile 4 vcpu/6GB RAM
Era Domain profile NTNXLAB
Era AD auth, add SSP Operators group with all 3 roles
Add PE to Era
Create Era managed network 211-253 IP range
enable multi-cluster
Spin up 1 copy of source DB
register that DB server
Create software profile from that image

(AWS staging script) Add AWS PE to Era
(AWS staging script) Create Era managed network 210-253 IP range
(AWS staging script) replicate MSSQL software profile to AWS


USE CASE

User with single instance on-prem app (Fiesta webserver/MSSQL DB VM/extra DBs in it)
Customer wants to build in more resiliency for app
Register source DBs (Fiesta)
Use Era to provision AAG across on-prem (2 sync copies) and AWS (1 async copy) - SE would manually import data afterwards ~60 minutes

Register Sample DB from same source VM
Add AWS-Cluster to Sample.DB time machine data access management
Clone Sample.db to another single instance VM (provisioned on AWS)

Use pre-provisioned source DB to do hammer DB stuff

Once AAG is done, update Fiesta webserver to point to AAG VIP
Fail primary AAG VM, confirm web app still works
Fail remaining on-prem AAG VM, log into AWS copy and make active - potential for data loss, but still have up time, need to speak to other considerations for webserver level HA (replicas/load balancers)

Once sample.db clone is done, patch that VM
