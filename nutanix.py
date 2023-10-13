import requests
from requests.auth import HTTPBasicAuth
import re
from termcolor import cprint

url = "https://nutanix-01.stor.rubrik.com:9440/api/nutanix/v3/clusters/list"


requests.packages.urllib3.disable_warnings()

# Set the username and password
username = "admin"
password = "Rubrik@123"

auth = HTTPBasicAuth(username, password)

# Create a dictionary with the credentials
credentials = {"username": username, "password": password}

body = {
  "kind": "cluster",
  "length": 1,
  "offset": 0
}

reg1 = r'^5\.(20|19|18|17|16|15|11|10|9|8|6|5|1)$'
reg2 = r'^6\.(0|1|5)(\.([1-3]\.\d+))?$'
reg3 = r'^6\.(0|1|5)(\.([1-2]\.\d+))?$'
reg4 = r'^6\.(0|1)?$'

nutanixCompatibilityDict = {
    "9.0.1": [reg1,reg2],
    "9.0.0": [reg1,reg2],
    "8.1.3": [reg1,reg2],
    "8.1.2": [reg1,reg3],
    "8.1.1": [reg1,reg3],
    "8.1.0": [reg1,reg3],
    "8.0.3": [reg1,reg2],
    "8.0.1": [reg1,reg3],
    "8.0.0": [reg1,reg4],
    "7.0.4": [reg1,reg3],
    "7.0.3": [reg1,reg4],
    "7.0.3": [reg1,reg4],
}

def getAosVersion():
    response = requests.post(url,verify=False,auth=(username, password),json=body)

    if response.status_code == 200:
        # Authorization successful
        # print(response.json()['entities'][0]['spec']['name'])
        return response.json()['entities'][0]['spec']['resources']['config']['software_map']['NOS']['version']
    else:
        # print('Authentication failed')
        return -1

def match_version(input_str,pattern):
    if re.match(pattern, input_str):
        return True
    else:
        return False
    
def checkNutanixCompatibility(cdmVersion):
    if cdmVersion in nutanixCompatibilityDict:
        aosVersion = str(getAosVersion())
        check=False
        for s in nutanixCompatibilityDict[cdmVersion]:
            if match_version(aosVersion,s):
                check=True
                break
        
        if check:
            cprint('AOS version '+ aosVersion+' is qualified on CDM '+cdmVersion,'green')
        else:
            cprint('AOS version '+ aosVersion+' is not qualified on CDM '+cdmVersion,'red')

    else:
        cprint('Invalid cdm version is supplied','red')
    
checkNutanixCompatibility("9.0.1")#############################