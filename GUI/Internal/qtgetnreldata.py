import sys
import time
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLabel, QLineEdit, QMessageBox, QFileDialog
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
from nrelsolardata import NRELData

class Sample (QMainWindow):

    def __init__ (self):
        super().__init__()
        self.title = "SWITCH - Get NREL Data"
        self.width = 430
        self.height = 380
        self.initUI()

    def initUI (self):
        # Main Window
        self.setGeometry(300, 300, self.width, self.height)
        self.setWindowTitle(self.title)
        # self.setWindowIco(QIcon(<path>))

        # NREL
        label1 = QLabel('Fill in the following info. to start pulling data from NREL', self)
        label1.move (35,20)
        label1.resize(350,20)

        # Name
        labelName = QLabel('Name: ', self)
        labelName.move(20, 55)
        self.textboxName = QLineEdit (self)
        self.textboxName.resize(340,25)
        self.textboxName.move(65, 55)

        # Reason for use
        labelReason = QLabel('Reason for use: ', self)
        labelReason.move(20, 90)
        self.textboxReason = QLineEdit (self)
        self.textboxReason.resize(280, 25)
        self.textboxReason.move(125, 90)
        
        # Email
        labelEmail = QLabel('User Email: ', self)
        labelEmail.move(20, 125)
        self.textboxEmail = QLineEdit (self)
        self.textboxEmail.resize(310,25)
        self.textboxEmail.move(95, 125)
        
        # Time interval (in minutes)
        labelInterval = QLabel('Interval (mins): ', self)
        labelInterval.move(20, 160)
        self.textboxInterval = QLineEdit (self)
        self.textboxInterval.resize(280, 25)
        self.textboxInterval.move(125, 160)

        # Affiliation
        labelAffiliation = QLabel('Affiliation: ', self)
        labelAffiliation.move(20, 195)
        self.textboxAffiliation = QLineEdit (self)
        self.textboxAffiliation.resize(310, 25)
        self.textboxAffiliation.move(95, 195)

        # API Key
        labelAPI = QLabel('API Key: ', self)
        labelAPI.move(20, 230)
        self.textboxAPI = QLineEdit (self)
        self.textboxAPI.resize(320, 25)
        self.textboxAPI.move(85, 230)

        # Data Year
        labelYear = QLabel('Year: ', self)
        labelYear.move(20, 265)
        self.textboxYear = QLineEdit (self)
        self.textboxYear.resize(340, 25)
        self.textboxYear.move(65, 265)

        # Pull Data Button
        pullDataBttn = QPushButton('Pull Data From NREL', self)
        pullDataBttn.move(120, 300)
        pullDataBttn.resize(180, 25)
        pullDataBttn.clicked.connect(self.pullDataNREL)
        
        self.show()

    @pyqtSlot()
    def pullDataNREL (self):
        missingD = self.checkForMissingInfo()

        print (self.textboxName.text())
        print (self.textboxEmail.text())
        print (self.textboxReason.text())
        print (self.textboxInterval.text())
        print (self.textboxAffiliation.text())
        print (self.textboxAPI.text())
        print (self.textboxYear.text())
        
        # Check for missing info.
        if len(missingD) != 0:
            QMessageBox.critical(self, "Missing information", "The following info. is missing: " + missingD, QMessageBox.Ok, QMessageBox.Ok)
            return

        self.meshFile = QFileDialog.getOpenFileName(self, 'Select Mesh File (.csv)', '/home')
        self.savingDirectory = QFileDialog.getExistingDirectory(self, 'Select Saving Directory', '/home')

        # Check that mesh file path isn't empty.
        if len(self.meshFile) == 0:
            QMessageBox.critical(self, "Missing Mesh File", "Please select a mesh file.", QMessageBox.Ok, QMessageBox.Ok)
            return

        # Check that the folder path isn't empty.
        if len(self.savingDirectory) == 0:
            QMessageBox.critical(self, "Missing Mesh File", "Please select a folder to save.", QMessageBox.Ok, QMessageBox.Ok)
            return

        print (self.meshFile[0])
        print (self.savingDirectory)
        
        NRELData.create_folders (self.savingDirectory, self.textboxYear.text())
        NRELData.get_data (self.meshFile[0], self.savingDirectory, self.textboxYear.text(), self.textboxInterval.text(), self.textboxName.text(), self.textboxEmail.text(), self.textboxReason.text(), self.textboxAffiliation.text(), self.textboxAPI.text(), 'false')
        
            
    def comaSeparate(self, string):
        if len(string) != 0:
            return ', '
        return ''
        
    def checkForMissingInfo (self):
        missingInfo = ''
        if self.textboxName.text() == '':
            missingInfo += 'Name'
        if self.textboxReason.text() == '':
            missingInfo += self.comaSeparate(missingInfo) + 'Reason for use'
        if self.textboxEmail.text() == '':
            missingInfo += self.comaSeparate(missingInfo) + 'User email'
        if self.textboxInterval.text() == '':
            missingInfo += self.comaSeparate(missingInfo) + 'Interval (mins)'
        if self.textboxAffiliation.text() == '':
            missingInfo += self.comaSeparate(missingInfo) + 'Affiliation'
        if self.textboxAPI.text() == '':
            missingInfo += self.comaSeparate(missingInfo) + 'API Key'
        if self.textboxYear.text() == '':
            missingInfo += self.comaSeparate(missingInfo) + 'Year'
            
        return missingInfo
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    sample = Sample()
    sys.exit(app.exec_())
