# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_window.ui'
#
# Created by: PyQt5 UI code generator 5.10
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_window(object):

    def setupUi(self, window):
        window.setObjectName("window") # 定义窗口名字
        window.resize(600, 600)  # 设置窗口的对象名称和大小
        # 创建 centralwidget
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")  # 创建一个 centralwidget 并设置其对象名称centralwidget
        '''
        centralwidget 是必须设置的小部件，它充当了所有主窗口内容的容器。结构如下
                菜单栏（menuBar）：位于窗口的顶部，包含菜单选项。
                工具栏（toolBar）：位于菜单栏下方，包含工具按钮。
                中央小部件（centralWidget）：主窗口的中央区域，容纳主内容。
                状态栏（statusBar）：位于窗口的底部，显示状态信息 
        '''
        # 在 centralwidget 中添加布局和控件
        self.menu = QtWidgets.QWidget(self.centralwidget)
        self.menu.setGeometry(QtCore.QRect(0, 0, 151, 581)) # 设置菜单小部件其几何位置
        self.menu.setStyleSheet("QWidget#menu{\n"# 设置菜单小部件和按钮的样式
"background-color:rgb(66, 75, 111);\n"
"}\n"
"QPushButton{\n"
"border:none;\n"
"padding: 3px;\n"
"min-height: 60px;\n"
"background-color:rgb(66, 75, 111);\n"
"color: rgb(235, 235, 235)\n"
"}\n"
"QPushButton:hover{\n"
"border:none;\n"
"padding: 3px;\n"
"min-height: 60px;\n"
"background-color:rgb(87, 100, 156);\n"
"color:rgb(234, 234, 234);\n"
"font-size:15px\n"
"}\n"
"QPushButton:checked{\n"
"border:none;\n"
"padding: 3px;\n"
"min-height: 60px;\n"
"background-color:rgb(73, 74, 90);\n"
"color:rgb(234, 234, 234);\n"
"font-size:15px\n"
"}\n"
"")
        self.menu.setObjectName("menu")# 设置菜单栏小部件的对象名称
        # 创建一个垂直布局管理器，并将其设置为菜单的布局
        self.verticalLayout = QtWidgets.QVBoxLayout(self.menu)
        self.verticalLayout.setContentsMargins(0, 60, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        # 创建一个按钮 pac_pbt，并将其添加到菜单的垂直布局中:Capturing
        self.pac_pbt = QtWidgets.QPushButton(self.menu)
        self.pac_pbt.setObjectName("pac_pbt")
        self.verticalLayout.addWidget(self.pac_pbt)
        # 创建一个按钮 app_pbt，并将其添加到菜单的垂直布局中:Visualisation
        self.app_pbt = QtWidgets.QPushButton(self.menu)
        self.app_pbt.setObjectName("app_pbt")
        self.verticalLayout.addWidget(self.app_pbt)
        # 创建一个按钮 xxx_pbt，并将其添加到菜单的垂直布局中:XXX
        self.xxx_pbt = QtWidgets.QPushButton(self.menu)
        self.xxx_pbt.setObjectName("xxx_pbt")
        self.verticalLayout.addWidget(self.xxx_pbt)

        # 创建一个间隔项，并将其添加到垂直布局中，以填充剩余空间
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)

        #声明堆栈小部件
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        # 设置堆栈小部件的对象名称
        self.stackedWidget.setObjectName("stackedWidget")
        # 设置其几何位置。 左边的列表位置
        self.stackedWidget.setGeometry(QtCore.QRect(150, 0, 451, 581))
        self.stackedWidget.setStyleSheet("QWidget{\n"# 设置堆栈小部件和其内部子部件的样式
"background-color:rgb(205, 206, 222);\n"
"color:rgb(88, 83, 127);\n"
"}\n"
"QPushButton{\n"
"border:none;\n"
"border-radius: 3px;\n"
"padding: 3px;\n"
"min-width: 60px;\n"
"background-color:rgb(113, 135, 167);\n"
"color: rgb(235, 235, 235);\n"
"}\n"
"QPushButton:hover{\n"
"border:none;\n"
"padding: 3px;\n"
"min-width: 60px;\n"
"background-color:rgb(146, 171, 208);\n"
"color:rgb(234, 234, 234);\n"
"}\n"
"QPushButton:disabled{\n"
"border:none;\n"
"padding: 3px;\n"
"min-height: 60px;\n"
"background-color:rgb(73, 74, 90);\n"
"}\n"
"QComboBox{\n"
"border: 1px solid rgb(88, 83, 127);\n"
"border-radius: 3px;\n"
"padding: 3px;\n"
"\n"
"color: rgb(88, 83, 127);\n"
"}\n"
"QComboBox:hover{\n"
"border: 1px solid rgb(148, 81, 108);\n"
"border-radius: 3px;\n"
"padding: 3px;\n"
"\n"
"color: rgb(194, 124, 123);\n"
"}\n"
"QTableWidget{\n"
"alternate-background-color: rgb(126, 152, 174);\n"
# "background-color: rgb(148, 137, 169);\n"
"color: rgb(250, 250, 250);\n"
"}\n"
"QTableWidget::item:!alternate{\n"
# "alternate-background-color: rgb(126, 152, 174);\n"
"background-color: rgb(148, 137, 169);\n"
"color: rgb(250, 250, 250);\n"
"}\n"
"QScrollBar{\n"
"background:rgb(73, 74, 90,50);\n"
"height:10px;"
"}\n"
"QScrollBar::handle{background:lightgray; border:2px solid transparent; border-radius:5px;}"
"")

        # 创建第一个页面，并设置其对象名称 Capturing这个页面
        self.page = QtWidgets.QWidget()
        self.page.setObjectName("page")
        # 创建一个用于包含水平布局的部件，并设置其几何位置和对象名称
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.page)
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(20, 30, 421, 32)) # NIC device name内块的框框
        # 创建一个水平布局管理器，并将其设置为 horizontalLayoutWidget 的布局
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        # 创建一个标签，并将其添加到水平布局中
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)


        # 创建下拉列表空间并加入水平布局中
        self.cb = QtWidgets.QComboBox()
        self.horizontalLayout.addWidget(self.cb)
        # 创建一个按钮 pbt，并将其添加到水平布局中 Start
        self.pbt = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.pbt.setMinimumSize(QtCore.QSize(66, 0))
        self.pbt.setObjectName("pbt")
        self.horizontalLayout.addWidget(self.pbt)
        # 创建一个按钮 sbt，并将其添加到水平布局中 Stop
        self.sbt = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.sbt.setMinimumSize(QtCore.QSize(172, 0))
        self.sbt.setObjectName("sbt")
        self.horizontalLayout.addWidget(self.sbt)
        # 创建一个 QTreeWidget 部件并将其添加到 self.page 页面。设置它的几何位置和对象名称，并设置它的表头文本为 "1"
        self.treeWidget = QtWidgets.QTreeWidget(self.page)
        self.treeWidget.setGeometry(QtCore.QRect(20, 340, 421, 221))##Protocol那个框
        self.treeWidget.setObjectName("treeWidget")
        self.treeWidget.headerItem().setText(0, "1")
        # 创建一个 QFrame 部件，用于在页面中绘制一条水平线。设置它的几何位置、形状和阴影效果，并设置对象名称。 中间内条线
        self.line = QtWidgets.QFrame(self.page)
        self.line.setGeometry(QtCore.QRect(20, 310, 421, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        # 创建一个 QTableWidget 部件并将其添加到 self.page 页面。设置它的几何位置、编辑触发器、选择模式和行为。设置对象名称、列数和行数. Time的那个框
        self.tableWidget = QtWidgets.QTableWidget(self.page)
        self.tableWidget.setGeometry(QtCore.QRect(20, 70, 421, 231))
        self.tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        # 将 self.page 页面添加到堆栈小部件（QStackedWidget）中
        self.stackedWidget.addWidget(self.page)

        # 创建第二个页面（page_2）和一个子部件 chart_widget，并设置它们的对象名称和几何位置 Vistulisation这个页面
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.chart_widget = QtWidgets.QWidget(self.page_2)
        self.chart_widget.setGeometry(QtCore.QRect(40, 40, 381, 501))
        self.chart_widget.setObjectName("chart_widget")
        # 创建一个垂直布局（QVBoxLayout）并将其设置为 chart_widget 的布局管理器。设置布局的边距和间距
        self.verticalLayout1 = QtWidgets.QVBoxLayout(self.chart_widget)
        self.verticalLayout1.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout1.setSpacing(0)
        self.verticalLayout1.setObjectName("verticalLayout1")

        # 将第二个页面（page_2）添加到堆栈小部件（QStackedWidget）中
        self.stackedWidget.addWidget(self.page_2)

        # 创建第三个页面（page_3）和一个标签（xxx_label），并设置它们的对象名称和几何位置 XXX这个页面
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setObjectName("page_3")

        # 创建一个 QTableWidget 部件并将其添加到 self.page_3 页面。设置它的几何位置、编辑触发器、选择模式和行为。设置对象名称、列数和行数. Time的那个框
        self.tableWidget2 = QtWidgets.QTableWidget(self.page_3)
        self.tableWidget2.setGeometry(QtCore.QRect(20, 70, 421, 231))
        self.tableWidget2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableWidget2.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget2.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget2.setObjectName("tableWidget2")
        self.tableWidget2.setColumnCount(0)
        self.tableWidget2.setRowCount(0)
        # 创建一个 QFrame 部件，用于在页面中绘制一条水平线。设置它的几何位置、形状和阴影效果，并设置对象名称。 中间内条线
        self.line = QtWidgets.QFrame(self.page)
        self.line.setGeometry(QtCore.QRect(20, 310, 421, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        # 创建一个 QTreeWidget 部件并将其添加到 self.page_3 页面。设置它的几何位置和对象名称，并设置它的表头文本为 "1"
        self.treeWidget2 = QtWidgets.QTreeWidget(self.page_3)
        self.treeWidget2.setGeometry(QtCore.QRect(20, 340, 421, 221))  ##IP那个框
        self.treeWidget2.setObjectName("treeWidget2")
        self.treeWidget2.headerItem().setText(0, "1")

        # 将第三个页面（page_3）添加到堆栈小部件（QStackedWidget）中
        self.stackedWidget.addWidget(self.page_3)

        # 将 centralwidget 设置为主窗口的中央小部件
        window.setCentralWidget(self.centralwidget)
        # 创建一个状态栏（QStatusBar）并设置它的对象名称。将其设置为主窗口的状态栏。 状态栏是窗口底部的一条水平区域，用于显示一些简短的提示信息
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)

        # 创建一个按钮组（QButtonGroup），并将三个按钮（pac_pbt, app_pbt, xxx_pbt）添加到按钮组中，并为每个按钮分配一个 ID
        self.groubbtn = QtWidgets.QButtonGroup()
        self.groubbtn.addButton(self.pac_pbt, 0)
        self.groubbtn.addButton(self.app_pbt, 1)
        self.groubbtn.addButton(self.xxx_pbt, 2)
        # 设置三个按钮为可选中状态（Checkable）
        self.pac_pbt.setCheckable(True)
        self.xxx_pbt.setCheckable(True)
        self.app_pbt.setCheckable(True)
        # 调用 retranslateUi 方法，将所有部件的文本翻译为当前语言环境的语言
        self.retranslateUi(window)
        # 设置堆栈小部件的当前索引为 0，即显示第一个页面（page）
        self.stackedWidget.setCurrentIndex(0)
        # 设置 pbt 按钮为不可用状态. 输入完NIC才能使用
        self.pbt.setEnabled(True)
        self.sbt.setEnabled(False)

        # UI与实际功能链接
        # 将 pbt 按钮的 clicked 信号连接到 window 的 capt 槽函数
        self.pbt.clicked.connect(window.capt)
        # 将 sbt 按钮的 clicked 信号连接到 window 的 stop 槽函数
        self.sbt.clicked.connect(window.stop)
        # 将按钮组（groubbtn）的 buttonClicked 信号连接到 window 的 showPage 槽函数
        self.groubbtn.buttonClicked['int'].connect(window.showPage)

        # 将 tableWidget 的 itemClicked 信号连接到 window 的 treeShow 槽函数
        self.tableWidget.itemClicked.connect(window.treeShow)
        self.tableWidget2.itemClicked.connect(window.treeShow2)

        # 使用 Qt 的元对象系统自动连接信号和槽
        QtCore.QMetaObject.connectSlotsByName(window)
        
    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "Picosniff"))
        self.pac_pbt.setText(_translate("window", "Capturing"))
        self.app_pbt.setText(_translate("window", "Visualisation"))
        self.xxx_pbt.setText(_translate("window", "Threat"))
        self.label.setText(_translate("window", "Choice a NIC Device"))
        self.pbt.setText(_translate("window", "Start"))
        self.sbt.setText(_translate("window", "Stop"))
        # self.xxx_label.setText(_translate("window", "map"))

