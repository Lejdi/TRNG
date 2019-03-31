import numpy as np
import matplotlib.pyplot as plt
import struct
import math
import sounddevice as sd


def floatToRawLongBits(value):
	return struct.unpack('Q', struct.pack('d', value))[0]
        # struct.pack('d', value) - rzutuje na double (w pythonie float o dlugosci 8), robimy to po to, żeby zgadzały się długości typów w pythonie
        # struct.unpack('Q',...) - z floata bierze bity i zapisuje je jako long (w pythonie int o dlugosci 8)
        # całość wyciąga bity z floata i zmienia im typ na long, żeby można było je odczytać


def entropy(n, size):
    result = 0
    for i in n:
        if i>0:
            result += ((i / size) * math.log2(i / size))
    return -result


def fT(x):
    a = 1.99999
    if x < 0.5:
        return np.float64(a*x)
    else:
        return np.float64(a*(1-x))

def swap(z):
    tmp=""
    tmp+=(z[32:63]+z[0:31])  # zamienia pierwsze 32 bity z ostatnimy 32 bitami i zapisuje je w stringu
    return tmp


def xor(x,y):
    z = int(x, 2) ^ int(y, 2) # zamieniamy stringi z binarnymi liczbami na intigery, a na intigerach dokonuje operacji XOR
    return '{0:b}'.format(z).zfill(64)  # zamiana intigera na stringa z liczbą binarną, dodatkowo wypełnia brakujące zera z lewej strony

def postprocessing(r):
    N = 8*1024*1024  # rozmiar ciągu na wyjściu
    L = 8  # rozmiar CCML
    y = 8  # liczba iteracji, mysle ze 500 to bedzie dobra liczba
    e = 0.05  # stała sprzęgacza (coupling constant)
    z = [0 for i in range(8)]
    x = [[0 for t in range(y)] for i in range(8)]  # tworzymy tablie [0:7][0:y-1] i wypełniamy ja zerami
    x[0][0] = 0.141592
    x[1][0] = 0.653589
    x[2][0] = 0.793238
    x[3][0] = 0.462643
    x[4][0] = 0.383279
    x[5][0] = 0.502884
    x[6][0] = 0.197169
    x[7][0] = 0.399375
    c = 10000  # licznik próbek
    O = "" # ciąg na wyjściu
    t=0
    while len(O) < N:
        for i in range(L):
                x[i][t] = ((0.071428571 * int(r[c],2)) + x[i][t]) * 0.666666667
                # print(x[i][t])
                c += 1
        for t in range(y-1):
            for i in range(L):
                x[i][t+1] = (1-e)*fT(x[i][t]) + (e/2)*(fT(x[(i+1) % L][t]) + fT(x[(i-1) % L][t]))
        for i in range(L):
            z[i] = floatToRawLongBits(x[i][4])
            z[i] = "{0:b}".format(z[i]) # rzutowanie intigera na stringa z binarną liczbą
            x[i][0] = x[i][4]

        z[0] = xor(z[0],swap(z[4]))
        z[1] = xor(z[1],swap(z[5]))
        z[2] = xor(z[2],swap(z[6]))
        z[3] = xor(z[3],swap(z[7]))
        O+=z[0]
        O+=z[1]
        O+=z[2]
        O+=z[3]
    #print("c: ",c)
    #print("O: ",O)
    return(O)

def xd():
        recSize=1000000
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
            
        eightBits=[]
        for i in range (0, int(len(allBits)/8)):
            eightBits.append('00000000')
            eightBits[i]+=allBits[i*8 : i*8+7]
            eightBits[i]=eightBits[i][-8:]
            
        numbins=256
        n, bins, patches = plt.hist(eightBits, numbins, facecolor='blue', alpha=1)
        plt.show()
        print("entropy1: %f"%entropy(n,int(recSize*3/8)))
        
        return threeBits


ciag = postprocessing(xd())
tablice = []
for i in range(1024*1024):
    tablice.append(ciag[i*8:i*8+8])

numbins=256


m, bins, patches = plt.hist(tablice, numbins, facecolor='blue', alpha=0.5)
plt.show()

print("entropy2: %f"%entropy(m, 1024*1024))
