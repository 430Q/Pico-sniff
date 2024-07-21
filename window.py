from Unit.Ui_window import *
from Unit.capThread import cap_package
from PyQt5 import QtCore, QtGui, QtWidgets
from Common.logcmd import printWARN , printTEST
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtChart import *
import socket
import time
from Protocol.handle_IP import IP


class WINGUI(QMainWindow):
    """docstring for window"""
    # cap_package_signal = pyqtSignal(list) 
    def __init__(self,parent=None):
        super(WINGUI, self).__init__(parent)
        self.ui = Ui_window()
        self.ui.setupUi(self)
        self.set_Png = True
        self.port = 0
        self.threatNum = 0
        self.threaTtype=0

        ##########package########
        self.list_package = []
        self.IP_list_tuple = []
        self.myIP = socket.gethostbyname(socket.gethostname())

        ##########线程#########
        self.Thread_cap = cap_package()
        self.Thread_cap.signal_packdict.connect(self.get_package)
        '''
        当 signal_packdict 信号被发射时，执行 self.get_package 方法，并将信号中的字典参数传递给该方法
            signal_packdict 是 cap_package 类中的一个信号（类型是 pyqtSignal(dict)），当这个信号被发射时，会传递一个字典类型的参数
            self.get_package 是一个槽函数，用于处理 signal_packdict 发射的信号
        '''
        self.Thread_cap.signal_iptuple.connect(self.show_IP)

        self.Thread_cap.signal_portstr.connect(self.show_flow)

        ##########Pull-Down list##########
        self.ui.cb.addItems(self.Thread_cap.getNIC())#更新下拉列表

        ##########page-table##########
        self.ui.tableWidget.setColumnCount(3)
        self.ui.tableWidget.horizontalHeader().setStretchLastSection(True);
        self.ui.tableWidget.setHorizontalHeaderLabels(['ID','Threat Level','Type'])#用Num对标起来
        self.ui.tableWidget.verticalHeader().setDefaultSectionSize(15)
        self.ui.tableWidget.setAlternatingRowColors(True);
        self.ui.tableWidget.verticalHeader().setHidden(True);
        ##########tree###########
        self.ui.treeWidget.setHeaderLabel("Protocol")

        ##########page3-table##########
        self.ui.tableWidget2.setColumnCount(3) # Time Type Level -> SrcIP DesIP Protocol Port Content
        self.ui.tableWidget2.horizontalHeader().setStretchLastSection(True);
        self.ui.tableWidget2.setHorizontalHeaderLabels(['ID', 'Threat Type','Threat Name'])
        self.ui.tableWidget2.verticalHeader().setDefaultSectionSize(15)
        self.ui.tableWidget2.setAlternatingRowColors(True);
        self.ui.tableWidget2.verticalHeader().setHidden(True);
        ##########tree###########
        self.ui.treeWidget2.setHeaderLabel("Detail")
        # self.ui.treeWidget.setHeaderLabel("Protocol")

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.show_time)

        self.m_chart = QChart();  
        self.chartView = QChartView(self.m_chart);  
        self.chartView.setRubberBand(QChartView.RectangleRubberBand);  

        self.m_series = QLineSeries()  
        self.m_chart.addSeries(self.m_series);  
      
        for i in range(10):  
           self.m_series.append(i,0)  
        
        self.m_series.setUseOpenGL(True)
      
        self.axisX = QValueAxis()
        self.axisX.setRange(0,10);  
        self.axisX.setLabelFormat("%g")  
        self.axisX.setTitleText("axisX")  
      
        self.axisY = QValueAxis()
        self.axisY.setRange(0,1000)
        self.axisX.setLabelFormat("%g") 
        self.axisY.setTitleText("axisY"); 
      
        self.m_chart.setAxisX(self.axisX, self.m_series)  
        self.m_chart.setAxisY(self.axisY, self.m_series)  
        self.m_chart.legend().hide();  
        self.m_chart.setTitle("Traffic Visualisation");
        
        self.ui.verticalLayout1.addWidget(self.chartView);

        self.timer.start(800)  
     


    ############# UI SLOT ################

    def capt(self):#Page1, 捕获数据包
        print("capt")
        '''capture package'''
        while self.ui.tableWidget.rowCount()>0:
            self.ui.tableWidget.removeRow(0)# 清空 tableWidget 中的所有行
        while self.ui.tableWidget2.rowCount()>0:
            self.ui.tableWidget2.removeRow(0)# 清空 tableWidget2 中的所有行
        name = self.ui.cb.currentText() #获取当前list的值
        print('device:',name)
        self.list_package.clear() # 清空 list_package 列表，准备存储新的捕获数据包
        self.Thread_cap.setstuid(eth_name = name)# 调用捕获线程对象的 setstuid 方法，传入获取的设备名称。此方法可能用于设置捕获线程的设备名称
        self.Thread_cap.change_status(0) # 调用捕获线程对象的 change_status 方法，传入 0。此方法可能用于更改捕获线程的状态，例如开始捕获
        time.sleep(0.5)
        # print(111)
        self.Thread_cap.restart() #Stop后重启抓包，重置标识位
        # print(222)
        # self.Thread_cap.start(self.packageNumber)# 启动捕获线程，开始捕获网络数据包
        self.Thread_cap.start()# 启动捕获线程，开始捕获网络数据包
        # print(333)
        self.ui.sbt.setEnabled(True) # 启用Stop按钮

    def stop(self):
        self.Thread_cap.stop()
        self.ui.sbt.setEnabled(False)


    def showPage(self, btn_id):# 处理页面切换
        self.ui.stackedWidget.setCurrentIndex(btn_id)
        try:
            self.Thread_cap.change_status(btn_id)
            self.ui.treeWidget.clear()
            self.ui.treeWidget2.clear()
            # while self.ui.tableWidget.rowCount()>0:
            #     self.ui.tableWidget.removeRow(0)
            self.ui.pbt.setEnabled(True) # 返回页面时按钮状态
            self.ui.lineEdit.clear()
            # self.list_package.clear()
        except:
            pass

    def treeShow(self, Item):
        self.ui.treeWidget.clear() # 清空 treeWidget 中的所有项，以准备显示新的数据

        row = self.ui.tableWidget.row(Item) # 获取当前点击的 tableWidget 项的行号
        try:
            eth = QTreeWidgetItem(self.ui.treeWidget, ['ethernet']); # 创建一个新的 QTreeWidgetItem，将其作为根节点，显示文本为 'ethernet'
            for key in self.list_package[row]['ethernet']:
                if key == 'frame_type':# 如果当前键是 'frame_type'，获取其值并创建一个新的 QTreeWidgetItem，显示键值对
                    curtype =  self.list_package[row]['ethernet'][key]
                    frame_type = QTreeWidgetItem(eth, [key+" : "+ curtype])
                    curtype = curtype[curtype.find(']')+1:] # 从 'frame_type' 值中提取类型名，假设值格式为 "[...]类型名"
                else:
                    QTreeWidgetItem(eth, [key+" : "+self.list_package[row]['ethernet'][key]]) # 对于其他键，创建新的 QTreeWidgetItem，显示键值对
            for key in self.list_package[row][curtype]:
                if key == 'IPv4_protocol' or key == 'IPv6_next_head': # 如果当前键是 'IPv4_protocol' 或 'IPv6_next_head'，获取其值并创建一个新的 QTreeWidgetItem，显示键值对
                    curTrans = self.list_package[row][curtype][key]
                    IP_type = QTreeWidgetItem(frame_type, [key+" : "+ curTrans])
                    curTrans = curTrans[curTrans.find(']')+1:] # 从 'IPv4_protocol' 或 'IPv6_next_head' 值中提取类型名，假设值格式为 "[...]类型名"。
                else:
                    QTreeWidgetItem(frame_type, [key+" : "+self.list_package[row][curtype][key]])  # 对于其他键，创建新的 QTreeWidgetItem，显示键值对
            for key in self.list_package[row][curTrans]:
                QTreeWidgetItem(IP_type, [key+" : "+self.list_package[row][curTrans][key]]) # 对于 curTrans 的每个键，创建新的 QTreeWidgetItem，显示键值对
        except:
            pass
        # self.list_package[row]['ethernet']

    def treeShow2(self, Item):
        self.ui.treeWidget2.clear()  # 清空 treeWidget 中的所有项，以准备显示新的数据

        row = self.ui.tableWidget2.row(Item)  # 获取当前点击的 tableWidget 项的行号
        try:

            PP = QTreeWidgetItem(self.ui.treeWidget2,[self.list_package[row]['TInfo']['msg']]);  # 创建一个新的 QTreeWidgetItem，将其作为根节点，显示文本为 'ethernet'
            # print(self.list_package) # [{'rawData': {'data': '0 c 29 5c 8a 25 0 50 56 e0 f9 6b 8 0 45 0 0 3c 9e 2b 0 0 80 1 45 63 d8 3a d4 ce c0 a8 e9 80 0 0 7b 43 0 2 da 16 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'time': 1720618992.737082}, 'ethernet': {'eth_dest_mac': '[48 bit]00:0C:29:5C:8A:25', 'eth_src_mac': '[48 bit]00:50:56:E0:F9:6B', 'frame_type': '[16 bit]IP'}, 'IP': {'version': '[4 bit]4', 'Internet head lenth': '[4 bit]5', 'Diff_service': '[6 bit]0', 'ECN': '[2 bit]0', 'total_length': '[16 bit]60', 'identification': '[16 bit]40491', 'flags': '[3 bit]0', 'offset': '[13 bit]0', 'TTL': '[8 bit]128', 'IPv4_protocol': '[8 bit]ICMP', 'checksum': '[16 bit]17763', 'SRC_IPv4': '[32 bit]216.58.212.206', 'DEST_IPv4': '[32 bit]192.168.233.128'}, 'ICMP': {'ICMP_type': "[16 bit]('Echo_reply', 0, 0)", 'checksum': '[16 bit]31555', 'ID': '[16 bit]2', 'sequence': '[16 bit]55830'}, 'TInfo': {'msg': 'PROTOCOL-ICMP Stacheldraht server spoof', 'Ttype': 'attempted-dos', 'TLevel': 'Waring'}}, {'rawData': {'data': '0 c 29 5c 8a 25 0 50 56 e0 f9 6b 8 0 45 0 0 3c 9e 2b 0 0 80 1 45 63 d8 3a d4 ce c0 a8 e9 80 0 0 7b 43 0 2 da 16 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'time': 1720618992.737082}, 'ethernet': {'eth_dest_mac': '[48 bit]00:0C:29:5C:8A:25', 'eth_src_mac': '[48 bit]00:50:56:E0:F9:6B', 'frame_type': '[16 bit]IP'}, 'IP': {'version': '[4 bit]4', 'Internet head lenth': '[4 bit]5', 'Diff_service': '[6 bit]0', 'ECN': '[2 bit]0', 'total_length': '[16 bit]60', 'identification': '[16 bit]40491', 'flags': '[3 bit]0', 'offset': '[13 bit]0', 'TTL': '[8 bit]128', 'IPv4_protocol': '[8 bit]ICMP', 'checksum': '[16 bit]17763', 'SRC_IPv4': '[32 bit]216.58.212.206', 'DEST_IPv4': '[32 bit]192.168.233.128'}, 'ICMP': {'ICMP_type': "[16 bit]('Echo_reply', 0, 0)", 'checksum': '[16 bit]31555', 'ID': '[16 bit]2', 'sequence': '[16 bit]55830'}, 'TInfo': {'msg': 'PROTOCOL-ICMP Stacheldraht server spoof', 'Ttype': 'attempted-dos', 'TLevel': 'Waring'}}]
# [{'rawData': {'data': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c af d9 0 0 80 1 0 0 c0 a8 e9 80 d8 3a d4 ce 8 0 71 44 0 2 dc 15 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'time': 1720619517.197693}, 'ethernet': {'eth_dest_mac': '[48 bit]00:50:56:E0:F9:6B', 'eth_src_mac': '[48 bit]00:0C:29:5C:8A:25', 'frame_type': '[16 bit]IP'}, 'IP': {'version': '[4 bit]4', 'Internet head lenth': '[4 bit]5', 'Diff_service': '[6 bit]0', 'ECN': '[2 bit]0', 'total_length': '[16 bit]60', 'identification': '[16 bit]45017', 'flags': '[3 bit]0', 'offset': '[13 bit]0', 'TTL': '[8 bit]128', 'IPv4_protocol': '[8 bit]ICMP', 'checksum': '[16 bit]0', 'SRC_IPv4': '[32 bit]192.168.233.128', 'DEST_IPv4': '[32 bit]216.58.212.206'}, 'ICMP': {'ICMP_type': "[16 bit]('Echo_request_(used_to_ping)', 8, 0)", 'checksum': '[16 bit]28996', 'ID': '[16 bit]2', 'sequence': '[16 bit]56341'}, 'TInfo': {'payload': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c af d9 0 0 80 1 0 0 c0 a8 e9 80 d8 3a d4 ce 8 0 71 44 0 2 dc 15 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'srcIP': '192.168.233.128', 'desIP': '216.58.212.206', 'Protocol': 'ICMP', 'itype': 8, 'icode': 0, 'msg': 'PROTOCOL-ICMP PING undefined code', 'Ttype': 'misc-activity', 'TLevel': 'Waring'}}, {'rawData': {'data': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c af d9 0 0 80 1 0 0 c0 a8 e9 80 d8 3a d4 ce 8 0 71 44 0 2 dc 15 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'time': 1720619517.197693}, 'ethernet': {'eth_dest_mac': '[48 bit]00:50:56:E0:F9:6B', 'eth_src_mac': '[48 bit]00:0C:29:5C:8A:25', 'frame_type': '[16 bit]IP'}, 'IP': {'version': '[4 bit]4', 'Internet head lenth': '[4 bit]5', 'Diff_service': '[6 bit]0', 'ECN': '[2 bit]0', 'total_length': '[16 bit]60', 'identification': '[16 bit]45017', 'flags': '[3 bit]0', 'offset': '[13 bit]0', 'TTL': '[8 bit]128', 'IPv4_protocol': '[8 bit]ICMP', 'checksum': '[16 bit]0', 'SRC_IPv4': '[32 bit]192.168.233.128', 'DEST_IPv4': '[32 bit]216.58.212.206'}, 'ICMP': {'ICMP_type': "[16 bit]('Echo_request_(used_to_ping)', 8, 0)", 'checksum': '[16 bit]28996', 'ID': '[16 bit]2', 'sequence': '[16 bit]56341'}, 'TInfo': {'payload': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c af d9 0 0 80 1 0 0 c0 a8 e9 80 d8 3a d4 ce 8 0 71 44 0 2 dc 15 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'srcIP': '192.168.233.128', 'desIP': '216.58.212.206', 'Protocol': 'ICMP', 'itype': 8, 'icode': 0, 'msg': 'PROTOCOL-ICMP PING undefined code', 'Ttype': 'misc-activity', 'TLevel': 'Waring'}}, {'rawData': {'data': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c af d9 0 0 80 1 0 0 c0 a8 e9 80 d8 3a d4 ce 8 0 71 44 0 2 dc 15 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'time': 1720619517.197693}, 'ethernet': {'eth_dest_mac': '[48 bit]00:50:56:E0:F9:6B', 'eth_src_mac': '[48 bit]00:0C:29:5C:8A:25', 'frame_type': '[16 bit]IP'}, 'IP': {'version': '[4 bit]4', 'Internet head lenth': '[4 bit]5', 'Diff_service': '[6 bit]0', 'ECN': '[2 bit]0', 'total_length': '[16 bit]60', 'identification': '[16 bit]45017', 'flags': '[3 bit]0', 'offset': '[13 bit]0', 'TTL': '[8 bit]128', 'IPv4_protocol': '[8 bit]ICMP', 'checksum': '[16 bit]0', 'SRC_IPv4': '[32 bit]192.168.233.128', 'DEST_IPv4': '[32 bit]216.58.212.206'}, 'ICMP': {'ICMP_type': "[16 bit]('Echo_request_(used_to_ping)', 8, 0)", 'checksum': '[16 bit]28996', 'ID': '[16 bit]2', 'sequence': '[16 bit]56341'}, 'TInfo': {'payload': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c af d9 0 0 80 1 0 0 c0 a8 e9 80 d8 3a d4 ce 8 0 71 44 0 2 dc 15 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'srcIP': '192.168.233.128', 'desIP': '216.58.212.206', 'Protocol': 'ICMP', 'itype': 8, 'icode': 0, 'msg': 'PROTOCOL-ICMP PING undefined code', 'Ttype': 'misc-activity', 'TLevel': 'Waring'}}, {'rawData': {'data': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c af d9 0 0 80 1 0 0 c0 a8 e9 80 d8 3a d4 ce 8 0 71 44 0 2 dc 15 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'time': 1720619517.197693}, 'ethernet': {'eth_dest_mac': '[48 bit]00:50:56:E0:F9:6B', 'eth_src_mac': '[48 bit]00:0C:29:5C:8A:25', 'frame_type': '[16 bit]IP'}, 'IP': {'version': '[4 bit]4', 'Internet head lenth': '[4 bit]5', 'Diff_service': '[6 bit]0', 'ECN': '[2 bit]0', 'total_length': '[16 bit]60', 'identification': '[16 bit]45017', 'flags': '[3 bit]0', 'offset': '[13 bit]0', 'TTL': '[8 bit]128', 'IPv4_protocol': '[8 bit]ICMP', 'checksum': '[16 bit]0', 'SRC_IPv4': '[32 bit]192.168.233.128', 'DEST_IPv4': '[32 bit]216.58.212.206'}, 'ICMP': {'ICMP_type': "[16 bit]('Echo_request_(used_to_ping)', 8, 0)", 'checksum': '[16 bit]28996', 'ID': '[16 bit]2', 'sequence': '[16 bit]56341'}, 'TInfo': {'payload': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c af d9 0 0 80 1 0 0 c0 a8 e9 80 d8 3a d4 ce 8 0 71 44 0 2 dc 15 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'srcIP': '192.168.233.128', 'desIP': '216.58.212.206', 'Protocol': 'ICMP', 'itype': 8, 'icode': 0, 'msg': 'PROTOCOL-ICMP PING undefined code', 'Ttype': 'misc-activity', 'TLevel': 'Waring'}}, {'rawData': {'data': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c af d9 0 0 80 1 0 0 c0 a8 e9 80 d8 3a d4 ce 8 0 71 44 0 2 dc 15 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'time': 1720619517.197693}, 'ethernet': {'eth_dest_mac': '[48 bit]00:50:56:E0:F9:6B', 'eth_src_mac': '[48 bit]00:0C:29:5C:8A:25', 'frame_type': '[16 bit]IP'}, 'IP': {'version': '[4 bit]4', 'Internet head lenth': '[4 bit]5', 'Diff_service': '[6 bit]0', 'ECN': '[2 bit]0', 'total_length': '[16 bit]60', 'identification': '[16 bit]45017', 'flags': '[3 bit]0', 'offset': '[13 bit]0', 'TTL': '[8 bit]128', 'IPv4_protocol': '[8 bit]ICMP', 'checksum': '[16 bit]0', 'SRC_IPv4': '[32 bit]192.168.233.128', 'DEST_IPv4': '[32 bit]216.58.212.206'}, 'ICMP': {'ICMP_type': "[16 bit]('Echo_request_(used_to_ping)', 8, 0)", 'checksum': '[16 bit]28996', 'ID': '[16 bit]2', 'sequence': '[16 bit]56341'}, 'TInfo': {'payload': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c af d9 0 0 80 1 0 0 c0 a8 e9 80 d8 3a d4 ce 8 0 71 44 0 2 dc 15 61 62 63 64 65 66 67 68 69 6a 6b 6c 6d 6e 6f 70 71 72 73 74 75 76 77 61 62 63 64 65 66 67 68 69 ', 'srcIP': '192.168.233.128', 'desIP': '216.58.212.206', 'Protocol': 'ICMP', 'itype': 8, 'icode': 0, 'msg': 'PROTOCOL-ICMP PING undefined code', 'Ttype': 'misc-activity', 'TLevel': 'Waring'}}]
            for key in self.list_package[row]['TInfo']:
                QTreeWidgetItem(PP, [key + " : " + self.list_package[row]['TInfo'][key]])

            # for key in self.list_package[row][curtype]:
            #     if key == 'IPv4_protocol' or key == 'IPv6_next_head':  # 如果当前键是 'IPv4_protocol' 或 'IPv6_next_head'，获取其值并创建一个新的 QTreeWidgetItem，显示键值对
            #         curTrans = self.list_package[row][curtype][key]
            #         IP_type = QTreeWidgetItem(frame_type, [key + " : " + curTrans])
            #         curTrans = curTrans[curTrans.find(
            #             ']') + 1:]  # 从 'IPv4_protocol' 或 'IPv6_next_head' 值中提取类型名，假设值格式为 "[...]类型名"。
            #     else:
            #         QTreeWidgetItem(frame_type, [
            #             key + " : " + self.list_package[row][curtype][key]])  # 对于其他键，创建新的 QTreeWidgetItem，显示键值对
            # for key in self.list_package[row][curTrans]:
            #     QTreeWidgetItem(IP_type, [key + " : " + self.list_package[row][curTrans][
            #         key]])  # 对于 curTrans 的每个键，创建新的 QTreeWidgetItem，显示键值对
        except:
            pass
        # self.list_package[row]['ethernet']

    ############ thread slot #############
    def get_package(self, package_dict): # 傳入數據包到前端頁面 觸發條件為判斷是str/dic/tuple
        print(f"get_package()")
        # print(f"package_dict:{package_dict}")
        '''
        package_dict:{'rawData': {'data': '0 50 56 e0 f9 6b 0 c 29 5c 8a 25 8 0 45 0 0 3c 26 73 0 0 80 11 0 0 c0 a8 e9 80 c0 a8 e9 2 e8 e7 0 35 0 28 54 e 87 af 1 0 0 1 0 0 0 0 0 0 3 77 77 77 6 67 6f 6f 67 6c 65 3 63 6f 6d 0 0 1 0 1 ', 'time': 1720606489.23598}, 'ethernet': {'eth_dest_mac': '[48 bit]00:50:56:E0:F9:6B', 'eth_src_mac': '[48 bit]00:0C:29:5C:8A:25', 'frame_type': '[16 bit]IP'}, 'IP': {'version': '[4 bit]4', 'Internet head lenth': '[4 bit]5', 'Diff_service': '[6 bit]0', 'ECN': '[2 bit]0', 'total_length': '[16 bit]60', 'identification': '[16 bit]9843', 'flags': '[3 bit]0', 'offset': '[13 bit]0', 'TTL': '[8 bit]128', 'IPv4_protocol': '[8 bit]UDP', 'checksum': '[16 bit]0', 'SRC_IPv4': '[32 bit]192.168.233.128', 'DEST_IPv4': '[32 bit]192.168.233.2'}, 'UDP': {'SRC_PORT': '[16 bit]59623', 'DEST_PORT': '[16 bit]53', 'length': '[16 bit]40', 'checksum': '[16 bit]21518'}, 'TInfo': {}}

        '''
        self.list_package.append(package_dict) #将 package_dict 添加到 self.list_package 列表中。package_dict 可能是一个包含数据包信息的字典
        # print(f"package_dict:{package_dict}")
        self.ui.statusbar.showMessage(f"Threat Number:  {self.threatNum}", 1500); # programing
        # Page1
        row_count = self.ui.tableWidget.rowCount()# 获取当前表格中的行数。这一行用于确定新数据包插入的位置
        self.ui.tableWidget.insertRow(row_count)  # 在表格的末尾插入一行。row_count 是当前行数，因此新行将插入在最后一行的位置
        # print(111)
        self.ui.tableWidget.setItem(row_count, 0, QTableWidgetItem(str(self.Thread_cap.ID)))
        # print(222)
        self.ui.tableWidget.setItem(row_count, 1, QTableWidgetItem(str(package_dict['TInfo']['TLevel'])))
        # print(333)
        self.ui.tableWidget.setItem(row_count, 2, QTableWidgetItem(str(self.Thread_cap.Protocol)))
        # print(444)

        # Page3
        row_count3 = self.ui.tableWidget2.rowCount()  # 获取当前表格中的行数。这一行用于确定新数据包插入的位置
        # print(555)
        if package_dict['TInfo']['TLevel'] == "Waring":
            self.ui.tableWidget2.insertRow(row_count3)  # 在表格的末尾插入一行。row_count 是当前行数，因此新行将插入在最后一行的位置
            # print(666)
            self.ui.tableWidget2.setItem(row_count3, 0, QTableWidgetItem(str(self.Thread_cap.ID)))
            # print(777)
            self.ui.tableWidget2.setItem(row_count3, 1, QTableWidgetItem(str(package_dict['TInfo']['Ttype']))) # TType
            print(package_dict['TInfo']['Ttype'])
            # print(888)
            self.ui.tableWidget2.setItem(row_count3, 2, QTableWidgetItem(str(package_dict['TInfo']['msg']))) # msg
            print(package_dict['TInfo']['msg'])

        self.Thread_cap.ID+=1


    def show_IP(self, IP_tuple):
        print("show_IP()")
        if str(self.myIP) in IP_tuple:
            self.IP_list_tuple.append(IP_tuple)
            printWARN("IP_tuple"+str(len(self.IP_list_tuple)))
            if len(self.IP_list_tuple) >= 100 and self.set_Png:
                self.set_Png == False  
                # self.Thread_cap.stop()
                self.Image.setIP(self.IP_list_tuple[:100], self.myIP)


    def show_flow(self,port):
        print(f"show_flow()")
        self.port += 1

    def show_time(self): # 实时更新图表数据
        # dataTime = QTime(QTime.currentTime())
        # eltime = dataTime.elapsed()
        # lastpointtime = 0
        # size = eltime - lastpointtime
        size = 1
        # printWARN(str(self.port))
        oldPoints = self.m_series.pointsVector()
        points = []
        for i in range(1,len(oldPoints)): 
            points.append(QPointF(i-size ,oldPoints[i].y()))
        sizePoints = len(points)
        for k in range(size): 
            points.append(QPointF(k+sizePoints, self.port));  
        self.m_series.replace(points) 
        self.port = 0
        self.timer.start(800)


        
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = WINGUI()
    win.show()
    sys.exit(app.exec_())
