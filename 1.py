# coding:utf-8

import sys
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QApplication, QLabel, QLineEdit,
                             QCompleter, QVBoxLayout)


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 300)
        self.setWindowTitle('QCompleter例子')

        # 创建一个QLabel
        label = QLabel('请输入国家名称：', self)
        label.setFont(QFont('Arial', 15))
        self.lineEdit = QLineEdit(self)

        # 创建一个QCompleter
        completer = QCompleter(['China', 'Japan', 'America', 'India'])
        self.lineEdit.setCompleter(completer)

        # 创建一个布局
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        vbox.addWidget(self.lineEdit)

        self.setLayout(vbox)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec_())