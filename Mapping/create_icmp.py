'''数据源不稳定'''
import os
import pickle
info = {}
with open('icmpType','r') as f:
    for line in f.readlines():
        print(line)
        ty, code, mm = line.split(',')
        print(f"ty:{ty},code:{code},mm:{mm}")
        if not ty in info.keys():
            info[ty] = {}
        
        info[ty][code] = mm.replace('\n','')
        print()
for i in range(42, 253):
    if not str(i) in info.keys():
        info[str(i)] = {}
    info[str(i)]['x'] = 'Reserved'
for i in range(20, 30):
    if not str(i) in info.keys():
        info[str(i)] = {}
    info[str(i)]['x'] = 'Reserved_for_robustness_experiment'
f = open('icmpType','wb')
pickle.dump(info, f)
f.close()
