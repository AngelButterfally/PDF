import sys
import os
from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Ui_PDF import Ui_MainWindow
from getThread import WorkThread_1, WorkThread_2, WorkThread_3
from S120SearchKeyWords import s120_getFailureInformation, getAllFalureCodeS120
from G120CSearchKeyWords import g120c_getFailureInformation, getAllFalureCodeG120C
from G120XSearchKeyWords import g120x_getFailureInformation, getAllFalureCodeG120X
from get_falt_dic_path import getFaltDictionaryPath

# 确保Windows系统下任务栏图标正常
try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'myproduct.subproduct.version'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    restarted = pyqtSignal(QWidget, str)
    _Self = None  # 很重要,保留窗口引用

    def __init__(self, isRestart='NULL', parent=None):
        super(MainWindow, self).__init__(parent)
        MainWindow._Self = self
        self.setupUi(self)
        self.iniFile()
        self.iniVariable()
        self.iniUI(isRestart=isRestart)
        self.iniConfigFunction()
        self.iniThread()
        self.connectFunction()

    def iniFile(self):
        if not os.path.exists('./TXT'):
            os.mkdir('./TXT')
        if not os.path.exists('./PDF'):
            os.mkdir('./PDF')
        if not os.path.exists('./icon'):
            os.mkdir('./icon')
        if not os.path.exists('./EXCEL'):
            os.mkdir('./EXCEL')
        return

    def iniVariable(self):
        # txtFolderFileNum = len([name for name in os.listdir('./TXT') if os.path.isfile(os.path.join('./TXT', name))])
        self.baseDir = os.path.dirname(__file__)
        self.faultDictionary = getFaltDictionaryPath()
        self.currentDictionaryPath = ''
        self.currentDict = ''
        self.currentAllFalure = []
        self.currentCompleter = QCompleter
        self.setFaltDictionaryNum = 3
        self.count = 0
        self.label_pix = 18
        self.ctrlPressed = False
        self.filePathPDF = ''
        self.resultFromChildThreadPDF = ''
        self.errCodeList = []
        self.maximum_storage_history = 10
        self.allFalureCodeS120 = []
        self.allFalureCodeG120X = []
        self.allFalureCodeG120C = []
        # 标志位
        self.flagBit = True
        self.flagLoadTXT = [False]*self.setFaltDictionaryNum
        self.flagSysERR = False

    def iniUI(self, isRestart):
        # 程序自检
        if isRestart == 'restart':
            self.textEdit.append('软件已完成重启。')
        self.setWindowTitle('北自所自控事业部故障码检索系统')
        self.setWindowIcon(
            QIcon(os.path.join(self.baseDir, "icon", "RIAMB.ico")))
        self.setGeometry(150, 150, 1550, 800)
        self.lineEdit.setValidator(QRegExpValidator(QRegExp("[a-zA-Z0-9]+$")))
        self.label.setStyleSheet('font-size:20px;')
        self.label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.label_icon.setPixmap(
            QPixmap(os.path.join(self.baseDir, "icon", "RIAMB_word.png")))
        self.statusShowTime()

    def iniConfigFunction(self):
        '''软件配置'''
        self.checkConfigurationFile(faltDictionary=self.faultDictionary)
        if self.flagSysERR == False:
            self.chooseDefaltDictionary()
            self.choose_errInfo_repository_FUNCTION()
            self.textEdit.append('软件初始化完成。')
        else:
            QMessageBox.critical(self, '错误', '配置文件错误。软件无法运行!')
            self.textEdit.append('软件初始化失败！请尝试重启！')

    def iniThread(self):
        # 子线程
        self.thread_1 = QThread()  # S120
        self.thread_2 = QThread()  # G120C
        self.thread_3 = QThread()  # G120X
        # 实例化线程类
        self.toWorkThread_1 = WorkThread_1()
        self.toWorkThread_2 = WorkThread_2()
        self.toWorkThread_3 = WorkThread_3()
        # moveToThread方法把实例化线程移到Thread管理
        self.toWorkThread_1.moveToThread(self.thread_1)
        self.toWorkThread_2.moveToThread(self.thread_2)
        self.toWorkThread_3.moveToThread(self.thread_3)
        # 接收子线程信号发来的数据
        self.toWorkThread_1.toMainMessage_1.connect(self.acceptThreadMessage)
        self.toWorkThread_2.toMainMessage_2.connect(self.acceptThreadMessage)
        self.toWorkThread_3.toMainMessage_3.connect(self.acceptThreadMessage)
        self.toWorkThread_1.flagFinish_1.connect(self.onThreadFinish)
        self.toWorkThread_2.flagFinish_2.connect(self.onThreadFinish)
        self.toWorkThread_3.flagFinish_3.connect(self.onThreadFinish)
        # 发送数据到子线程
        self.toWorkThread_1.fromMainMessage_1.connect(
            self.toWorkThread_1.processWork)
        self.toWorkThread_2.fromMainMessage_2.connect(
            self.toWorkThread_2.processWork)
        self.toWorkThread_3.fromMainMessage_3.connect(
            self.toWorkThread_3.processWork)
        # 线程执行完成关闭线程
        self.thread_1.finished.connect(self.threadStop)
        self.thread_2.finished.connect(self.threadStop)
        self.thread_3.finished.connect(self.threadStop)

    def connectFunction(self):
        # self.pushButton.clicked.connect(self.show_txt)
        self.actionloadProfileS120.triggered.connect(
            self.load_profile_S120_FUNCTION)
        self.actionloadProfileG120C.triggered.connect(
            self.load_profile_G120C_FUNCTION)
        self.actionloadProfileG120X.triggered.connect(
            self.load_profile_G120X_FUNCTION)
        self.pushButton.clicked.connect(self.search_key_words_FUNCTION)
        self.pushButton.clicked.connect(self.history_storage)
        self.lineEdit.returnPressed.connect(self.search_key_words_FUNCTION)
        self.lineEdit.returnPressed.connect(self.history_storage)
        self.lineEdit.textChanged.connect(self.auto_capitalize_FUNCTION)
        self.comboBox.currentIndexChanged[int].connect(
            self.choose_errInfo_repository_FUNCTION)
        self.listWidget.doubleClicked.connect(self.history_show)
        self.actionEXIT.triggered.connect(QCoreApplication.quit)
        self.actionClearHistory.triggered.connect(self.history_clear_FUNCTION)
        self.actionHistoryNumber.triggered.connect(
            self.history_maxNumber_storage_FUNCTION)
        self.actionFontSize.triggered.connect(self.font_size_FUNCTION)
        self.actionopenHistory.triggered.connect(
            self.show_history_dockwidget_FUNCTION)
        # listwigiet右键菜单
        self.listWidget.customContextMenuRequested.connect(
            self.listWidget_right_menu_FUNCTION)
        # 重启
        self.actionRestart.triggered.connect(self.restart_FUNCTION)
        self.restarted.connect(MainWindow.onRestart)
        # 启动虚拟键盘
        self.actionOpenKeyboard.triggered.connect(self.onOpenKeyboard_FUNCTION)
        # 关于
        self.actionAboutQT.triggered.connect(self.aboutQT_FUNCTION)

    def checkConfigurationFile(self, faltDictionary):
        folder_name = os.path.join(self.baseDir, "TXT")
        if os.path.exists(folder_name):
            # print("文件夹存在")
            # for root, dirs, files in os.walk(folder_name):
            #     for f in files:
            #         print("相对路径：", os.path.relpath(os.path.join(root, f)))
            #         print("绝对路径：", os.path.abspath(os.path.join(root, f)))
            for i in range(self.setFaltDictionaryNum):
                if not os.path.exists(faltDictionary[i][0]):
                    self.textEdit.append('{}配置文件缺失，无法执行{}故障码搜索功能。'.format(
                        faltDictionary[i][1], faltDictionary[i][1]))
                    self.comboBox.setItemData(
                        i, Qt.NoItemFlags, Qt.UserRole - 1)
                    self.flagLoadTXT[i] = False
                else:
                    self.flagLoadTXT[i] = True
        if self.flagLoadTXT[0] == False and self.flagLoadTXT[1] == False and self.flagLoadTXT[2] == False:
            self.comboBox.setDisabled(True)
            self.pushButton.setDisabled(True)
            self.flagSysERR = True
        if os.path.exists(folder_name) ==False:
            self.comboBox.setDisabled(True)
            self.pushButton.setDisabled(True)
            self.flagSysERR = True

    def chooseDefaltDictionary(self):
        if self.flagSysERR == False:
            defaultFile_Index = [i for i, x in enumerate(
                self.flagLoadTXT) if x is True]  # 查询列表中TRUE的索引值
            self.currentDictionaryPath = self.faultDictionary[defaultFile_Index[0]][0]
            self.currentDict = self.faultDictionary[defaultFile_Index[0]][1]
            self.comboBox.setCurrentIndex(defaultFile_Index[0])
        pass

    def choose_errInfo_repository_FUNCTION(self):
        self.allFalureCodeS120 = getAllFalureCodeG120C()
        self.allFalureCodeG120X = getAllFalureCodeG120X()
        self.allFalureCodeG120C = getAllFalureCodeS120()
        self.completer_G120C = QCompleter(self.allFalureCodeS120)
        self.completer_G120X = QCompleter(self.allFalureCodeG120X)
        self.completer_S120 = QCompleter(self.allFalureCodeG120C)
        # 设置匹配模式  有三种： Qt.MatchStartsWith 开头匹配（默认）  Qt.MatchContains 内容匹配  Qt.MatchEndsWith 结尾匹配
        self.completer_G120C.setFilterMode(Qt.MatchContains)
        self.completer_G120X.setFilterMode(Qt.MatchContains)
        self.completer_S120.setFilterMode(Qt.MatchContains)
        # 设置补全模式  有三种： QCompleter.PopupCompletion（默认）  QCompleter.InlineCompletion   QCompleter.UnfilteredPopupCompletion
        self.completer_G120C.setCompletionMode(QCompleter.PopupCompletion)
        self.completer_G120X.setCompletionMode(QCompleter.PopupCompletion)
        self.completer_S120.setCompletionMode(QCompleter.PopupCompletion)
        # 区分大小写的另一种方式
        # self.completer_S120.setCaseSensitivity(Qt.CaseInsensitive)
        self.lineEdit.setCompleter(self.completer_S120)

        if self.comboBox.currentIndex() == 0:
            self.currentDict = 'S120'
            self.textEdit.append('已加载 S120 故障信息库')
            self.currentDictionaryPath = self.faultDictionary[0][0]
            self.currentAllFalure = self.allFalureCodeS120
            self.currentCompleter = self.completer_S120
            self.lineEdit.setCompleter(self.completer_S120)
            self.label.clear()
        elif self.comboBox.currentIndex() == 1:
            self.currentDict = 'G120C'
            self.textEdit.append('已加载 G120C 故障信息库')
            self.currentDictionaryPath = self.faultDictionary[1][0]
            self.currentAllFalure = self.allFalureCodeG120C
            self.currentCompleter = self.completer_G120C
            self.lineEdit.setCompleter(self.completer_G120C)
            self.label.clear()
        elif self.comboBox.currentIndex() == 2:
            self.currentDict = 'G120X'
            self.textEdit.append('已加载 G120X 故障信息库')
            self.currentDictionaryPath = self.faultDictionary[2][0]
            self.currentAllFalure = self.allFalureCodeG120X
            self.currentCompleter = self.completer_G120X
            self.lineEdit.setCompleter(self.completer_G120X)
            self.label.clear()
        # elif self.comboBox.currentIndex() == 3:
        #     self.currentDict = 'HAHA'
        #     self.textEdit.append('已加载 HAHA 故障信息库')
        #     self.defaultDictionaryPath = './TXT/G120X_failure_code_list.txt'

    def auto_capitalize_FUNCTION(self, txt):
        # 输入自动改为大写
        upp_text = txt.upper()
        self.lineEdit.setText(upp_text)
        return

    def load_profile_S120_FUNCTION(self):
        self.filePathPDF, fileTypePDF = QFileDialog.getOpenFileName(
            self, "选择S120故障手册文件", ".", "PDF Files (*.pdf)")
        # 当前线程id
        print('main id', QThread.currentThread())
        # 启动线程
        self.toWorkThread_1.fromMainMessage_1.emit(self.filePathPDF)
        if not self.thread_1.isRunning():
            if os.path.exists(self.filePathPDF):
                self.thread_1.start()
                self.actionloadProfileS120.setEnabled(False)
                self.textEdit.append('正在执行: S120文档扫描')
            else:
                self.textEdit.append('文件路径不存在。')
        else:
            self.textEdit.append('功能正在运行')
        return

    def load_profile_G120C_FUNCTION(self):
        self.filePathPDF, fileTypePDF = QFileDialog.getOpenFileName(
            self, "选择G120C故障手册文件", ".", "PDF Files (*.pdf)")
        # 当前线程id
        print('main id', QThread.currentThread())
        # 启动线程
        self.toWorkThread_2.fromMainMessage_2.emit(self.filePathPDF)
        if not self.thread_2.isRunning():
            if os.path.exists(self.filePathPDF):
                self.thread_2.start()
                self.actionloadProfileG120C.setEnabled(False)
                self.textEdit.append('正在执行: G120C文档扫描')
            else:
                self.textEdit.append('文件路径不存在。')
        else:
            self.textEdit.append('功能正在运行')
        return

    def load_profile_G120X_FUNCTION(self):
        self.filePathPDF, fileTypePDF = QFileDialog.getOpenFileName(
            self, "选择G120X故障手册文件", ".", "PDF Files (*.pdf)")
        # 当前线程id
        print('main id', QThread.currentThread())
        # 启动线程
        self.toWorkThread_3.fromMainMessage_3.emit(self.filePathPDF)
        if not self.thread_3.isRunning():
            if os.path.exists(self.filePathPDF):
                self.thread_3.start()
                self.actionloadProfileG120X.setEnabled(False)
                self.textEdit.append('正在执行: G120X文档扫描')
            else:
                self.textEdit.append('文件路径不存在。')
        else:
            self.textEdit.append('功能正在运行')
        return

    def history_maxNumber_storage_FUNCTION(self):
        num, ok = QInputDialog.getInt(
            self, '历史存储数量', '输入数字(1~20)', value=5, min=1, max=20)
        if ok:
            self.maximum_storage_history = num
            if len(self.errCodeList) > self.maximum_storage_history:
                self.errCodeList = self.errCodeList[0:self.maximum_storage_history]
                self.listWidget.clear()
                self.listWidget.addItems(self.errCodeList)
        self.textEdit.append(
            '设置最大历史信息存储数量为：'+str(self.maximum_storage_history))
        return

    def font_size_FUNCTION(self):
        num, ok = QInputDialog.getInt(
            self, '字体大小设置', '输入数字(12~34)', value=self.label_pix, min=8, max=30, step=2)
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
        code = self.lineEdit.text()
        if len(code) == 6:
            errCode = self.lineEdit.text()
        else:
            errCode = self.currentCompleter.currentCompletion()
        self.lineEdit.setText(errCode)
        message, self.flagBit = self.search_key_words(
            self.currentDictionaryPath, errCode, self.currentDict)
        self.label.setText(message)
        return

    def show_history_dockwidget_FUNCTION(self):
        self.dockWidget_History.show()

    def search_key_words(self, errDictionaryPath, errCode, switchDict):
        if switchDict == 'S120':
            message, flagBit = s120_getFailureInformation(
                errDictionaryPath, errCode)
        elif switchDict == 'G120C':
            message, flagBit = g120c_getFailureInformation(
                errDictionaryPath, errCode)
        elif switchDict == 'G120X':
            message, flagBit = g120x_getFailureInformation(
                errDictionaryPath, errCode)
        return message, flagBit

    def wheelEvent(self, event):
        angle = event.angleDelta() / 8  # 返回QPoint对象，为滚轮转过的数值，单位为1/8度
        angleY = angle.y()
        # 获取当前鼠标相对于view的位置
        if self.ctrlPressed == True and self.label.underMouse():
            if angleY > 0:
                self.label_pix += 2
                if self.label_pix >= 24:
                    self.label_pix = 24
            else:  # 滚轮下滚
                self.label_pix -= 2
                if self.label_pix <= 16:
                    self.label_pix = 16
            label_pix = 'font-size:' + str(self.label_pix) + 'px;'
            self.label.setStyleSheet(label_pix)
            # self.adjustSize()
            self.update()

    def keyReleaseEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Control:
            self.ctrlPressed = False
        return super().keyReleaseEvent(QKeyEvent)

    def keyPressEvent(self, QKeyEvent):
        if QKeyEvent.key() == Qt.Key_Control:
            self.ctrlPressed = True
        return super().keyPressEvent(QKeyEvent)

    def history_storage(self):
        if self.flagBit == True:
            errCode = self.lineEdit.text()
            indexFaultictionary = self.comboBox.currentIndex()
            if indexFaultictionary == 0:
                faultDictionaryHistory = 'S120'
            elif indexFaultictionary == 1:
                faultDictionaryHistory = 'G120C'
            elif indexFaultictionary == 2:
                faultDictionaryHistory = 'G120X'
            faultHistoryInformation = faultDictionaryHistory + '-' + errCode
            if len(self.errCodeList) < self.maximum_storage_history:
                if faultHistoryInformation not in self.errCodeList:
                    self.errCodeList.insert(0, faultHistoryInformation)
            else:
                if faultHistoryInformation not in self.errCodeList:
                    self.errCodeList.insert(0, faultHistoryInformation)
                    self.errCodeList.pop()
            self.listWidget.clear()
            self.listWidget.addItems(self.errCodeList)
        elif self.flagBit == False:
            return

    def history_show(self):
        a_item = self.listWidget.selectedItems()[0]  # 获取选择的item
        index = self.listWidget.indexFromItem(a_item)  # 通过item获取选择的索引号
        message = self.errCodeList[index.row()]
        switchDict = message.split('-', 1)[0]
        errCode = message.split('-', 1)[1]
        if switchDict == 'S120':
            errDictionary = './TXT/S120_failure_code_list.txt'
        elif switchDict == 'G120C':
            errDictionary = './TXT/G120C_failure_code_list.txt'
        elif switchDict == 'G120X':
            errDictionary = './TXT/G120X_failure_code_list.txt'
        message = self.search_key_words(errDictionary, errCode, switchDict)
        self.label.setText(message[0])
        return

    def listWidget_right_menu_FUNCTION(self, pos):

        menu = QtWidgets.QMenu()
        opt1 = menu.addAction("删除条目")
        opt2 = menu.addAction("清空历史记录")
        hitIndex = self.listWidget.indexAt(pos).column()
        if hitIndex > -1:
            # 获取item内容
            # name=self.listWidget.item(hitIndex).text()
            action = menu.exec_(self.listWidget.mapToGlobal(pos))
            if action == opt1:
                self.errCodeList.pop(hitIndex)
                self.listWidget.clear()
                self.listWidget.addItems(self.errCodeList)
            elif action == opt2:
                self.errCodeList.clear()
                self.listWidget.clear()
                self.listWidget.addItems(self.errCodeList)
                return

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

    def showCurrentTime(self, timeLabel):
        '''获取当前时间'''
        # import time
        # time.sleep(5)
        currentTime = QDateTime.currentDateTime()
        self.timeDisplay = currentTime.toString('yyyy-MM-dd hh:mm:ss dddd')
        timeLabel.setText(self.timeDisplay)

    def restart_FUNCTION(self):
        if QMessageBox.question(self, "提示", "确认要重启软件吗?") == QMessageBox.Yes:
            self.hide()
            # 软件底部日期显示重置
            self.restarted.emit(self, 'restart')
            self.timeLabel = QLabel()
            self.info = QLabel()
        return

    @classmethod  # 使用classmethod重载功能
    def onRestart(cls, widget, restart):
        w = MainWindow(restart)
        w.show()
        widget.close()
        widget.deleteLater()
        del widget

    def onOpenKeyboard_FUNCTION(self):
        import glob
        kernelType = QSysInfo.kernelType()
        if kernelType == 'winnt':
            try:
                path = glob.glob(
                    r'C:\Windows\WinSxS\amd64_microsoft-windows-osk_*\osk.exe')[0]
                ret = QProcess.startDetached(path)
                self.textEdit.append('虚拟键盘调用成功。')
            except Exception as e:
                self.textEdit.append('调用错误，错误信息: %s' % e)
            # try:
            #     # 32位程序调用64位操作系统下的程序会被重定向到SysWOW64目录
            #     # 可通过`Wow64DisableWow64FsRedirection`和`Wow64RevertWow64FsRedirection`控制
            #     ret.QProcess.startDetached(r'C:\Windows\system32\osk.exe')
            #     self.textEdit.append('start 32 osk: %s' % ret)
            # except Exception as e:
            #     self.textEdit.append('start osk error: %s' % e)
        elif kernelType == 'darwin':
            self.textEdit.append('该系统无法使用此功能')
            pass
        elif kernelType == 'linux':
            self.textEdit.append('该系统无法使用此功能')
            pass

    def acceptThreadMessage(self, receiveMessageFromChild):
        self.resultFromChildThreadPDF = receiveMessageFromChild

    def onThreadFinish(self, flagFinish):
        if flagFinish == 'finish_T1' and self.thread_1.isRunning():
            self.thread_1.requestInterruption()
            self.thread_1.quit()
            self.thread_1.wait()
        elif flagFinish == 'finish_T2' and self.thread_2.isRunning():
            self.thread_2.requestInterruption()
            self.thread_2.quit()
            self.thread_2.wait()
        elif flagFinish == 'finish_T3' and self.thread_3.isRunning():
            self.thread_3.requestInterruption()
            self.thread_3.quit()
            self.thread_3.wait()

    def threadStop(self):
        '''退出线程'''
        if self.thread_1.isRunning() == False and self.actionloadProfileS120.isEnabled() == False:
            self.actionloadProfileS120.setEnabled(True)
        elif self.thread_2.isRunning() == False and self.actionloadProfileG120C.isEnabled() == False:
            self.actionloadProfileG120C.setEnabled(True)
        elif self.thread_3.isRunning() == False and self.actionloadProfileG120X.isEnabled() == False:
            self.actionloadProfileG120X.setEnabled(True)
        self.textEdit.append(self.resultFromChildThreadPDF)

    def aboutQT_FUNCTION(self):
        QMessageBox.aboutQt(self, 'QT')

    def TEST(self):
        self.textEdit.append('test message ~')
        return


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    myWin = MainWindow()
    myWin.show()
    sys.exit(app.exec_())
