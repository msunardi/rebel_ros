# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''dynamic_time_warping.py

Author: msunardi
Created: 5/20/18

Given two input signals, find the distance matrix
'''
import numpy as np
import matplotlib.pyplot as plt

sig_a = np.array([[1,3,4,9,8,2,1,5,7,3]])
sig_b = np.array([[1,6,2,3,0,9,4,3,6,3]])

#print(sig_a.shape)

#print(np.outer(sig_a, sig_b))

def nyohnyoh(nsig_a, nsig_b):
    dim_a = nsig_a.shape[1]
    dim_b = nsig_b.shape[1]
    
    D = np.zeros((dim_a,dim_b))
    #print(D)
    
    case = 1
    for i in range(dim_a):
        for j in range(dim_b):
            zoot = abs(nsig_a[0, i] - nsig_b[0, j])
            print("Indices: i={}, j={}".format(i,j))
            print("Signals: A {} x B {}".format(nsig_a[0,i], nsig_b[0,j]))
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
    sig_warped = []
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
    nyohd = np.multiply(nyoh, D)
    print("Nyoh X D: \n{}".format(np.flip(nyohd,0)))
    return D, nyohd, matching, matches

#f, (ax1, ax2) = plt.subplots(2)
#ax1.plot(sig_a[0])
#ax2.plot(sig_b[0])

def construct_warped(distance_matrix, sig1, sig2, matching):
    prev = None
    warped = []
    insertion = []
    deletion = []
    history = []
    for m in matching:
        print(m)
        if not prev:
            warped.append(sig2[0,m[1]])
            
        else:
            print("Prev: {}".format(prev))
            if m[0]==prev[0]-1 and m[1]==prev[1]-1:
                if insertion:
                    history.append(insertion)
#                    insertion.append(sig2[0,m[1]])
                    x = np.mean(insertion)
                    warped.append(x)
                    print("Insertion: {} = {}".format(insertion, x))                    
                    insertion = []
                    
                if deletion:
                    history.append(deletion)
#                    deletion.append(sig2[0,m[1]])
                    x = np.mean(deletion)
                    print("Deletion: {} = {}".format(deletion, x))
                    warped.append(x)
                    deletion = []
                    
                warped.append(sig2[0,m[1]])
                print("Warped: {}".format(warped))
                history.append([sig2[0,m[1]]])
                
            elif m[0]==prev[0] and m[1]==prev[1]-1:
                print("Insertion!")
                insertion.append(sig2[0,m[1]])
                
            elif m[0]==prev[0]-1 and m[1]==prev[1]:
                print("Deletion!")
                deletion.append(sig2[0,m[1]])
        prev = m
    else:
        if insertion:
            x = np.mean(insertion)
            warped.append(x)
            print("Insertion: {} = {}".format(insertion, x))
            warped.append(x)
            history.append(insertion)
        if deletion:
            x = np.mean(deletion)
            print("Deletion: {} = {}".format(deletion, x))
            warped.append(x)
            history.append(deletion)
            
    warped = list(reversed(warped))
    plt.figure(figsize=(10,8))
    plt.subplot(3,1,1)
    plt.plot(np.arange(sig1.shape[1]),sig1[0])
    plt.subplot(3,1,2)
    plt.plot(np.arange(sig2.shape[1]),sig2[0])
    plt.subplot(3,1,3)
    plt.plot(np.arange(len(warped)), warped)
    plt.show()
    print(history)
    return warped