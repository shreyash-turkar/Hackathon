import smbprotocol
import scapy
import ldap3
import os
from ldap3 import Server, Connection
from termcolor import cprint
from colorama import init
import subprocess
import win32security
import smbclient
from smbprotocol.connection import Connection, Dialects
import uuid

# Define the server and port to check
server = '10.0.32.239'
port = 445
ldap_port = 443
ldap_username = 'RUBRIK-LAB\\administrator'
ldap_password = 'scaledata!@34'

# try:
    # connection = Connection(uuid.uuid4(), server, port)
    # connection.connect(Dialects.SMB_3_0_2)
    # print('SMB is enabled')
# except Exception as e:
    # print('SMB is disabled:', e)

init()
result = subprocess.getoutput('python getdc.py -d rubrik-lab.com -f host')
domain_controllers = result.strip(' ').split('.\n')

# Print the list of domain controllers
# print("\n*****************List of domain Controllers found:************************")
# for entry in domain_controllers:
    # print(entry)
    
print("\n*****************   Ping check for DCs    ************************\n")
for entry in domain_controllers:
    if entry.endswith('.'):
        entry = entry[:-1]
    if ' ' in entry:
        entry = entry.split(' ')[1]
    result = subprocess.getoutput('ping -n 1 ' + entry)
    if 'Packets: Sent = 1, Received = 1, Lost = 0 (0% loss)' in result:
        print(entry + ": ", end='')
        cprint('passed', 'green')
    else:
        print(entry + ": ", end='')
        cprint('failed','red')
        
print("\n************   authentication check for DCs  *********************\n")

for entry in domain_controllers:
    if entry.endswith('.'):
        entry = entry[:-1]
    if ' ' in entry:
        entry = entry.split(' ')[1]
    ldap_server = entry
    # Define the connection to the LDAP server
    server = ldap3.Server(entry)

    # Authenticate with the server using the provided credentials
    try:
        conn = ldap3.Connection(server, user=ldap_username, password=ldap_password, auto_bind=True)
        print(entry + ": ", end='')
        cprint('passed', 'green')
        conn.unbind()
    except Exception as e:
        print(entry + ": ", end='')
        cprint('failed','red')




    