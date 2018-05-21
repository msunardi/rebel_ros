# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''motion_analyzer.py

Author: msunardi
Created: 5/16/18

Given two input signals, find the distance matrix
'''
import numpy as np

sig_a = np.array([[1,3,4,9,8,2,1,5,7,3]])
sig_b = np.array([[1,6,2,3,0,9,4,3,6,3]])

#print(sig_a.shape)

#print(np.outer(sig_a, sig_b))

dim_a = sig_a.shape[1]
dim_b = sig_b.shape[1]

D = np.zeros((dim_a,dim_b))
#print(D)

case = 1
for i in range(dim_a):
    for j in range(dim_b):
        zoot = abs(sig_a[0, i] - sig_b[0, j])
        print("Indices: i={}, j={}".format(i,j))
        print("Signals: A {} x B {}".format(sig_a[0,i], sig_b[0,j]))
        print("zoot: {}".format(zoot))
        print("case: {}".format(case))
        if i == 0 and j == 0:
            D[i,j] = zoot
            case = 1
            
        elif i == 0:
            D[i,j] = zoot + D[0,j-1]
            case = 2
            print("D[0,{}]: {}".format(j, D[0,j-1]))            
        elif j == 0:
            D[i,j] = zoot + D[i-1,0]
            case = 3
            print("D[{},0]: {}".format(i, D[i-1,0]))
        else:
            D[i,j] = zoot + min([D[i-1,j-1], D[i-1,j], D[i, j-1]])
            case = 4
            print("D[i-1,j-1]: {}\nD[i-1,j]: {}\nD[j-1]: {}".format(D[i-1,j-1], D[i-1,j], D[i, j-1]))
        print("case: {}".format(case))
        print("D[i,j]: {}".format(D[i,j]))
        print(D)
#        input("Press enter to continue...")


# Start finding the matching pairs
# Always start with/include the corner value (N,N)
matching = [(dim_a-1,dim_b-1)]
matches = [D[dim_a-1,dim_b-1]]
k = dim_a-1
l = dim_b-1
while k >= 0 or l >= 0:
    if k == 0 and l == 0:
        mmin = (k,l)
        mmiin_dist = D[k,l]
        break
    
    elif k == 0 and l != 0:
        mmin = (k, l-1)
        mmiin_dist = D[k,l-1]
        l = l-1
    
    elif k != 0 and l == 0:
        mmin = (k-1, l)
        mmiin_dist = D[k-1,l]
        k = k-1
    else:
        
        mmiin_dist = D[k-1,l-1]
        mmin = (k-1, l-1)
        k_ = k-1
        l_ = l-1
        
        if D[k-1,l] < mmiin_dist:
            mmin = (k-1,l)
            mmiin_dist = D[k-1,l]
            l_ = l
        if D[k,l-1] < mmiin_dist:
            mmin = (k,l-1)
            mmiin_dist = D[k,l-1]
            k_ = k
        k = k_
        l = l_
        
    matching.append(mmin)
    matches.append(mmiin_dist)
        
print("Matching: {}".format(matching))
print("Matches: {}".format(matches))

nyoh = np.zeros_like(D)
for f, g in matching:
    nyoh[f,g] = 1.0
    
print("Nyoh: \n{}".format(nyoh))