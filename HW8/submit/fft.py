import math
import time
import matplotlib.pyplot as plt

def getV(n, s):
    # v = []
    # for i in range(0, n):
    v = [complex(math.cos(i*2*math.pi/n), s * math.sin(i*2*math.pi/n)) for i in range(0, n)] 
    return v


def fft(p, x, n):

    #base case
    if n == 1:
        return p

    #split even odd
    even = [p[j] for j in range(0, n, 2)]
    odd = [p[j] for j in range(1, n, 2)]

    #double half of x values
    # w = []
    # for i in range(0, n//2):
    #     w[i] = x[i] * x[i]
    w = [x[i] * x[i] for i in range(0, n//2)]

    #compute values for odd and even
    SE = fft(even, w, n//2)
    SO = fft(odd, w, n//2)

    #Construct solution
    # solution = []
    # for i in range(0, n//2):
    #     solution[i] = (SE[i] + (x[i] * SO[i])) + (SE[i] - (x[i] * SO[i]))
    solution = [SE[i] + x[i] * SO[i] for i in range(0, n//2)] +  [SE[i] - x[i] * SO[i] for i in range(0, n//2)]

 
    return solution


def runner():
    n = 128
    runtime = 0
    timeArray = []
    while runtime < 1500:
        p = []
        for i in range(0, n):
            p.append(i)
        start = time.time()
        sol = fft([complex(p[i],0) for i in range(0,n)], getV(n, +1), n)
        back=[s/8 for s in fft(sol, getV(n, -1), n)]
        runtime = time.time() - start
        n = n * 2
        timeArray.append(runtime)
    return timeArray



def createGraph():
    temp = 128
    timeArray = runner()
    nArray = []
    for i in range(0, len(timeArray)):
        nArray.append(temp)
        temp = temp * 2
    print(nArray)
    print(timeArray)
    plt.yscale('log')
    plt.xscale('log')
    plt.plot(nArray, timeArray)
    plt.xlabel('Size of Polynomials (Largest Exponent)')
    plt.ylabel('Run Time (seconds)')
    plt.title("FFT Conversions Times")
    plt.legend()
    plt.show()

createGraph()