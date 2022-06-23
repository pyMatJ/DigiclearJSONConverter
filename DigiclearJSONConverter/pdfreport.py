"""
Generate a pdf report from a dictionnary
"""
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.colors import Color
from lxml.html import document_fromstring

class PDFReport():
    
    def __init__(self, report_dict, outfilepath):
        """
        Generate the PDF report from the `report_dict` generated by the 
        operationhistory class. 
        The report is generated by creating a list of flowables that are added 
        in chronological order, starting from title, subtitle and then ordered list 
        of operations. 

        Parameters
        ----------
        report_dict : dictionnary
            Dictionnary generated from the json and API calls by the operationhistory module.
        outfilepath : str
            Path to the pdf report file to generate.

        Returns
        -------
        None.

        """
        self.report_dict = report_dict
        
        
        self.titleText = self.report_dict['Title']
        self.subtitleText = self.report_dict['Subtitle']
        self.flowables = []
        
        self.outfilepath = outfilepath
        self.doc = SimpleDocTemplate(outfilepath,pagesize=letter,
                                     rightMargin=72,leftMargin=72,
                                     topMargin=72,bottomMargin=18)
        
        ## uninteresting fields not to be displayed
        self.discardFields = ['machineId', 'userId', 'inheritorId', 'id', 
                              'projectId', 'sampleId',
                              'machineName', 'operatorName', 'sampleName', 'projectName', 
                              'operationDate', 'operation-samples']

        self.MakeHeadersFlowables()
        
        self.MakeDescriptionFlowable()
        
        self.MakeParentsFloables()
        
        self.MakeOperationFlowables()
        
        
        self.BuildDoc()


    def MakeHeadersFlowables(self):
        """
        Format and adds the headers to the list of flowables. 
        """
        ## paragraph styles
        psHeaderText = ParagraphStyle('Hed0', fontSize=20, alignment=TA_CENTER, borderWidth=3)
        psSubHeaderText = ParagraphStyle('Hed1', fontSize=18, alignment=TA_CENTER, borderWidth=3)
        
        ## paragraphs
        pgHeader = Paragraph(self.titleText, psHeaderText)
        pgSubHeader = Paragraph(self.subtitleText, psSubHeaderText)
        
        ## append to flowable list
        self.flowables.append(pgHeader)
        self.flowables.append(Spacer(1,psHeaderText.fontSize))
        self.flowables.append(pgSubHeader)
        self.flowables.append(Spacer(1,psSubHeaderText.fontSize))
    
    def MakeDescriptionFlowable(self):
        """
        Formats the flowable from the 'Description' field of the report_dict.
        This corresponds to the description of the sample in the sample/settings tab in digiclear.

        Returns
        -------
        None.

        """
        if len(self.report_dict['Description'])>0:
            ## paragraph style
            psDescriptionText = ParagraphStyle('Hed2', fontSize=12, alignment=TA_LEFT, borderWidth=3)
            ## paragraph
            pgDescription = Paragraph(self.report_dict['Description'], psDescriptionText)
            
            ## append to flowable list
            self.flowables.append(pgDescription)
            self.flowables.append(Spacer(1,psDescriptionText.fontSize))
    
    def MakeParentsFloables(self):
        """
        Makes a table of all the parents of a sample found recursively from operationhistory.GetSampleParents

        Returns
        -------
        None.

        """
        if len(self.report_dict['Parents'])>0:
            parentsData = [['Parent Samples', '']]
            for par_i in self.report_dict['Parents']:
            # for par_i in Operation_Dict.report_dict['Parents']:
                parentsData.append(['', par_i[1]])
            tblstyle = TableStyle([
                ('LINEBELOW', (0,0), (-1,0), 1, Color(0, 0, 0)),
                ])
            parentsTable = Table(parentsData, colWidths='*', spaceBefore=10)
        
            tblstyle = TableStyle([
                ('LINEBELOW', (0,0), (-1,0), 1, Color(0, 0, 0)),
                ])
            parentsTable.setStyle(tblstyle)
            self.flowables.append(parentsTable)
            
    def HTMLCommentFormatting(self, s):
        """
        Formats the comments fields from the json into reportlab-readable strings.
        Initially they are in a html-like syntax

        Parameters
        ----------
        s : str
            String retrieved from the json file in a comment field. Usually in 
            html-like format '<p> some text <br /> more text </p>'

        Returns
        -------
        text : str
            Text formatted in string stripped of HTML markers and with ``\\n``
            for newline characters

        """
        doc = document_fromstring(s)
        for br in doc.xpath("*//br"):
            ## element.tail returns the text between tags https://lxml.de/tutorial.html ctrl+f tail
            br.tail = "\n" + br.tail if br.tail else "\n"
        text = doc.text_content()
        return text
        
    def MakeOperationFlowables(self):
        """
        Loops through the list of operation and adds them in the flowables as tables.
        Each operation consists of two tables, one for the machine settings, the other one 
        for the samples settings. 
        """
        
        ### loop through all operations
        for op in self.report_dict['Operations']:
            
            ### header of the operation is the machine name
            machineName = op['machineName']
            
            operatorName = op['operatorName']
            operationDate = op['operationDate']
            data = [
                    [machineName, operationDate],
                    ['operator', operatorName]
                    ]
            
            opHeaderStyle = TableStyle([
                ('BACKGROUND', (0,0), (-1,0), Color(85/255, 153/255, 255/255)), ## colored header
                ('ALIGN', (0,0), (0,0), 'LEFT'),
                ('ALIGN', (1,0), (-1,-1), 'RIGHT'),
                ])
            opHeadTable = Table(data, colWidths='*', spaceBefore=10)
            opHeadTable.setStyle(opHeaderStyle)
            self.flowables.append(opHeadTable)
        
            ### list all operation data
            operationData = []
            for param in op:
                if param not in self.discardFields:
                    if 'Comment' in param and len(op[param])>1: 
                        ## 'Comment' in field name indicates that there might be html text to cleanup
                        paramText = self.HTMLCommentFormatting(op[param]) ## correct formatting
                    else:
                        paramText = op[param]
                    operationData.append([param, paramText])
            operationTable = Table(operationData, colWidths='*')
            opTableStyle = TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP')
                ])
            operationTable.setStyle(opTableStyle)
            self.flowables.append(operationTable)
            
            
            #### list all sample-specific data
            sampleData = [['Sample Data', '']]
            sampleData.append(['Project Name', op['projectName']])
            op_sample = op['operation-samples'][0]
            for param in op_sample:
                if param not in self.discardFields:
                    if 'Comment' in param and len(op_sample[param])>1:
                        ## 'Comment' in field name indicates that there might be html text to cleanup
                        paramText = self.HTMLCommentFormatting(op_sample[param]) ## correct formatting
                    else:
                        paramText = op_sample[param]
                    sampleData.append([param, paramText])
            sampleTable = Table(sampleData, colWidths='*', spaceBefore=10)
        
            tblstyle = TableStyle([
                ('LINEBELOW', (0,0), (-1,0), 1, Color(0, 0, 0)),
                ('VALIGN', (0,0), (-1,-1), 'TOP')
                ])
            sampleTable.setStyle(tblstyle)
            self.flowables.append(sampleTable)
            
        
    def BuildDoc(self):
        self.doc.build(self.flowables)