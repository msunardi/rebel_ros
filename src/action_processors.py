# -*- coding: utf-8 -*-
import numpy as np
from scipy.interpolate import interp1d
import scipy.fftpack as spfft
import matplotlib.pyplot as plt

from utils import elapsed, rprint
from pandas import DataFrame

@elapsed
def merges(*data, **kwargs):
    '''Accepts arbitrary number of data points to merge
       Merges using FFT
       Returns: inverse FFT of merged signals
    '''
    # Need to support multiple joint movements
    joint='R_SHO_PITCH'
    if 'joint' in kwargs:
        joint = kwargs['joint']
    N=400
    if 'N' in kwargs:
        N = kwargs['N']
    p=[1.0]
    if 'p' in kwargs:
        p = kwargs['p']
    else:
        p = np.ones((len(data),))/np.float(len(data))
        rprint("[MERGES]: P not provided. Assumes equal distribution for {} items.\np={}", len(data), p)
    
    assert len(p) == len(data), "[MERGE2]: Mismatch number of values in p to perform weighted sum! p size={}, data size={}".format(len(p), len(data))
    assert sum(p) == 1.0, "[MERGE2]: P value does not sum to 1: {}".format(p)
    
    LL = len(data)
    if LL == 1:
        print("[MERGE2]: There's only one data. Returning as-is.")
        return data
    
    # Find 
    # Check data type
    if type(data[0]) == dict:
        just_joint_data = [d[joint] for d in data]
    elif type(data[0]) == DataFrame:
        just_joint_data = [d[joint].values for d in data]
    data_lengths = [len(dx) for dx in just_joint_data]
    max_data_lengths = max(data_lengths)
    
    # Container for all Fourier'd signals
    fftx_all = []
    all_data = []
    
    T = 1.0/800.0
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    for dd in just_joint_data:
        l = len(dd)
        
        x = np.arange(0, l)
        rprint("[MERGES]: dd: {}", dd)
        fx = interp1d(x, dd, kind='nearest', fill_value='extrapolate')
        
        xnew = np.linspace(0, l-1, N*2, endpoint=True)        
        
        fxxnew = fx(xnew)[:-50]
        fftx = spfft.fft(fxxnew)
        fftx_all.append((xf, fftx))
#        print(len(xnew), len(dd))
        all_data.append((xnew, fxxnew))
        
    # Combined data
    le_p = np.array(p)
    fftx_all_array = np.array(fftx_all)[:,1]
    assert le_p.shape == fftx_all_array.shape, "[MERGE2]: le_p shape: {}, fftx_shape: {}".format(le_p.shape, fftx_all_array.shape)
        
    fft_combined = np.dot(le_p, fftx_all_array)
    print("[MERGE2]: fft_combined.shape: {}".format(fft_combined.shape))

    ifft_combined = spfft.ifft(fft_combined)
    fftx_all.append((xf, fft_combined))
    ix = np.linspace(0, max_data_lengths, ifft_combined.shape[0])
    
    # interpolate result
#    ln = ifft_combined.shape[0]
#    x = np.arange(0, ln)
#    ifft_interp = interp1d(x, ifft_combined, kind='cubic')
#    xnew = np.linspace(0, l-1, N*2, endpoint=True)
    all_data.append((ix, ifft_combined))
#    all_data.append((ix, ifft_interp(xnew)))
    
    f, ax = plt.subplots(len(all_data), 2, figsize=(8,7))
    
    assert len(all_data) == len(fftx_all)
    
    print("[MERGE2]: Will plot {} data.".format(len(all_data)))
    
    for j in np.arange(len(all_data)):
        xnew, fxxnew = all_data[j]
        if len(xnew) != len(fxxnew):
            ll = min(len(xnew), len(fxxnew))
        ax[j, 0].plot(xnew[:ll], fxxnew[:ll])   
        
#        assert len(xnew) == len(fxxnew), "xnew: {} vs. fxxnew: {}".format(len(xnew), len(fxxnew))
#        ax[j, 0].plot(xnew, fxxnew)
    
    for i in np.arange(len(fftx_all)):
        xff, fftxx = fftx_all[i]
        ax[i, 1].plot(xff, 2.0/N*abs(fftxx.imag[:N//2]))
        
    
    plt.show()
    return ifft_combined