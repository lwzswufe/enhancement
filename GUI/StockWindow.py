from PyQt5 import QtCore, QtGui, QtWidgets
from typing import Tuple, Callable
from copy import deepcopy


class Position(object):
    def __init__(self, xLeft: int, yTop: int, xRight: int, yBottom: int):
        self.xLeft = xLeft
        self.yTop = yTop
        self.xRight = xRight
        self.yBottom = yBottom

    def MoveDown(self, num):
        self.yTop += num
        self.yBottom += num

    def MoveUp(self, num):
        if self.yTop >= num:
            self.yTop -= num
            self.yBottom -= num

    def GetData(self):
        return self.xLeft, self.yTop, self.xRight, self.yBottom

    def GetHigh(self):
        return self.yBottom-self.yTop

    def GetRect(self):
        return self.xLeft, self.yTop, self.xRight-self.xLeft, self.yBottom-self.yTop


class SubWindow(object):
    def __init__(self, parent: QtWidgets.QWidget, name: str, pos: Position, deleteCallBack: Callable):
        # self.groupBox.setGeometry(QtCore.QRect(10, 10, 611, 251))
        self.deleteCallBack = deleteCallBack
        self.pos = Position(pos.xLeft+5, pos.yTop+10, pos.xRight-10, pos.yBottom-5)
        print("window {} pos: {}".format(name, self.pos.GetData()))
        window = QtWidgets.QFrame(parent)
        window.setGeometry(QtCore.QRect(*(self.pos.GetRect())))
        # self.groupBox.setGeometry(QtCore.QRect(10, 10, 611, 251))
        window.setObjectName("subQWidget")
        window.setFrameShape(QtWidgets.QFrame.Box)
        print(window.geometry())
        self.window = window
        # 策略输入框
        textEdit = QtWidgets.QTextEdit(self.window)
        textEdit.setGeometry(QtCore.QRect(30, 50, 60, 30))
        textEdit.setObjectName("textBrowser")
        self.textBrowser = textEdit
        # 名称显示标签
        mainLabel = QtWidgets.QLabel(self.window)
        mainLabel.setGeometry(QtCore.QRect(20, 10, 100, 30))
        mainLabel.setObjectName("mainLabel")
        mainLabel.setText(name)
        self.mainLable = mainLabel
        # 删除按钮
        deletePushButton = QtWidgets.QPushButton(self.window)
        deletePushButton.setGeometry(QtCore.QRect(480, 20, 95, 30))
        deletePushButton.setObjectName("deletePushButton")
        deletePushButton.clicked.connect(self.deleteWindow)
        deletePushButton.setText("删除")
        self.deletePushButton = deletePushButton
        self.name = name

    def moveUp(self, num):
        '''
        向上移动
        :return:
        '''
        print("window {} move up {} oldPos:{}".format(self.name, num, self.pos.GetData()))
        self.pos.MoveUp(num)
        self.window.move(self.pos.xLeft, self.pos.yTop)
        self.show()
        print("window {} pos: {} {}".format(self.name, self.pos.GetData(), self.window.geometry()))

    def deleteWindow(self):
        '''

        :return:
        '''
        self.deleteCallBack(self.name)
        print("delete window {}".format(self.name))

    def show(self):
        self.window.show()

    def close(self):
        print("close window {}".format(self.name))
        self.window.close()


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 680)
        self.WindowMap = {}
        self.WindowList = []
        # 主窗口
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # 滚动窗口
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setGeometry(QtCore.QRect(60, 100, 620, 800))
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 600, 2500))
        self.pos = Position(0, 0, 600, 240)
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        # 主输入框
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.mainTextEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.mainTextEdit.setGeometry(QtCore.QRect(440, 70, 121, 31))
        self.mainTextEdit.setObjectName("mainTextEdit")
        # 主按钮
        self.mainPushButton = QtWidgets.QPushButton(self.centralwidget)
        self.mainPushButton.setGeometry(QtCore.QRect(560, 67, 101, 31))
        self.mainPushButton.setObjectName("mainPushButton")
        self.mainPushButton.clicked.connect(self.addSubWindow)
        # 设置主窗口
        MainWindow.setCentralWidget(self.centralwidget)
        # 菜单
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        # 状态栏
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # 文本替换
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.mainPushButton.setText(_translate("MainWindow", "添加代码"))

    def onDeleteSubWindow(self, name: str):
        '''
        删除子窗口事件
        :return:
        '''
        print("OnDeleteSubWindow {}".format(name))
        deletePos = -1
        for i in range(len(self.WindowList)):
            subWindow = self.WindowList[i]
            if deletePos < 0:
                if subWindow.name == name:
                    deletePos = i
                    subWindow.close()
            else:
                subWindow.moveUp(self.pos.GetHigh())

        if deletePos >= 0:
            # 在储存列表/字典删除子窗口
            del self.WindowList[deletePos]
            del self.WindowMap[name]
            # 新窗口位置复位
            high = self.pos.GetHigh()
            self.pos.MoveUp(high)

    def addSubWindow(self):
        '''
        添加子窗口
        :return:
        '''
        name = self.mainTextEdit.toPlainText()
        if isinstance(name, str) and len(name) > 0 and name not in self.WindowMap.keys():
            # self.mainPushButton.setText(name)
            window = SubWindow(self.scrollAreaWidgetContents, name, self.pos, self.onDeleteSubWindow)
            self.WindowMap[name] = window
            self.WindowList.append(window)
            self.WindowMap[name].show()
            high = self.pos.GetHigh()
            self.pos.MoveDown(high)


if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication, QMainWindow
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # 等待用户退出
    sys.exit(app.exec_())
