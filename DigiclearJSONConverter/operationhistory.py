"""
Get all the information from the json file + API calls to fill some blanks
"""
import json 
from datetime import datetime
from pathlib import Path

class OperationHistory():
    
    def __init__(self, jsonfilepath, digiclearconnection):
        """
        This class holds the operation history data. 
        It take a json history file as input, and a digiclearconnection object to 
        make some API calls to complete information. 
        The information to pass to the report renderer (pdf or docx) is stored in 
        the `report_dict` dictionnary.

        Parameters
        ----------
        jsonfilepath : str
            Path to the file to be converted.
        digiclearconnection : digiclearconnection object
            digiclearconnection object for the API calls.

        Returns
        -------
        None.

        """
        self.jsonfilepath = jsonfilepath
        self.dcc = digiclearconnection

        titleParams = Path(jsonfilepath).name.split('.json')[0].split('_')
        titleText = f'{titleParams[0]} history'
        subtitleText = f'Downloaded {titleParams[2]} at {titleParams[3]}'
        self.report_dict = {'Title': titleText,
                            'Subtitle': subtitleText}
        
        self.GetOperationsData()
        self.SortOperations()
        
        self.sampleId = self.op_list[0]['operation-samples'][0]['sampleId']
        self.GetSampleParents()
        self.report_dict['Parents'] = self.ParentList
        
    def GetSampleParent(self, sampleId):
        """
        Get the parent of a sample identified by its sampleId

        Parameters
        ----------
        sampleId : str
            sampleId in the digiclear DB.

        Returns
        -------
        parentInfo : 2-list or None
            2-List of the parent sample Id and name. Returns None if the sample has no parent.

        """
        parent_json = json.loads(self.dcc.s.get(self.dcc.base_api_url+f'getSampleParents?id={sampleId}').text)
        if len(parent_json) == 1:
            parentId = parent_json[0]['id']
            parentName = self.GetSampleName(parentId)
            parentInfo = [parentId, parentName]
            return parentInfo
        else:
            return None
    def GetSampleParents(self):
        """
        Get all the sample parents recursively for the current sample.

        Returns
        -------
        ParentList : list
            List of 2-lists of couples [sampleId, sampleName] of all parent samples.

        """
        self.ParentList = []
        currentId = self.sampleId
        currentName = self.GetSampleName(self.sampleId)
        currentInfo = [currentId, currentName]
        while currentInfo is not None:
            currentInfo = self.GetSampleParent(currentInfo[0])
            if currentInfo is not None:
                self.ParentList.append(currentInfo)
        return self.ParentList
    
    def GetSampleName(self, sampleId):
        """
        API request to get the sample name from the sampleId.

        Parameters
        ----------
        sampleId : str
            sampleId in the digiclear DB.

        Returns
        -------
        sampleName : str
            Sample name.

        """
        sample_info = json.loads(self.dcc.s.get(self.dcc.base_api_url+f'getSample?id={sampleId}').text)
        sampleName = sample_info['name']
        return sampleName
    def GetProjectName(self, projectId):
        """
        API request to get the project name from the projectId.

        Parameters
        ----------
        projectId : str
            projectId in the digiclear DB.

        Returns
        -------
        projectName : str
            Project name.

        """
        project_info = json.loads(self.dcc.s.get(self.dcc.base_api_url+f'getProject?id={projectId}').text)
        projectName = project_info['name']
        return projectName
    def GetMachineName(self, machineId):
        """
        API request to get the machine name from the machineId.

        Parameters
        ----------
        machineId : str
            machineId in the digiclear DB.

        Returns
        -------
        machineName : str
            Machine name.

        """
        machine_info = json.loads(self.dcc.s.get(self.dcc.base_api_url+f'getMachine?id={machineId}').text)
        machineName = machine_info['name']
        return machineName


    def GetOperationsData(self):
        """
        Load the operation data from the json file to a dictionnary and fill 
        some missing information, such as retreiving a machine name from its id. 

        Returns
        -------
        op_list : list
            List of the operations. Each operation is a dictionnary with keys from 
            the machine template. 

        """
        ### not possible to find a single user through api so load them all up and use later
        all_users = json.loads(self.dcc.s.get(self.dcc.base_api_url+'getUsers').text)
        
        f = open(self.jsonfilepath)
        
        op_list_loc = json.load(f)['operations'] #### local copy of list of all operations
        
        for op_dict in op_list_loc: 
            ######## machine/process relevant part
            ### add the machine name 
            machineId = op_dict['machineId']
            machineName = self.GetMachineName(machineId)
            
            ### add the operator name
            operatorName = [e['fullName'] for e in all_users if e['userId']==op_dict['userId']][0]
            
            ######## sample relevant part
            operationsSamples = op_dict['operation-samples'][0]
            projectId = operationsSamples['projectId']
            sampleId = operationsSamples['sampleId']
            projectName = self.GetProjectName(projectId)
            sampleName = self.GetSampleName(sampleId)
            
            ######## add to the local copy of the operation dict 
            op_dict['machineName'] = machineName
            op_dict['operatorName'] = operatorName
            op_dict['projectName'] = projectName
            op_dict['sampleName'] = sampleName
        
        f.close()
        
        self.op_list = op_list_loc
        
        return self.op_list

    def SortOperations(self):
        """
        Sorts the operations by date, in chronological order.

        Returns
        -------
        None.

        """
        op_dates = []
        for op in self.op_list:
            op_dt = datetime.strptime(op['operationDate'], '%Y-%m-%d %H:%M:%S')
            op_dates.append(op_dt)

        ### from https://stackoverflow.com/questions/6618515/sorting-list-based-on-values-from-another-list
        ### sort the operations by operation date
        sorted_operations = [op for _, op in sorted(zip(op_dates, self.op_list))]
        self.report_dict['Operations'] = sorted_operations
        

