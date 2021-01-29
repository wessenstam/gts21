.. _snowdeploy:

--------------------
Deploying ServiceNow
--------------------

Intro

Use case:

Have on-prem environment with limited capacity
Looking at add self-service for end users, with ability to easily add capacity
Need control over approvals
Want an active/active approach with automatic DR between sites
Portability of security between sites
interested in autonomous DC operations with approval control



Review Add Clusters to PC (or as separate AZ)
create simple flow isolation policy, enable - tag env:dev to VM, tag env:prod to webserver, tag both to MSSQL DB
create simple protection policy (both ways)
upload and configure Calm BP (or create from scratch), assign categories for Flow/DR/User
tlak to ability to do native self-service and introduce snow
review snow setup - MID server, plugins, plugin config, approval workflow, user assignments, lack of LDAP
create snow catalog item
log in as operator#, launch BP
approve request
duplicate operator role, basic VM access, assign operator#
log in as operator to access VM console/stats
verify flow policy and replication
set up user alert policy for VM, set up playbook to send alert
trigger alert with stress
look for alert in SNOW, view CMDB dashboard
build playbook for webhook, create snow action/flow
re-trigger alert and verify added memory
migrate VM back to on-prem environment, verify flow policy followed - reason being for latency to on-prem applications

talk about other ways this could be extended - using playbooks or SNOW to dynamically grow/shrink clusters environment with MCM; reporting on overprovisioned or orphaned VMs in AWS environment
Create Calm project,





Requesting Developer Instance
+++++++++++++++++++++++++++++

Configuring Developer Instance
++++++++++++++++++++++++++++++

Reviewing Configuration
+++++++++++++++++++++++

Look at config settings, synced Calm data

Create Catalog Item
+++++++++++++++++++

(If you want to build your own Calm blueprint, go here...)

Otherwise, use provided CentOS Blueprint

https://www.nutanix.dev/2020/04/27/installing-and-configuring-the-nutanix-calm-plugin-for-servicenow/

Stress -
