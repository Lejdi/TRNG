import numpy as np
import matplotlib.pyplot as plt
import math
import sounddevice as sd


def entropy(n, size):
    result = 0
    for i in n:
        if i>0:
            result += ((i / size) * math.log2(i / size))
    return -result


recSize=100000
mask=0b111
threeBits=[]

samples=sd.rec(recSize,channels=1,dtype='int16')
sd.wait()

for i in range(recSize):
    threeBits.append('00')
    threeBits[i]+=(bin(samples[i][0] & mask)[2:5])
    threeBits[i]=threeBits[i][-3:]

allBits=''
for i in threeBits:
    allBits+=i

#code for testing compression:
"""
newFile = open("filename1.bin", "wb")
newFile.write(b"%r"%allBits[0:100])
newFile.close()
"""

#generating short words from all bits
wordSize=int(input("Enter word size:"))
if wordSize<=0 or wordSize>recSize:
    wordSize=1
    
redundantBits = recSize % wordSize
newSize=len(allBits)-redundantBits

word=[]
for i in range (0, int(newSize/wordSize)):
    word.append('')
    word[i].zfill(wordSize)
    word[i]+=allBits[i*wordSize : i*wordSize+wordSize]
    word[i]=word[i][-wordSize:]
#drawing histogram
"""
numbins=2**wordSize
n, bins, patches = plt.hist(word, numbins, facecolor='blue', alpha=1)
plt.show()
print("entropy: %f"%entropy(n,int(newSize/wordSize)))
"""
