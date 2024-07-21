'''
参数和实际意义的映射关系
'''
import pickle
import os

'''
ICMPTYPE = {
    'type(str)':{
        'code(str)': 'description(str)''
    }
}
'''
ICMPTYPE = pickle.load(open('Static/icmpType','rb'))

'''
IP_PROTOCOL={
    i(int): 'Protocol(str)'
}
'''
IP_PROTOCOL = pickle.load(open("Static/IPprotocol",'rb'))

'''
FRAME_TYPE={
    i(int): 'frame_type(str)'
}
'''
FRAME_TYPE = pickle.load(open("Static/FrameType", "rb"))

'''
ARP_OP={
    i(int): 'str'  
}
'''
ARP_OP = pickle.load(open('Static/arp_op','rb'))

'''
ARP_HARDWARE={
    int: 'str'
}
'''
ARP_HARDWARE = pickle.load(open('Static/arp_hardware','rb'))

'''
IPV6_ICMPTYPE ={
    int: str
}
'''
IPV6_ICMPTYPE = pickle.load(open('Static/IPv6_IcmpType','rb'))