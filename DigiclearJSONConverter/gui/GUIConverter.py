# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 08:19:57 2022

@author: mathieu
"""

from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from pathlib import Path

from DigiclearJSONConverter.digiclearconnection import DigiclearConnection
from DigiclearJSONConverter.operationhistory import OperationHistory
from DigiclearJSONConverter.pdfreport import PDFReport


def main():
    """
    Run the GUI application

    Returns
    -------
    None.

    """
    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()
        #print('QApplication instance already exists: %s' % str(app))
        
    win = MainWindow()
    win.setWindowTitle('Digiclear JSON converter')
    win.show()
    sys.exit(app.exec_())
    
    
class MainWindow(QtWidgets.QMainWindow):
    
    def __init__(self):
        """
        Creates the main window holding everything. 
        
        Returns
        -------
        None.

        """
        super().__init__()
        
        self.convertButton = QtWidgets.QPushButton('Convert Files')
        self.convertButton.clicked.connect(self.convertButtonCallback)
        self.quitButton = QtWidgets.QPushButton('Quit')
        self.quitButton.clicked.connect(self.quitButtonCallback)
        self.loginField = QtWidgets.QLineEdit(placeholderText='login')
        self.passwordField = QtWidgets.QLineEdit(placeholderText='password')
        self.passwordField.setEchoMode(QtWidgets.QLineEdit.Password)
        self.serverField = QtWidgets.QComboBox()
        # self.serverField.addItems(['digiclear', 'remoteclear-lan', 'remoteclear']) ## test servers
        self.serverField.addItems(['digiclear'])
        self.FileManager = FileManager()
        self.FileManager.itemChanged.connect(self.FileManager.onClick)
        
        self._make_UI()
    
    def quitButtonCallback(self):
        QtWidgets.QApplication.quit()
        self.close()
        
    def convertButtonCallback(self):
        
        fileItemsList = self.FileManager.fileItems
        success = self.login()
        if success:
            for item in fileItemsList:
                jsonfilepath = item.filepath
                Operation_Dict = OperationHistory(jsonfilepath, digiclearconnection = self.session)
                if item.exportPDF:
                    outfilepath = jsonfilepath.replace('json','pdf')
                    print(f'\n Exporting {Path(outfilepath).name} to pdf \n')
                    Report = PDFReport(Operation_Dict.report_dict, outfilepath)
                if item.exportDocx:
                    print('\n Exporting docx will be supported later \n')
        self.logout()
    
    def login(self):
        username = self.loginField.text()
        password = self.passwordField.text()
        digiclear_servername = str(self.serverField.currentText())
        if digiclear_servername == 'remoteclear-lan':
            check_certificate = False ### remoteclear certificate does not match remoteclear-lan so we bypass checking it
        else:
            check_certificate = True

        self.session = DigiclearConnection(digiclear_servername)
        success = self.session.login(username, password, check_certificate) 
        return success
        
    def logout(self):
        self.session.disconnect()
        
        
    def _make_UI(self):
        width = 720
        height = 200
        layout = QtWidgets.QHBoxLayout()
        ## make a splitter to allow resizing plot region
        vSplit = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
       
        ## left panel is a simple VBox
        leftPanel = QtWidgets.QWidget() ## the left panel with all other widgets
        leftPanelLayout = QtWidgets.QVBoxLayout() ## left panel layout
        
        leftPanelLayout.addWidget(self.FileManager)
        leftPanel.setLayout(leftPanelLayout)
        
        rightPanel = QtWidgets.QWidget()
        rightPanelLayout = QtWidgets.QVBoxLayout() ## left panel layout
    
        ## Add widgets to the right panel layout in their proper positions
        rightPanelLayout.addWidget(self.convertButton)   # convert button goes top
        rightPanelLayout.addWidget(self.quitButton)  # quit button
        rightPanelLayout.addWidget(self.loginField) # login field
        rightPanelLayout.addWidget(self.passwordField) # login field
        rightPanelLayout.addWidget(self.serverField) # login field
        
        rightPanel.setLayout(rightPanelLayout)
        vSplit.addWidget(leftPanel)
        vSplit.addWidget(rightPanel)
        
        
        layout.addWidget(vSplit) 
        vSplit.setSizes((int(width*0.8), int(width*0.2)))
        w = QtWidgets.QWidget()
        w.setLayout(layout)
        
        self.setCentralWidget(w)
        self.resize(width, height)
        self.show()
        
        
class FileManager(QtWidgets.QTreeWidget):
    
    def __init__(self):
        """
        QTreeWidget handling the display of all files

        Returns
        -------
        None.

        """
        super().__init__()

        self.fileItems = []
        
        self.viewport().setAcceptDrops(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        
        self.setColumnCount(3)
        self.setColumnWidth(0,460)
        self.setColumnWidth(1,3)
        self.setColumnWidth(2,3)
        headerlabels = ['Filename', 'PDF', 'Docx']
        self.setHeaderLabels(headerlabels)
        self.root = self.invisibleRootItem()
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        
        ### Indicator text widget that disappears after first dropped file
        self.indicator = QtWidgets.QLabel('Drop JSON files here', parent = self)
        self.indicator.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents, True)
        indicatorfont = QtGui.QFont('Time',20)
        self.indicator.setFont(indicatorfont)
        self.indicator.setStyleSheet('color : gray')
        self.indicator.show()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls: ## check that the items are a file
            for url in event.mimeData().urls():
                if url.isLocalFile() and Path(url.toLocalFile()).suffix=='.json': ## only accept json files
                    event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls(): ## check that the items are a file
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
       if event.mimeData().hasUrls(): ## check that the items are a file
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
            for url in event.mimeData().urls():
                if url.isLocalFile() and Path(url.toLocalFile()).suffix=='.json': ## only accept json files
                    filepath = Path(url.toLocalFile()).__str__()
                    self.addFile(filepath) ## add the file to the list
                    self.indicator.hide() ## indicator no longer necessary
            
    def addFile(self, path):
        fileItem = FileItem(path)
        self.addTopLevelItem(fileItem) ## add the item to the QTreeWidget
        self.fileItems.append(fileItem) ## keep a reference in the list
        
    def onClick(self, item, column):
        if column==1: ## export PDF selector
            if item.checkState(column)==0:
                item.exportPDF = False
            elif item.checkState(column)==2:
                item.exportPDF = True
        elif column==2: ## export docx selector
            if item.checkState(column)==0:
                item.exportDocx = False
            elif item.checkState(column)==2:
                item.exportDocx = True
    
    def resizeEvent(self, e):
        super().resizeEvent(e)
        ### need to recalculate the position of the indicator child widget
        self.indicator.move(
            self.geometry().center() - QtCore.QPoint(int(self.indicator.width()/2),
                                                      int(self.indicator.height()/2))
            )
    
    
class FileItem(QtWidgets.QTreeWidgetItem):
    
    def __init__(self, filepath):
        """
        Item representing a file

        Parameters
        ----------
        filepath : pathlib.Path
            Path to a json file. 

        Returns
        -------
        None.

        """
        super().__init__()
        self.filepath = filepath ## data label in the legend
        self.exportPDF = True
        self.exportDocx = False
        
        self.setFlags(self.flags() | QtCore.Qt.ItemIsUserCheckable) # make checkable
        
        self.setCheckState(1, QtCore.Qt.Checked) # set the checkbox state
        self.setCheckState(2, QtCore.Qt.Unchecked) # set the checkbox state
        
        
        self.setText(0, filepath) ## show filepath
        self.setText(1, '') ## tickbox to export
        self.setText(2, '') ## tickbox to export
      

if __name__ == '__main__':
    main()