"""
Simple script that looks for all Digiclear JSON files in a given directory 
(or the current directory) and converts them all to pdf.
Supply username and password in strings
"""

from DigiclearJSONConverter.digiclearconnection import DigiclearConnection
from DigiclearJSONConverter.operationhistory import OperationHistory
from DigiclearJSONConverter.pdfreport import PDFReport
from pathlib import Path
this_dir = Path(__file__).parent ## current directory where the file is

username = 'prenom.nom' ### your digiclear username
password = 'password' ### your digiclear password
digiclear_servername = 'remoteclear-lan' ## digiclear, remoteclear or remoteclear-lan


####### to run in the current directory
sourcedirectory = this_dir
####### to get json files from another directory
sourcedirectory = Path(r'directory_holding_json_files')

####### list json files matching the pattern
jsonfilelist = list(sourcedirectory.glob('*_history_*.json')) 

### connect to Digiclear
s = DigiclearConnection(digiclear_servername)
test = s.login(username, password, check_certificate=False) ## False for remoteclear-lan 
if not test:
    print('\n login failed \n')

### do the actual conversion
if len(jsonfilelist)>0:
    for jsonfilepath in jsonfilelist:
        outfilename = jsonfilepath.name.replace('json','pdf') ## output file name
        outfilepath = Path(jsonfilepath.parent, outfilename).__str__() ## output file path as str
        Operation_Dict = OperationHistory(jsonfilepath, digiclearconnection = s) ## get all info
        Report = PDFReport(Operation_Dict.report_dict, outfilepath) ## write to pdf

s.disconnect() ## close connection do digiclear
