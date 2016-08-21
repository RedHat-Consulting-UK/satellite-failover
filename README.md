# satellite-failover

## Description

Python script which allows Red Hat Satellite 6 clients either directly connect to a Red Hat Satellite 6 server or Capsule Server to fail over to another if the capsule or satellite server they are registered to dies.

The idea is to allow the client to fail over automatically instead of relying on the Satellite 6 infrastructure to be resilient.

Authors: Calvin Hartwell (cjh@redhat.com).

## The script has the following planned functionality:

 * Ability to register and automatically subscribe from a predefined list of Satellite 6/Capsule servers.
 * Ability to set failure detection conditions for the Satellite 6/Capsule Servers.
 * Ability to specify priority/weight of servers from the predefined list and which services should be configured (Puppet may not be used for example).
 * Ability to log errors if unable to connect to any Satellite 6/Capsule servers.
 * Ability to failover goferd, puppet client and subscription manager (RHSM) to a new Satellite 6/Capsule Server.
 * Ability to fallover to the Red Hat CDN if all capsules or satellite 6 servers are down and it is accessible (useful for cloud environments)
 * Automatically downloads, installs and updates the Katello CA RPM from a selected Satellite 6/Capsule server.
 * Ability to run the script as a daemon, one-shot execution or use the tool through CRON.
 * Script will eventually be packaged as an RPM and a Puppet module/Ansible Playbook will be provided for deploying the agent config.


 ## How to use the script
 ## Script config file examples
 
