import os
import math
import numpy as np
import matplotlib as plt
import argparse

qamcoord = [0, 1, 3, 2, 6, 7, 5, 4,
        12, 13, 15, 14, 10, 11, 9, 8,
        24, 25, 27, 26, 30, 31, 29, 28,
        20, 21, 23, 22, 18, 19, 17, 16] #for max 10 bits

# This function takes specific set of bits and maps them
# into a desired QAM modulation.
def qammod(b, mod):
    global qamcoord
    if b.size != mod:
        print('number of bits do not match the modulation scheme')
        return -1
    elif mod not in [2, 4, 6, 8, 10]:
        print('Currently supporting only QPSK, 16QAM, 64QAM, 256QAM, 1024QAM')
        return -1
    else:
        dims = np.power(2,mod/2) # one side of the square
        coord = qamcoord[0:dims]
        xdim = 0
        ydim = 0
        for i in range(0, mod/2):
            xdim = xdim+b[i]*np.power(2,i)
            ydim = ydim+b[i+mod/2]*np.power(2,i)
        return np.complex(dims-(2*xdim+1), dims-(2*ydim+1))

def normFactor(mod):
    if mod not in [2, 4, 6, 8, 10]:
        print('Currently supporting only QPSK, 16QAM, 64QAM, 256QAM, 1024QAM')
        return -1
    dims = np.power(2,mod/2)
    ene_sum = 0
    for i in range(0,dims/2):
        for j in range(0, dims/2):
            ene_sum = ene_sum+np.power(2*i+1,2)+np.power(2*j+1,2)
    ene_sum = ene_sum/(np.power(dims,2)/4)
    return ene_sum


def generateIQ(N, mod):
    # N = number of samples
    # mod = modulation scheme, BPSK, QPSK, ..., 1024QAM
    #   BPSK=1, QPSK=2, ... 1024QAM=10
    bitN = N * mod
    c = [np.complex(0,0)]*N
    for i in range(N):
        # get random bits
        b = np.random.randint(2, size=mod)
        # encode bits into samples
        c[i] = qammod(b, mod)
    c = c/np.sqrt(normFactor(mod))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("N", help="Number of complex samples.",
                    type=int)
    parser.add_argument("mod", help="Number of bits per sample.",
                    type=int, choices=[2,4,6,8,10], metavar='Mod')
    args = parser.parse_args()
    N = args.N
    mod = args.mod
    # generate the base-band IQ signal
    generateIQ(N, mod)

if __name__ == "__main__":
    main()
