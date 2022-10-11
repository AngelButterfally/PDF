import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui_PDF import Ui_MainWindow
from scanPDF import scan_PDF_function

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
        self.pushButton.clicked.connect(self.show_txt)
        self.actionscanPDF.triggered.connect(self.scan_PDF)

    def show_txt(self):
        self.textEdit.append(str(self.count))
        self.textEdit.append(self.lineEdit.text())
        self.count = self.count+1
    
    def scan_PDF(self):
        filename = QFileDialog.getOpenFileName(self, "选择文件", ".", "PDF Files (*.pdf)")
        result = scan_PDF_function(filename[0])
        self.textEdit.append(result)

    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())
