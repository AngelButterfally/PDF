import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui_PDF import Ui_MainWindow
from S120ScanPDF import s120_scan_PDF_function
from S120SearchKeyWords import s120_search_key_words_function


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.iniVariable()
        self.iniUI()
        self.connectFunction()

    def iniUI(self):
        self.setWindowTitle('北自所自控事业部故障码检索系统')
        self.setGeometry(300, 300, 1000, 500)
        self.lineEdit.setValidator(QRegExpValidator(QRegExp("[A-Z0-9]+$")))
        self.textEdit.append('系统默认加载S120故障信息库')

    def iniVariable(self):
        self.count = 0
        self.label_pix = 20
        self.ctrlPressed=False
        self.faultDictionary = './TXT/S120_failure_code_list.txt'

    def connectFunction(self):
        # self.pushButton.clicked.connect(self.show_txt)
        self.actionscanPDF.triggered.connect(self.scan_PDF)
        self.actionsearchERR.triggered.connect(self.search_key_words)
        self.pushButton.clicked.connect(self.search_key_words)
        self.lineEdit.returnPressed.connect(self.search_key_words)
        self.comboBox.currentIndexChanged[int].connect(self.choose_combobox)

    def choose_combobox(self):
        # self.textEdit.append(self.comboBox.currentText())
        # self.textEdit.append(str(self.comboBox.currentIndex()))
        if self.comboBox.currentIndex() == 0:
            self.textEdit.append('已加载S120故障信息库')
            self.faultDictionary = './TXT/S120_failure_code_list.txt'
        elif self.comboBox.currentIndex() == 1:
            self.textEdit.append('已加载G120C故障信息库')
            self.faultDictionary = './TXT/G120C_failure_code_list.txt'

    def scan_PDF(self):
        filename = QFileDialog.getOpenFileName(
            self, "选择文件", ".", "PDF Files (*.pdf)")
        result = s120_scan_PDF_function(filename[0])
        self.textEdit.append(result)

    def search_key_words(self):

        errCode = self.lineEdit.text()
        message = s120_search_key_words_function(self.faultDictionary, errCode)
        self.label.setText(message)

    def wheelEvent(self, event):
        if self.ctrlPressed == True:
            angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
            angleY = angle.y()
            # 获取当前鼠标相对于view的位置
            if angleY > 0:
                self.label_pix += 1
                if self.label_pix >= 50:
                    self.label_pix = 50
            else:  # 滚轮下滚
                self.label_pix -= 1
                if self.label_pix <=15:
                    self.label_pix = 15
            self.textEdit.append(str(self.label_pix))
            label_pix = 'font-size:' + str(self.label_pix) + 'px;'
            self.label.setStyleSheet(label_pix)
            # self.adjustSize()
            self.update()
    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key()==Qt.Key_Control:
            self.ctrlPressed=False
            self.textEdit.append('false ctrl')
        return super().keyReleaseEvent(QKeyEvent)
    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key()==Qt.Key_Control:
            self.ctrlPressed=True
            self.textEdit.append('true ctrl')
        return super().keyPressEvent(QKeyEvent)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())
