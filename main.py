import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui_PDF import Ui_MainWindow
from S120ScanPDF import s120_scan_PDF_function
from S120SearchKeyWords import s120_getFailureInformation

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.iniUI()
        self.iniVariable()
        self.connectFunction()

    def iniUI(self):
        self.setWindowTitle('FUCK!')
        self.setGeometry(300, 300, 1000, 500)
        self.lineEdit.setValidator(QRegExpValidator(QRegExp("[A-Z0-9]+$")))
    
    def iniVariable(self):
        self.count = 0

    def connectFunction(self):
        # self.pushButton.clicked.connect(self.show_txt)
        self.actionscanPDF.triggered.connect(self.scan_PDF)
        self.actionsearchERR.triggered.connect(self.search_key_words)
        self.pushButton.clicked.connect(self.search_key_words)
        self.lineEdit.returnPressed.connect(self.search_key_words)


    # def show_txt(self):
    #     self.textEdit.append(str(self.count))
    #     self.textEdit.append(self.lineEdit.text())
    #     self.count = self.count+1
    
    def scan_PDF(self):
        filename = QFileDialog.getOpenFileName(self, "选择文件", ".", "PDF Files (*.pdf)")
        result = s120_scan_PDF_function(filename[0])
        self.textEdit.append(result)
    def search_key_words(self):

        errCode= self.lineEdit.text()
        message = s120_getFailureInformation('./TXT/S120_failure_code_list.txt',errCode)
        
        self.label.setStyleSheet('font-size:20px;')
        # self.label.setStyleSheet('line-height:800px;')
        self.label.setText(message)
        return
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())
