import os
import pickle

info = {}
f = open('icmpv6-parameters-2.csv', 'r')
for line in f.readlines():
    l = line.split(',')
    try:
        info[int(l[0],10)] = l[1]
    except:
        pass
f.close()
pickle.dump(info,open('IPv6_IcmpType','wb'))