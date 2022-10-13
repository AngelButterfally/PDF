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
        self.iniVariable()
        self.iniUI()
        self.connectFunction()

    def iniVariable(self):
        self.count = 0
        self.label_pix = 18
        self.ctrlPressed=False
        self.faultDictionary = './TXT/S120_failure_code_list.txt'
        self.errCodeList = []
        self.maximum_storage_history = 10
        # self.errInfoRepository = 'S120'

    def iniUI(self):
        self.setWindowTitle('北自所自控事业部故障码检索系统')
        self.setWindowIcon(QIcon('./icon/RIAMB.png'))
        self.setGeometry(300, 300, 1000, 500)
        self.lineEdit.setValidator(QRegExpValidator(QRegExp("[A-Z0-9]+$")))
        self.textEdit.append('已加载S120故障信息库')
        self.label.setStyleSheet('font-size:20px;')

    def connectFunction(self):
        # self.pushButton.clicked.connect(self.show_txt)
        self.actionscanPDF.triggered.connect(self.scan_PDF_FUNCTION)
        self.actionsearchERR.triggered.connect(self.search_key_words_FUNCTION)
        self.actionsearchERR.triggered.connect(self.history_storage)
        self.pushButton.clicked.connect(self.search_key_words_FUNCTION)
        self.pushButton.clicked.connect(self.history_storage)
        self.lineEdit.returnPressed.connect(self.search_key_words_FUNCTION)
        self.lineEdit.returnPressed.connect(self.history_storage)
        self.comboBox.currentIndexChanged[int].connect(self.choose_errInfo_repository_FUNCTION)
        self.listWidget.doubleClicked.connect(self.history_show)
        # self.pushButton_2.clicked.connect(self.test)
        self.actionEXIT.triggered.connect(QCoreApplication.quit)
        self.actionClearHistory.triggered.connect(self.history_clear_FUNCTION)
        self.actionHistoryNumber.triggered.connect(self.history_maxNumber_storage_FUNCTION)

    def choose_errInfo_repository_FUNCTION(self):
        if self.comboBox.currentIndex() == 0:
            self.textEdit.append('已加载S120故障信息库')
            self.faultDictionary = './TXT/S120_failure_code_list.txt'
        elif self.comboBox.currentIndex() == 1:
            self.textEdit.append('已加载G120C故障信息库')
            self.faultDictionary = './TXT/G120C_failure_code_list.txt'

    def scan_PDF_FUNCTION(self):
        filename = QFileDialog.getOpenFileName(
            self, "选择文件", ".", "PDF Files (*.pdf)")
        result = s120_scan_PDF_function(filename[0])
        self.textEdit.append(result)

    def history_maxNumber_storage_FUNCTION(self):
        num,ok=QInputDialog.getInt(self,'历史存储数量','输入数字(1~20)',value=5,min=1,max=20)
        if ok:
            self.maximum_storage_history = num
            if len(self.errCodeList) > self.maximum_storage_history:
                self.errCodeList = self.errCodeList[0:self.maximum_storage_history]
                self.listWidget.clear()
                self.listWidget.addItems(self.errCodeList)
        return

    def history_clear_FUNCTION(self):
        self.listWidget.clear()
        return

    def search_key_words_FUNCTION(self):
        errCode = self.lineEdit.text()
        message = self.search_key_words(self.faultDictionary, errCode)
        self.label.setText(message)
    
    def search_key_words(self,errDictionary,errCode):
        message = s120_getFailureInformation(errDictionary, errCode)
        return message

    def wheelEvent(self, event):
        if self.ctrlPressed == True:
            angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
            angleY = angle.y()
            # 获取当前鼠标相对于view的位置
            if angleY > 0:
                self.label_pix += 2
                if self.label_pix >= 34:
                    self.label_pix = 34
            else:  # 滚轮下滚
                self.label_pix -= 2
                if self.label_pix <=14:
                    self.label_pix = 14
            print(self.label_pix)
            label_pix = 'font-size:' + str(self.label_pix) + 'px;'
            self.label.setStyleSheet(label_pix)
            # self.adjustSize()
            self.update()

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key()==Qt.Key_Control:
            self.ctrlPressed=False
        return super().keyReleaseEvent(QKeyEvent)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key()==Qt.Key_Control:
            self.ctrlPressed=True
        return super().keyPressEvent(QKeyEvent)

    def history_storage(self):
        errCode = self.lineEdit.text()
        indexFaultictionary = self.comboBox.currentIndex()
        if indexFaultictionary ==0:
            faultDictionaryHistory ='S120'
        elif indexFaultictionary ==1:
            faultDictionaryHistory ='G120C'
        faultHistoryInformation = faultDictionaryHistory + '-' + errCode
        if len(self.errCodeList) <self.maximum_storage_history:
            if faultHistoryInformation not in self.errCodeList:
                self.errCodeList.insert(0,faultHistoryInformation)
        else:
            if faultHistoryInformation not in self.errCodeList:
                self.errCodeList.insert(0,faultHistoryInformation)
                self.errCodeList.pop()
        self.listWidget.clear()
        self.listWidget.addItems(self.errCodeList)

    def history_show(self):
        a_item = self.listWidget.selectedItems()[0]  # 获取选择的item
        index = self.listWidget.indexFromItem(a_item)  # 通过item获取选择的索引号
        message = self.errCodeList[index.row()]
        errInfoRepository = message.split('-',1)[0]
        errCode = message.split('-',1)[1]
        if errInfoRepository == 'S120':
            errDictionary = './TXT/S120_failure_code_list.txt'
        elif errInfoRepository == 'G120C':
            errDictionary = './TXT/G120C_failure_code_list.txt'
        message = self.search_key_words(errDictionary,errCode)
        self.label.setText(message)
        return

    def test(self):
        self.textEdit.append('test message ~')
        return



if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())
