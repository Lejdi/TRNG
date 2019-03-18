import sounddevice as sd
import matplotlib.pyplot as plt
import numpy as np
import math

def entropy(n, size):
    result=0
    for i in n:
        result+=((i/size)*math.log2(i/size))
    return -result

recSize=100000
mask=0b111
str_threeBits=[]
int_threeBits=[]

samples=sd.rec(recSize,channels=1,dtype='int16')
sd.wait()

for i in range(0,recSize):
    int_threeBits.append(samples[i][0] & mask)
    str_threeBits.append('00')
    str_threeBits[i]+=(bin(samples[i][0] & mask)[2:5])
    str_threeBits[i]=str_threeBits[i][-3:]
numbins=8
n, bins, patches = plt.hist(int_threeBits, numbins, facecolor='blue', alpha=0.5)
plt.show()
print("entropy: %f"%entropy(n,recSize))
