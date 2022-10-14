import sys
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui_PDF import Ui_MainWindow
from S120ScanPDF import s120_scan_PDF_function
from S120SearchKeyWords import s120_getFailureInformation
from G120CSearchKeyWords import g120c_getFailureInformation


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
        self.faultDictionaryPath = './TXT/S120_failure_code_list.txt'
        self.errCodeList = []
        self.maximum_storage_history = 10
        self.currentDict = 'S120'

    def iniUI(self):
        self.setWindowTitle('北自所自控事业部故障码检索系统')
        self.setWindowIcon(QIcon('./icon/RIAMB.ico'))
        self.setGeometry(150, 150, 1550, 800)
        self.statusShowTime()
        self.lineEdit.setValidator(QRegExpValidator(QRegExp("[A-Z0-9]+$")))
        self.textEdit.append('已加载S120故障信息库')
        self.label.setStyleSheet('font-size:20px;')
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.textEdit.append('软件初始化完成。')      

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
        self.actionFontSize.triggered.connect(self.font_size_FUNCTION)

    def choose_errInfo_repository_FUNCTION(self):
        if self.comboBox.currentIndex() == 0:
            self.currentDict = 'S120'
            self.textEdit.append('已加载S120故障信息库')
            self.faultDictionaryPath = './TXT/S120_failure_code_list.txt'
        elif self.comboBox.currentIndex() == 1:
            self.currentDict = 'G120C'
            self.textEdit.append('已加载G120C故障信息库')
            self.faultDictionaryPath = './TXT/G120C_failure_code_list.txt'

    def scan_PDF_FUNCTION(self):
        filename = QFileDialog.getOpenFileName(
            self, "选择文件", ".", "PDF Files (*.pdf)")
        result = s120_scan_PDF_function(filename[0])
        self.textEdit.append(result)
        self.textEdit.append('正在执行：文档扫描')

    def history_maxNumber_storage_FUNCTION(self):
        num,ok=QInputDialog.getInt(self,'历史存储数量','输入数字(1~20)',value=5,min=1,max=20)
        if ok:
            self.maximum_storage_history = num
            if len(self.errCodeList) > self.maximum_storage_history:
                self.errCodeList = self.errCodeList[0:self.maximum_storage_history]
                self.listWidget.clear()
                self.listWidget.addItems(self.errCodeList)
        self.textEdit.append('设置最大历史信息存储数量为：'+str(self.maximum_storage_history))
        return

    def font_size_FUNCTION(self):
        num,ok=QInputDialog.getInt(self,'字体大小设置','输入数字(12~34)',value=self.label_pix,min=8,max=30,step=2)
        self.label_pix = num
        label_pix = 'font-size:' + str(self.label_pix) + 'px;'
        self.label.setStyleSheet(label_pix)
        self.update()
        self.textEdit.append('设置显示字体大小为：'+str(self.label_pix) + 'px')
        return

    def history_clear_FUNCTION(self):
        self.errCodeList = []
        self.listWidget.clear()
        return

    def search_key_words_FUNCTION(self):
        errCode = self.lineEdit.text()
        message = self.search_key_words(self.faultDictionaryPath, errCode,self.currentDict)
        self.label.setText(message)
        return
    
    def search_key_words(self,errDictionaryPath,errCode,switchDict):
        if switchDict == 'S120':
            message = s120_getFailureInformation(errDictionaryPath, errCode)
        elif switchDict == 'G120C':
            message = g120c_getFailureInformation(errDictionaryPath, errCode)
        return message

    def wheelEvent(self, event):
        if self.ctrlPressed == True:
            angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
            angleY = angle.y()
            # 获取当前鼠标相对于view的位置
            if angleY > 0:
                self.label_pix += 2
                if self.label_pix >= 24:
                    self.label_pix = 24
            else:  # 滚轮下滚
                self.label_pix -= 2
                if self.label_pix <=16:
                    self.label_pix = 16
            # print(self.label_pix)
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
        switchDict = message.split('-',1)[0]
        errCode = message.split('-',1)[1]
        if switchDict == 'S120':
            errDictionary = './TXT/S120_failure_code_list.txt'
        elif switchDict == 'G120C':
            errDictionary = './TXT/G120C_failure_code_list.txt'
        message = self.search_key_words(errDictionary,errCode,switchDict)
        self.label.setText(message)
        return

    def showCurrentTime(self, timeLabel):
        '''获取当前时间'''
        time = QDateTime.currentDateTime()
        timeDisplay = time.toString('yyyy-MM-dd hh:mm:ss dddd')
        timeLabel.setText(timeDisplay)

    def statusShowTime(self):
        '''显示当前时间'''
        self.timer = QTimer()
        self.timeLabel = QLabel()
        self.statusBar.addPermanentWidget(self.timeLabel, 1)
        self.timer.timeout.connect(lambda: self.showCurrentTime(
            self.timeLabel))
        self.timer.start(500)
        self.info = QLabel()
        self.info.setText('-Code by RIAMB-')
        self.statusBar.addPermanentWidget(self.info, 0)

    def test(self):
        self.textEdit.append('test message ~')
        return

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())