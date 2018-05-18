#!/usr/bin/env python
'''motion_analyzer.py

Author: msunardi
Created: 5/16/18

Find statistics of motion data
'''
import pandas as pd
import numpy as np
from scipy.interpolate import interp1d
import scipy.fftpack as spfft
import scipy.signal as spsig
import matplotlib.pyplot as plt
import scipy


def analyze(data):
    foo_time = pd.DataFrame(data)
    # print foo_time
    foo = foo_time[foo_time.columns.difference(['Time', 'PauseTime'])]
    foo.plot()
    print(foo)
    print(foo.std(axis=0))

    # Ref: https://stackoverflow.com/a/41532180
    foo_mean = foo.mean()
    normalized_foo_std = (foo - foo.mean())/foo.std()
    normalized_foo_minmax = (foo - foo.min())/(foo.max() - foo.min())

    # Ref: https://stackoverflow.com/a/49813507
    def normalize(x):
        try:
            x = x / np.linalg.norm(x, ord=1)
            return x
        except:
            raise

    normalized_norm = foo.apply(normalize)
    #print "NORMALIZED_NORM: {}".format(normalized_norm)

    # Check by gradient
    pyuu = foo.apply(np.gradient)
    pyuu_mean_std = (pyuu - pyuu.mean())/pyuu.std()
    pyuu_norm = pyuu.apply(normalize)
    print("PYUU MAX: \n{}".format(pyuu.max()))
    pyuu_blah = ((pyuu.max() - pyuu.mean()) + (pyuu.mean() - pyuu.min()))/pyuu.std()
    print("PYUU MAX-MEAN: \n{}".format(pyuu_blah))
    print("PYUU.MODE: \n{}".format(pyuu_blah.mode()))

    # print "PYUU: {}".format(pyuu_mean_std)
    def f(x):
        return x/x.max()
    normalized_f = foo.apply(f, axis=0)
    pyuu_f = pyuu.apply(f)
    #print "NORMALIZED_F: {}".format(normalized_f)
    normalized = {'PYUU_NORM': pyuu_norm.mean(), 'PYUU_F': pyuu_f.mean(), 'PYUU': pyuu_mean_std.mean(), 'FOO': foo_mean, 'STD': pd.DataFrame(normalized_foo_std).mean(), 'MINMAX': pd.DataFrame(normalized_foo_minmax).mean(), 'NORM': normalized_norm.mean(), 'F': normalized_f.mean()}
    normalized = pd.DataFrame(normalized)
    # print "NORMALIZED SUMMARY: \n{}".format(normalized)
    pyuu.plot()
    return 0
    for col in foo.columns:
        m = max(abs(normalized_foo_std.mean()[col]), abs(normalized_foo_minmax.mean()[col]))
        if m > 0.0 and not pd.isnull(m):
            normalized[col] = m
        else:
            normalized[col] = 0.0
    # print("NORMALIZED: {}".format(normalized))
    normalized_foo = pd.DataFrame(normalized)
    # print(normalized_foo)
    # print(foo.mean())
    # print(normalized_foo.mean())
    # print(normalized_foo.columns)
    # assert normalized_foo.mean()['R_HIP_PITCH'] == 0.0
    to_return ={}
    # for col in foo.columns:
    #     if normalized_foo.mean()[col] != 0.0 and not pd.isnull(normalized_foo.mean()[col]):
    #         print normalized_foo.mean()[col]
    #         to_return[col] = list(foo[col].values)
    #     else:
    #         to_return[col] = [-1] * len(foo[col])
    for col in foo.columns:

        if normalized_foo.mean()[col] != 0.0:
            print(normalized_foo.mean()[col])
            to_return[col] = list(foo[col].values)
        else:
            to_return[col] = [-1] * len(foo[col])
    print(to_return)
    
def spectralize(data1, data2=None, joint='R_SHO_PITCH', N=400):
    l = len(data1[joint])
#    print("l: {}".format(l))
#    x = np.linspace(0, l-1, l)
    x = np.arange(0, l)
#    print("x: {} (shape: {})".format(x, x.shape))
#    print("data[{}]: {}".format(joint, data[joint]))
    fx = interp1d(x, data1[joint], kind='cubic', fill_value='extrapolate')
    
    T = 1.0/800.0
#    xf = np.linspace(0, l, num=N, endpoint=True)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
#    print("xf: {} (shape: {})".format(xf, xf.shape))
    
#    plt.plot(x, data[joint], xf, fx(xf))
#    xnew = np.linspace(0.0, N*T, N)
    xnew = np.linspace(0, l, N*2, endpoint=True)
#    print(fx(xf))
#    fxcont = np.concatenate((fx(xnew), fx(xnew), fx(xnew)))
    
#    xnew = np.linspace(0.0, N*T, N)
    fxxnew = fx(xnew)[:-50]
    fftx = spfft.fft(fxxnew)
#    fftx = spfft.fft(fxcont)
    freq1 = np.fft.fftfreq(N//2)
    freq1 = np.linspace(0.0, N*T*10, N)
    
    if data2:
        l2 = len(data2[joint])
        x2 = np.linspace(0, l2-1, l2)
        fx2 = interp1d(x2, data2[joint], kind='cubic', fill_value='extrapolate')
        fx2xnew = fx2(xnew)[:-50]
        
        fftx2 = spfft.fft(fx2xnew)
        
        p = 0.3
        fftx3 = p*fftx + (1-p)*fftx2
        ifftx3 = spfft.ifft(fftx3)
        x3corr = spsig.correlate(fxxnew, fx2xnew, method='auto')/(fx2xnew.shape[0]*N)
        x3conv = spsig.fftconvolve(fx2xnew, fxxnew)
        superimpose = (fxxnew + fx2xnew) / 2.0
        
        ix = np.linspace(0, l, ifftx3.shape[0])
        icorr = np.linspace(0, x3corr.shape[0]-1, x3corr.shape[0])
        iconv = np.linspace(0, x3conv.shape[0]-1, x3conv.shape[0])
        
#        iz = np.linspace(0.0, 1.0/(2*))
        f, ax = plt.subplots(3, 2)
        ax[0,0].plot(xnew[:-50], fxxnew)
        ax[1,0].plot(xnew[:-50], fx2xnew)
        ax[2,0].plot(ix, ifftx3)
#        ax[2,0].plot(icorr, x3corr)
#        ax[2,0].plot(iconv, x3conv)
#        ax[2,0].plot(xnew, superimpose)
#        ax[0,1].plot(freq1, 2.0/N * np.abs(fftx[:N//2]))
        ax[0,1].plot(xf, 2.0/N*abs(fftx.imag[:N//2]))
#        ax[0,1].plot(xf, 2.0/N * np.abs(fftx.imag[:N//2]), xf, 2.0/N * np.abs(fftx.real[:N//2]))
#        ax[1,1].plot(freq1, 2.0/N * np.abs(fftx2.imag[:N//2]), xf, 2.0/N * np.abs(fftx2.real[:N//2]))
        ax[1,1].plot(xf, 2.0/N*abs(fftx2.imag[:N//2]))
#        ax[2,1].plot(freq1, 2.0/N * np.abs(fftx3.imag[:N//2]), xf, 2.0/N * np.abs(fftx3.real[:N//2]))
        ax[2,1].plot(xf, 2.0/N*abs(fftx3.imag[:N//2]))
    else:
        plt.plot(xf, 2.0/N * np.abs(fftx.imag[:N//2]), xf, 2.0/N * np.abs(fftx.real[:N//2]))
#    plt.plot(freq1, 2.0/N * np.abs(fftx.imag[:N//2]), freq1, 2.0/N * np.abs(fftx.real[:N//2]))
#    plt.plot(xf, np.abs(fftx.imag[:N//2]), xf, np.abs(fftx.real[:N//2]))
    plt.show()
    
def test_spectral(data):
    # Number of samplepoints
    N = 600
    # sample spacing
    T = 1.0 / 800.0
#    x = np.linspace(0.0, N*T, N)
    x = np.linspace(0.0, 8.0, 600)
    #y = np.sin(50.0 * 2.0*np.pi*x) + 0.5*np.sin(80.0 * 2.0*np.pi*x)
    x2 = np.arange(0, len(data)) 
    f = interp1d(x2, data, kind='cubic', fill_value='extrapolate')
    y = f(x)
    yf = scipy.fftpack.fft(y)
    xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
    
    freq1 = np.fft.fftfreq(yf.shape[-1]//2)
    fig, ax = plt.subplots()
#    ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    ax.plot(xf, 2.0/N * np.abs(yf[:N//2]))
    plt.show()
    
def test_wavelet(data=None):
#    from scipy import signal
#    import matplotlib.pyplot as plt
    t = np.linspace(-1, 1, 200, endpoint=False)
#    sig  = np.cos(2 * np.pi * 7 * t) + spsig.gausspulse(t - 0.4, fc=2)
    
#    widths = np.arange(1, 31)
#    cwtmatr = spsig.cwt(sig, spsig.ricker, widths)
#    plt.imshow(cwtmatr, extent=[-1, 1, 31, 1], cmap='PRGn', aspect='auto',
#               vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
    x = np.linspace(0.0, 8.0, 600)
    x2 = np.arange(0, len(data)) 
    f = interp1d(x2, data, kind='cubic', fill_value='extrapolate')
    widths = np.arange(1, 31)
    cwtmatr = spsig.cwt(f(x), spsig.ricker, widths)
    plt.imshow(cwtmatr, extent=[-5, 5, 31, 1], cmap='PRGn', aspect='auto',
               vmax=abs(cwtmatr).max(), vmin=-abs(cwtmatr).max())
    plt.show()


if __name__ == "__main__":
    yes = {'L_HIP_ROLL': [510, 510, 510, 512], 'L_ANK_ROLL': [507, 507, 507, 512], 'Time': [21.634560916587375, 158.5851161449524, 163.7319856666194, 120.88843273331082], 'R_ANK_PITCH': [531, 531, 531, 512], 'R_SHO_PITCH': [863, 641, 682, 512], 'R_HIP_ROLL': [512, 512, 512, 512], 'R_HIP_YAW': [510, 510, 510, 512], 'L_ELBOW': [572, 572, 572, 512], 'R_ANK_ROLL': [508, 508, 508, 512], 'R_KNEE': [498, 98, 498, 512], 'L_SHO_ROLL': [563, 563, 563, 512], 'L_ANK_PITCH': [488, 488, 488, 512], 'R_HIP_PITCH': [494, 494, 494, 512], 'L_SHO_PITCH': [641, 641, 641, 512], 'HEAD_PAN': [509, 534, 534, 512], 'L_KNEE': [514, 514, 514, 512], 'R_ELBOW': [452, 211, 231, 512], 'HEAD_TILT': [512, 419, 502, 512], 'PauseTime': [111.35027490207358, 136.76900811944626, 205.1885074375004, 150.02956881612775], 'R_SHO_ROLL': [360, 342, 342, 512], 'L_HIP_PITCH': [521, 521, 521, 512], 'L_HIP_YAW': [510, 510, 510, 512]}
    wow = {'L_HIP_ROLL': [510, 510, 510, 512, 510, 510, 510, 510, 512], 'L_ANK_ROLL': [507, 507, 507, 512, 507, 507, 50, 507, 512], 'Time': [8.392673525291272, 124.96984319452696, 209.8742498654571, 40.69462704187933, 213.21572561894865, 78.87771445977911, 246.36666345136854, 0.49844984435603124, 237.02436067811087], 'R_ANK_PITCH': [531, 531, 531, 512, 531, 530, 531, 531, 512], 'R_SHO_PITCH': [863, 641, 682, 512, 601, 821, 897, 794, 512], 'R_HIP_ROLL': [512, 512, 512, 512, 512, 512, 512, 512, 512], 'R_HIP_YAW': [510, 510, 510, 512, 510, 510, 467, 545, 512], 'L_ELBOW': [572, 572, 572, 512, 570, 597, 649, 601, 512], 'R_ANK_ROLL': [508, 508, 508, 512, 508, 508, 508, 508, 512], 'R_KNEE': [498, 98, 498, 512, 498, 498, 498, 498, 512], 'L_SHO_ROLL': [563, 563, 563, 512, 545, 546, 686, 517, 512], 'L_ANK_PITCH': [488, 488, 488, 512, 488, 488, 488, 488, 512], 'R_HIP_PITCH': [494, 494, 494, 512, 494, 519, 519, 519, 512], 'L_SHO_PITCH': [641, 641, 641, 512, 450, 211, 162, 140, 512], 'HEAD_PAN': [509, 534, 534, 512, 509, 44, 598, 598, 512], 'L_KNEE': [514, 514, 514, 512, 514, 514, 514, 514, 512], 'R_ELBOW': [452, 211, 231, 512, 451, 435, 391, 379, 512], 'HEAD_TILT': [512, 419, 502, 512, 511, 541, 582, 582, 512], 'PauseTime': [123.88246746818449, 193.02985972159877, 128.66462672479162, 131.19227027090247, 91.05143798033616, 166.98756637716062, 41.712556568027225, 209.39841144114038, 155.6572018855816], 'R_SHO_ROLL': [360, 342, 342, 512, 477, 471, 561, 336, 512], 'L_HIP_PITCH': [521, 521, 521, 512, 529, 486, 486, 486, 512], 'L_HIP_YAW': [510, 510, 510, 512, 510, 510, 465, 554, 512]}
    wave3 = {'L_HIP_ROLL': [510, 510, 512, 510, 510, 510, 510, 512, 512, 521, 523, 523, 523, 523, 506, 512], 'L_ANK_ROLL': [507, 507, 512, 507, 507, 50, 507, 512, 512, 517, 517, 517, 517, 517, 517, 512], 'Time': [-76.99210045078934, -50.11816592955054, 87.66298573777365, 307.2739331715854, -13.662008897786777, 136.61304724095584, 110.27623071910419, 45.37131090956419, 177.99613279867077, 89.87253555901381, 243.3660108722867, 77.26836584808937, 198.3255968663169, 287.37854435243844, 232.04825440933504, 68.52055794546357], 'R_ANK_PITCH': [531, 531, 512, 531, 530, 531, 531, 512, 516, 530, 530, 530, 530, 530, 516, 512], 'R_SHO_PITCH': [641, 682, 512, 601, 821, 897, 794, 512, 512, 512, 512, 512, 470, 470, 444, 512], 'R_HIP_ROLL': [512, 512, 512, 512, 512, 512, 512, 512, 513, 533, 533, 533, 533, 533, 513, 512], 'R_HIP_YAW': [510, 510, 512, 510, 510, 467, 545, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'L_ELBOW': [572, 572, 512, 570, 597, 649, 601, 512, 512, 512, 575, 642, 451, 652, 652, 512], 'R_ANK_ROLL': [508, 508, 512, 508, 508, 508, 508, 512, 511, 535, 535, 535, 535, 535, 511, 512], 'R_KNEE': [98, 498, 512, 498, 498, 498, 498, 512, 512, 435, 435, 435, 435, 435, 483, 512], 'L_SHO_ROLL': [563, 563, 512, 545, 546, 686, 517, 512, 512, 512, 567, 401, 401, 441, 581, 512], 'L_ANK_PITCH': [488, 488, 512, 488, 488, 488, 488, 512, 512, 544, 544, 544, 544, 544, 502, 512], 'R_HIP_PITCH': [494, 494, 512, 494, 519, 519, 519, 512, 512, 447, 447, 447, 447, 447, 468, 512], 'L_SHO_PITCH': [641, 641, 512, 450, 211, 162, 140, 512, 512, 512, 598, 179, 272, 207, 496, 512], 'HEAD_PAN': [534, 534, 512, 509, 44, 598, 598, 512, 512, 512, 572, 652, 652, 681, 542, 512], 'L_KNEE': [514, 514, 512, 514, 514, 514, 514, 512, 512, 477, 477, 477, 477, 477, 507, 512], 'R_ELBOW': [211, 231, 512, 451, 435, 391, 379, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'HEAD_TILT': [419, 502, 512, 511, 541, 582, 582, 512, 512, 512, 512, 548, 510, 510, 510, 512], 'PauseTime': [131.35369339521242, 143.55288696444296, 94.50053754355176, 191.37278060637723, 93.35573683969675, 184.2986883636579, 133.9382311481281, 35.08416861341072, 199.22178179909778, 98.82118984417448, 134.70737367584962, 104.12967090199867, 56.83720497664956, 194.59941820928628, 118.09356844140423, 92.06220864516463], 'R_SHO_ROLL': [342, 342, 512, 477, 471, 561, 336, 512, 512, 512, 456, 456, 456, 456, 456, 512], 'L_HIP_PITCH': [521, 521, 512, 529, 486, 486, 486, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'L_HIP_YAW': [510, 510, 512, 510, 510, 465, 554, 512, 512, 512, 512, 512, 512, 512, 512, 512]}
    alas2 = {'L_HIP_ROLL': [512, 521, 523, 523, 523, 523, 506, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'L_ANK_ROLL': [512, 517, 517, 517, 517, 517, 517, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'Time': [156.1468338729221, 64.84886489357689, 197.42012437621548, 265.27558000516035, 14.18194312799453, 199.88804743962066, 107.55921195958169, 155.73916683283716, 77.51926701108877, 109.23258355766338, 226.0079273941755, 132.91125290186375, 68.52451101290269, -40.36928610096027, 105.47641812298116, 178.00381534961372], 'R_ANK_PITCH': [516, 530, 530, 530, 530, 530, 516, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'R_SHO_PITCH': [512, 512, 512, 512, 470, 470, 444, 512, 512, 512, 533, 997, 850, 570, 473, 512], 'R_HIP_ROLL': [513, 533, 533, 533, 533, 533, 513, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'R_HIP_YAW': [512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'L_ELBOW': [512, 512, 575, 642, 451, 652, 652, 512, 512, 512, 577, 529, 529, 485, 485, 512], 'R_ANK_ROLL': [511, 535, 535, 535, 535, 535, 511, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'R_KNEE': [512, 435, 435, 435, 435, 435, 483, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'L_SHO_ROLL': [512, 512, 567, 401, 401, 441, 581, 512, 512, 625, 625, 625, 505, 520, 565, 512], 'L_ANK_PITCH': [512, 544, 544, 544, 544, 544, 502, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'R_HIP_PITCH': [512, 447, 447, 447, 447, 447, 468, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'L_SHO_PITCH': [512, 512, 598, 179, 272, 207, 496, 512, 512, 512, 478, 141, 212, 469, 580, 512], 'HEAD_PAN': [512, 512, 572, 652, 652, 681, 542, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'L_KNEE': [512, 477, 477, 477, 477, 477, 507, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'R_ELBOW': [512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 375, 474, 474, 516, 516, 512], 'HEAD_TILT': [512, 512, 512, 548, 510, 510, 510, 512, 512, 512, 397, 616, 563, 488, 512, 512], 'PauseTime': [29.28338183982239, 25.315631196886326, 196.65184863523163, 168.00975811104573, 76.37687975332311, 43.33147774578007, 41.863217443268475, 10.759656636537077, 113.03316292112765, 86.71353303696489, 68.6232405964445, 167.4622257648791, 61.46045860270312, 156.6286928368727, 47.0160877723829, 178.89032576704187], 'R_SHO_ROLL': [512, 512, 456, 456, 456, 456, 456, 512, 512, 389, 389, 389, 547, 458, 458, 512], 'L_HIP_PITCH': [512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512], 'L_HIP_YAW': [512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512, 512]}

    mydata = yes
    analyze(mydata)