import platform
# import cprint
from termcolor import cprint

hypervCompatibilityDict = {
    "4.2.0": 2016,
    "5.2.0": 2019,
    "5.2.1": 2019,
    "5.3.0": 2019,
    "6.0": 2019,
    "6.0.1": 2019,
    "7.0": 2019,
}

def checkHyperVCompatibility(cdmVersion):
    
    if cdmVersion in hypervCompatibilityDict:
        systemVersion = platform.release()
        systemVersionInt = int(systemVersion[:4])
        
        if systemVersionInt < hypervCompatibilityDict[cdmVersion]:
            cprint('CDM version '+cdmVersion+' does not support Hyper-V '+systemVersion,'red')
        else:
            cprint('Hyper-V version '+systemVersion+' is compatible with CDM '+cdmVersion,'green')
    else:
        cprint('Invalid cdm version is supplied','red')


checkHyperVCompatibility("4.2.0")######################################

# print(platform.platform())
# print(platform.system())
# print(platform.release())
# print(platform.version())
# print(platform.version().split('.')[2]) 
# print(platform.machine())
# cprint('passed', 'green')