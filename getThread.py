import os
from PyQt5.QtCore import QThread, pyqtSignal,QObject
from S120ScanPDF import s120_scan_PDF_function
from G120CScanPDF import g120c_scan_PDF_function
from G120XScanPDF import g120x_scan_PDF_function

class WorkThread_1(QObject):
    toMainMessage_1 = pyqtSignal(str)  # 值变化信号
    fromMainMessage_1 = pyqtSignal(str)
    flagFinish_1 = pyqtSignal(str)
    def __init__(self):
        super(WorkThread_1,self).__init__()

    def processWork(self,str):
        print('thread id', QThread.currentThread())
        # print(str)
        if os.path.exists(str):
            result = s120_scan_PDF_function(str)
        self.toMainMessage_1.emit(result)
        self.flagFinish_1.emit('finish_T1')

class WorkThread_2(QObject):
    toMainMessage_2 = pyqtSignal(str)  # 值变化信号
    fromMainMessage_2 = pyqtSignal(str)
    flagFinish_2 = pyqtSignal(str)
    def __init__(self):
        super(WorkThread_2,self).__init__()

    def processWork(self,str):
        print('thread id', QThread.currentThread())
        # print(str)
        if os.path.exists(str):
            result = g120c_scan_PDF_function(str)
        self.toMainMessage_2.emit(result)
        self.flagFinish_2.emit('finish_T2')

class WorkThread_3(QObject):
    toMainMessage_3 = pyqtSignal(str)  # 值变化信号
    fromMainMessage_3 = pyqtSignal(str)
    flagFinish_3 = pyqtSignal(str)
    def __init__(self):
        super(WorkThread_3,self).__init__()

    def processWork(self,str):
        print('thread id', QThread.currentThread())
        # print(str)
        if os.path.exists(str):
            result = g120x_scan_PDF_function(str)
        self.toMainMessage_3.emit(result)
        self.flagFinish_3.emit('finish_T3')