#!/usr/bin/python
from datetime import datetime
from optparse import OptionParser
from ConfigParser import SafeConfigParser

import yaml
import subprocess
import re


error_colors = {
    'HEADER': '\033[95m',
    'OKBLUE': '\033[94m',
    'OKGREEN': '\033[92m',
    'WARNING': '\033[93m',
    'FAIL': '\033[91m',
    'ENDC': '\033[0m',
}

def print_error(msg):
    print "[%sERROR%s], [%s], EXITING: [%s] failed to execute properly." % (error_colors['FAIL'], error_colors['ENDC'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg)


def print_warning(msg):
    print "[%sWARNING%s], [%s], NON-FATAL: [%s] failed to execute properly." % (error_colors['WARNING'], error_colors['ENDC'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg)


def print_success(msg):
    print "[%sSUCCESS%s], [%s], [%s], completed successfully." % (error_colors['OKGREEN'], error_colors['ENDC'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg)


def print_running(msg):
    print "[%sRUNNING%s], [%s], [%s] " % (error_colors['OKBLUE'], error_colors['ENDC'], datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg)


def print_generic(msg):
    print "[NOTIFICATION], [%s], [%s] " % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), msg)


def exec_failok(command):
    print_running(command)
    output = commands.getstatusoutput(command)
    retcode = output[0]
    if retcode != 0:
        print_warning(command)
    print output[1]
    print ""
    return retcode


def exec_failexit(command):
    print_running(command)
    output = commands.getstatusoutput(command)
    retcode = output[0]
    if retcode != 0:
        print_error(command)
        print output[1]
        sys.exit(retcode)
    print output[1]
    print_success(command)
    print ""


def parse_failover_config(configfile):
    print_generic("Attempting to parse failover config")
    with open(configfile, 'r') as stream:
        try:
            cfg=yaml.load(stream)
        except yaml.YAMLError as exc:
            print_error("unable to read %s: %s"%(configfile,exc))



    for i in range(0,len(cfg['failover']['capsules'])):
        if not validatecapsule(cfg['failover']['capsules'][i]):
            print_warning("capsule '%s' failed validation, ignoring"%(cfg['failover']['capsules'][i].get("name","unknown")))
            del cfg['failover']['capsules'][i]

    return cfg


def validatecapsule(capsule):
    ## check required options
    if capsule.get("name") == None:
        print_warning("name attribute is required")
        return False

    ## set some values to defaults if not present
    if capsule.get("hostname") == None:
        capsule['hostname']=capsule['name']

    if capsule.get("priority") == None:
        capsule['priority']=1

    return True


def failover(configdir,config):
    consumer = configdir + "/" + config['name'] +"/katello-rhsm-consumer"
    print_running(consumer)
    #code = os.system(consumer)
    #if code != 0:
    #    print_error("unable to reconfigure to use %s"%(config['name']))

    gofer="systemctl restart goferd"
    print_running(gofer)
    #code = os.system("systemctl restart goferd")
    


def getcurrentcapsule():
    hostname=None
    try:
        proc = subprocess.Popen(['subscription-manager','config','--list'],stdout=subprocess.PIPE)
        for line in proc.stdout.readlines():
            #print "line=%s"%line
            m=re.match(r" *hostname *= *\[?([\.\w]+)\]?",line)
            if m:
                hostname = m.group(1)
                break
    except Exception,e:
        print_error("failed to get current capsule %s"%e)
    
    return hostname

def getnextcapsule(currenthostname,config):
    nextcapsule = {}
    for i in config['failover']['capsules']:
        if i['hostname'] == currenthostname:
            next
        if i['priority'] > nextcapsule.get('priority',0):
            nextcapsule=i

    print "next:"
    print nextcapsule
    return nextcapsule

# Entry point
def main():
    
    parser = OptionParser()
    parser.add_option("-c", "--config", dest="failover_config", help="Custom path to failover config yaml file", metavar="failover_config", default="/etc/satellite-failover.cfg")
    (opt,args) = parser.parse_args()


    config=parse_failover_config(opt.failover_config)
    
    print config
    #print config['failover']['capsules']

    currentcapsule = getcurrentcapsule()

    capsuleconfig = getnextcapsule(currentcapsule,config) 

    failover(config['failover']['config'], capsuleconfig)



if __name__ == "__main__":
    main()
