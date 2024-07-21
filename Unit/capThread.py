from PyQt5.QtCore import *
import pcap
import time
from Protocol import handle_Ftype_factory
from Common.logcmd import printINFO, printTEST, printWARN
from Common.address import get_raw_data
from EthFrame.extra_Ethernet import extra_Ethernet
import socket
from idstools import rule
import pickle

# 以太网帧 工厂模式
FrameType = handle_Ftype_factory()

class cap_package(QThread):
    signal_packdict = pyqtSignal(dict) # 包
    signal_iptuple = pyqtSignal(tuple) # IP
    signal_portstr = pyqtSignal(str) # port
    def __init__(self, parent = None):
        super(cap_package, self).__init__(parent)
        self.package = []
        self.is_stop = False
        self.myIP = socket.gethostbyname(socket.gethostname())
        self.Protocol = ""
        self.threatRuleFile="./Rule/snort3-community.rules"
        self.ID=0
        

    def stop(self):
        printWARN("STOP Thred")
        self.is_stop = True

    def restart(self):
        printWARN("RESTART Thred")
        self.ID = 0
        self.is_stop = False

    def change_status(self, cur):
        self.status = cur

    def threatDected(self,package): # 數據包格式匹配
        print("threatDected")
        # print(f"threatDected_pac:{package}")
        msg=None
        Ttype=None
        TLevel=None
        payloads=[]
        rule = self.match_rules(package)
        print(f"Rule:{rule}")
        if not rule == None:
            msg=rule[0]
            Ttype=rule[1]
            payloads=rule[2]
        if Ttype == None:
            TLevel = "Normal"
        else:
            TLevel = "Waring"
        print(f"ID:{self.ID}")
        print(f"msg:{msg}")
        print(f"Ttype:{Ttype}")
        return (str(msg),str(Ttype),TLevel,payloads)


    def match_rules(self,Package):
        print(f"match_rules()")
        '''
        Threat Level:classtype
        Payload: content
        Protocol:proto
        srcIP:source IP
        srcPort:source port
        destIP:destination IP
        destPort:destination port
        Threat Name:msg
        ICMP
            option:itype：匹配ICMP类型。
            option:icode：匹配ICMP代码
            alert icmp $EXTERNAL_NET any -> $HOME_NET any ( msg:"PROTOCOL-ICMP PING undefined code"; icode:>0; itype:8; metadata:ruleset community; classtype:misc-activity; sid:365; rev:11; )
        定位：
            content：匹配数据包中的特定内容。
            offset：指定搜索内容的起始位置。
            depth：限制搜索内容的结束位置

        '''

        if Package['Protocol'] == 'ICMP':
            print(f"Pack_ICMP")
            for erule in rule.parse_file(self.threatRuleFile):# https://idstools.readthedocs.io/en/latest/apidoc/idstools.rule.html
                # print(f"erule:{erule}")
                # 标志位重置 when新的一条
                content_match=None
                payload=None
                itype_match=None
                content_flag = False  # 判断是否存在content字段
                if erule.proto == 'icmp':
                    print(f"Proto_ICMP")
                    for option in erule.options: # 匹配option中的数据类型
                        # print(f"option:{option}")
                        if option['name'] == 'itype':
                            # print(f"option['value']:{option['value']},{type(option['value'])}")
                            # print(f"Package['itype']:{Package['itype']},{type(Package['itype'])}")
                            if int(option['value']) == Package['itype']:
                                # print(f"itype=Ture")
                                itype_match=True
                        if option['name'] == 'content':
                            print(f"content_flag=True")
                            content_flag=True
                            # print(f"option['name']:{option['name']}{type(option['name'])},option['value']:{option['value']}{type(option['value'])}")
                            # print(f"Package['payload']:{Package['payload']}{type(Package['payload'])}")
                            if option['value'] in Package['rawData']:# Package['payload']是二进制，没有解码，应该匹配不到！！！！ programing
                                print(f"content=Ture")
                                content_match = True
                                payload=option['value']
                                # print(f"content_match_detail:{payload}")



                    if itype_match and content_match:
                        print(f"itype_match & content_match")
                        print(f"ThreatItem:{(str(erule['msg']),str(erule['classtype']))}")
                        return (str(erule['msg']),str(erule['classtype']),payload)
                    if itype_match and content_flag==False:
                        print(f"itype_match")
                        print(f"ThreatItem:{(str(erule['msg']), str(erule['classtype']))}")
                        return (str(erule['msg']), str(erule['classtype']),payload) # classtype:Page1-threat level
        else:
            return None

                    # alert icmp $EXTERNAL_NET any -> $HOME_NET any ( msg:"PROTOCOL-ICMP PING undefined code"; icode:>0; itype:8; metadata:ruleset community; classtype:misc-activity; sid:365; rev:11; )
                    # 365 || PROTOCOL-ICMP PING undefined code

    def run(self):
        print('caping')
        Info = {}
        TInfo={} # Threat package format
        src_dest_ip = None
        src_dest_port = None
        port = None

        try:
            pc = pcap.pcap(self.eth_name,timeout_ms=50) #使用 pcap 初始化捕获接口 pc，并指定超时时间 timeout_ms=1 毫秒
        except Exception as e:
            print(f"Error:{e}")
            self.signal_error.emit(f"Invalid network interface: {self.eth_name}")
            return
        # print(f"Packages::{pc}") #Packages::<pcap._pcap.pcap object at 0x000001DE84850850>
        for ts, pkt in pc:  #循环从捕获接口 pc 中获取数据包，每个数据包包含时间戳 ts 和数据包内容 pkt
            if self.is_stop:#检查是否停止抓包
                break
            # print(f"ts::{ts}")
            # print(f"pkt::{pkt}")
            # 将原始数据和时间戳存储在 Info['rawData'] 字典中
            Info['rawData'] = {}
            Info['rawData']['data'] = get_raw_data(pkt)
            TInfo['rawData']=Info['rawData']['data']

            Info['rawData']['time'] = ts
            # print(Info['rawData']['time'])
            # 解码以太网帧，并打印解码信息
            eth = extra_Ethernet(pkt)
            printINFO("Decode Ethernet：")
            print('Destination: {}, Source: {}, Protocol: {}'.format(eth.dest_mac, eth.src_mac, eth.ftype))
            
            # 将以太网信息存储在 Info['ethernet'] 字典中
            Info['ethernet'] = eth.get_Info()

            cur_frame = FrameType.factor_Frame_Type(eth.ftype, eth.other_data)# 根据以太网帧类型进一步解析数据
            # print(f"cur_frame:{cur_frame}")# cur_frame:<Protocol.handle_IP.IP object at 0x000001DE8486E550>


            if cur_frame:
                curinfo = cur_frame.get_Info()
                # print(f"curinfo:{curinfo}") # curinfo:({'version': '[4 bit]4', 'Internet head lenth': '[4 bit]5', 'Diff_service': '[6 bit]0', 'ECN': '[2 bit]0', 'total_length': '[16 bit]60', 'identification': '[16 bit]36427', 'flags': '[3 bit]0', 'offset': '[13 bit]0', 'TTL': '[8 bit]128', 'IPv4_protocol': '[8 bit]ICMP', 'checksum': '[16 bit]0', 'SRC_IPv4': '[32 bit]192.168.233.128', 'DEST_IPv4': '[32 bit]142.250.179.238'}, 'IP')
                Info[curinfo[-1]] = curinfo[0] # Protocol type
                src_dest_ip = cur_frame.get_IP()
                # print(f"src_dest_ip:{src_dest_ip}")
                TInfo['srcIP']=src_dest_ip[0]
                TInfo['desIP']=src_dest_ip[1]

                printINFO(eth.ftype + " Data reporting & Data analysis：")
                self.Protocol = cur_frame.print_result()
                TInfo['Protocol']= self.Protocol
                # print(f"self.Protocol:{self.Protocol}")

                proto_data = cur_frame.deal_data() # 根據數據類型 進一步解析數據
                # print(f"proto_data:{proto_data}") # proto_data:<Protocol.underIP.UDP.UDP object at 0x000002BAB4F49E50>

                if not proto_data == None:
                    # print(111)
                    curinfo = proto_data.get_Info()
                    # tcurinfo = proto_data.
                    # print(f"curinfo[-1]:{curinfo[-1]}")
                    if not src_dest_ip == None and (curinfo[-1] == "TCP" or curinfo[-1] == "UDP"):
                        # print(f"self.myIP:{self.myIP}")
                        # print(f"src_dest_ip:{src_dest_ip}")
                        TInfo['itype'] = None
                        TInfo['icode'] = None
                        TInfo['srcPort'] = None
                        TInfo['destPort'] = None
                        src_dest_port = proto_data.print_result() #??为啥这里有，下面还要设置port为空
                        if src_dest_port:
                            # print(222)
                            TInfo['srcPort'] = src_dest_port[1]
                            TInfo['destPort'] = src_dest_port[2]
                        if self.myIP in src_dest_ip:
                            port = ""

                    if not src_dest_ip == None and curinfo[-1] == "ICMP":
                        # print(222)
                        icmpCode=proto_data.print_result()
                        TInfo['itype'] = icmpCode[1]
                        TInfo['icode'] = icmpCode[2]

                    Info[curinfo[-1]] = curinfo[0]
                    # print(f"Info[curinfo[-1]]:{Info[curinfo[-1]]}")

                    Trules = self.threatDected(TInfo)
                    # print(f"Trules:{Trules}")
                    # print(f"port:{port}{type(port)}")
                    TInfo['msg'] = Trules[0]
                    TInfo['Ttype'] = Trules[1]
                    TInfo['TLevel'] = Trules[2]
                    TInfo['payload'] = Trules[3]
                    Info['TInfo']=TInfo
                    print(f"Info['TInfo']:{Info['TInfo']}")


                    # print(f"Info['TInfo']['msg']:{Info['TInfo']['msg']}")
                    # print(f"Info['TInfo']['Ttype']:{Info['TInfo']['Ttype']}")
                    # print(444)




            # 控制输出
            if self.status == 0: #如果self.status等于0，表示当前状态是cap
                print("cap")
                # print(f"Info:{Info}")
                '''cap'''
                # print(f"port:{port}{type(port)}")
                # print(f"src_dest_ip:{src_dest_ip}")
                if not port == None : # 如果port不为None，发出signal_portstr信号，携带port信息
                    # print("signal_portstr")
                    self.signal_portstr.emit(port)
                    # print(f"Cap_port:{port},{type(port)}")
                    # TInfo['port']=port
                if not src_dest_ip == None : # 如果src_dest_ip不为None，发出signal_iptuple信号，携带src_dest_ip信息                    print("signal_portstr")
                    # print("signal_iptuple")
                    self.signal_iptuple.emit(src_dest_ip)
                # print(111)
                # print(f"Info:{Info}")
                self.signal_packdict.emit(Info) # 发出signal_packdict信号，携带Info字典
                # print(333)
                time.sleep(1)
            elif self.status == 1: # 如果self.status等于1，表示当前状态是flow
                print("flow")
                '''flow'''
                if not src_dest_ip == None : # 如果src_dest_ip不为None，发出signal_iptuple信号，携带src_dest_ip信息
                    # print("signal_iptuple")
                    self.signal_iptuple.emit(src_dest_ip)
                if not port == None : # 如果port不为None，发出signal_portstr信号，携带port信息
                    # print("signal_portstr")
                    self.signal_portstr.emit(port)
                    # print(f"Flow_port:{port}")

                self.signal_packdict.emit(Info) # 发出signal_packdict信号，携带Info字典
            else:# 如果self.status不是0或1，进行以下处理
                # print("self.status others")
                if self.is_stop: # 如果self.is_stop为True，则退出循环
                    # print(f"is_stop true")
                    break
                if not port == None : # 如果port不为None，发出signal_portstr信号，携带port信息
                    # print(f"signal_portstr")
                    self.signal_portstr.emit(port)
                    # print(f"N_port:{port}")

                    
                self.signal_packdict.emit(Info) # 发出signal_packdict信号，携带Info字典
                if src_dest_ip == None: # 如果src_dest_ip为None，继续下一个循环
                    continue
                self.signal_iptuple.emit(src_dest_ip) # 如果src_dest_ip为None，继续下一个循环
              
           
        
    def setstuid(self, eth_name = None):
        self.eth_name = eth_name

    def getNIC(self):
        interfaces = pcap.findalldevs()
        return interfaces


