# Author: shreyash.turkar@rubrik.com

from json import loads
from subprocess import run
from cprint import cprint

shouldBeRunningServices = ['vss', 'Rubrik Backup Service']


INDEXES = {
    'ENABLED': 2,
    'DIRECTION': 3,
    'LOCALIP': 6,
    'REMOTEIP': 7,
    'PROTOCOL': 8,
    'REMOTEPORT': 10,
    'ACTION': 12
}

def getFirewallRuleForPort(port):
    """
    Return all firewall rules associated with the given port.
    """
    cprint.info('Checking rule for port: %s' % port)
    firewallRuleCmd = ("powershell -command netsh advfirewall firewall show rule name=all | select-string -pattern \"(LocalPort.*.%s)\" -context 9,4" % port).split()
    portFirewallOuput = run(firewallRuleCmd, capture_output=True)
    retRules = []
    for rawRule in str(portFirewallOuput.stdout).split('Rule Name:'):
        try:
            rule = str(rawRule).split('\\r\\n')
            if len(rule) < 14:
                continue
            aRule = {
                'NAME': rule[0].strip(),
                'PORT': rule[9].split()[2]
            }
            for name, index in INDEXES.items():
                aRule[name] = rule[index].split()[1]
            retRules.append(aRule)
        except:
            cprint.warn('Error parsing rule for port: %s' % port)
            pass
    return retRules

def checkRuleAgainstConfig(rule, config):
    """
    Checks a firewall rule against the given config.
    """
    if rule['ENABLED'] == 'No':
        cprint.ok('Skipping check on disabled rule: %s' % rule['NAME'])
        return

    if rule['PORT'] != str(config['port']):
        cprint('OOPs')
        return
    
    if rule['PROTOCOL'].lower() != config['protocol'].lower():
        return
    
    if rule['REMOTEIP'].lower() != 'any' and rule['ACTION'].lower() == 'block':
        cprint.warn(
            'IP: %s is blocked under rule: %s.\n'
            'Please check if this is a CDM IP.\n'
            'This port is needed to: %s'
            % (rule['REMOTEIP'], rule['NAME'], config['justification']))
    
    if rule['REMOTEIP'].lower() == 'any' and rule['ACTION'].lower() == 'block':
        cprint.err(
            'Rule: %s is blocking access to port: %s from remote. '
            'This port is needed to: %s'
            % (rule['NAME'], config['port'], config['justification']))


def checkStatusOfservice(serviceName):
    """
    Checks if a service is running.  
    """
    command = 'powershell -command Get-Service \'%s\'' % serviceName
    output = run(command, capture_output=True)
    if output.stderr:
        cprint.err('Error occured while checking %s service status: %s' % (serviceName, output.stderr))
        return
    
    status = None
    try:
        status = str(output.stdout).split('\\r\\n')[3].split()[0]
    except Exception as e:
        cprint.err('Error occured while parsing %s service status: %s' % (serviceName, e))
        return

    if status.lower() != 'running':
        cprint.err('%s is not running' % serviceName)

portsConfigFile = open("./portConfig.json")
portConfig = loads(portsConfigFile.read())
portsConfigFile.close()

outBoundPorts = portConfig.get('outbound')
inBoundPorts = portConfig.get('inbound')
allPorts = outBoundPorts + inBoundPorts

for config in allPorts:
    port = config.get('port')
    rules = getFirewallRuleForPort(port)
    for rule in rules:
        checkRuleAgainstConfig(rule, config)

for serviceName in shouldBeRunningServices:
    cprint.info('Checking status of service: %s' % serviceName)
    checkStatusOfservice(serviceName)