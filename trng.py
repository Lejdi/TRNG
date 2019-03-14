import sounddevice as sd

recSize=100
mask=0b111
str_threeBits=[]
int_threeBits=[]

samples=sd.rec(recSize,channels=1,dtype='int16')
sd.wait()

for i in range(0,recSize):
    str_threeBits.append(bin(samples[i][0] & mask)[2:5])
    int_threeBits.append(samples[i][0] & mask)
print(str_threeBits)
print(int_threeBits)
