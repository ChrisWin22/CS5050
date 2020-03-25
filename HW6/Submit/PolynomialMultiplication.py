import numpy as np
import random
import time
import matplotlib.pyplot as plt


def makePoly(n):
    poly = np.random.uniform(-1.0, 1.0, size=(n))
    return poly

def multiply(P, Q, n):
    PQ = np.zeros(((2*n) - 1))
    for i in range(0, n):
        for j in range(0,n):
            PQ[i+j] = PQ[i+j] + (P[i] * Q[j])
    return PQ

def makeGraphs(dc, hs, three, num):
    polysize = [0]
    startPoint = 32
    for _ in range(1, len(dc)):
        startPoint = startPoint * 2
        polysize.append(startPoint)

    # dcbf = np.polyfit(np.log(polysize), np.log(dc), 1)
    # hsbf = np.polyfit(np.log(polysize), np.log(hs), 1)
    # threebf = np.polyfit(np.log(polysize), np.log(three), 1)
    # print(dcbf)
    # print(hsbf)
    # print(threebf)
    plt.yscale('log')
    plt.xscale('log')
    plt.plot(polysize, dc, color='blue', label = "Divide and Conquer")
    plt.plot(polysize, hs, color='red', label = "High School")
    plt.plot(polysize, three, color='green', label = "Three Calls")
    # plt.plot(polysize, dcbf[0], color='blue', label = "Divide and Conquer Slope", linestyle = 'dashed')
    # plt.plot(polysize, hsbf[0], color='red', label="High School Slope", linestyle='dashed')
    # plt.plot(polysize, threebf[0], color='green', label="Three Calls Slope", linestyle = 'dashed')
    plt.xlabel('Size of Polynomials (Largest Exponent)')
    plt.ylabel('Run Time (seconds)')
    plt.title("Divide and Conquer vs High School: Polynomial Multiplication")
    plt.legend()
    plt.show()


def dcMultiply(P, Q, n):
    PQ = np.zeros((2*n))
    if n == 1: 
        PQ[0] = P[0] * Q[0]
        return PQ
    PQll = dcMultiply(P[0:int(n/2)], Q[0:int(n/2)], int(n/2))
    PQlh = dcMultiply(P[0:int(n/2)], Q[int(n/2):], int(n/2))
    PQhl = dcMultiply(P[int(n/2):], Q[0:int(n/2)], int(n/2))
    PQhh = dcMultiply(P[int(n/2):], Q[int(n/2):], int(n/2))

    for i in range(0,n):
        PQ[i] = PQ[i] + PQll[i]
        PQ[i + int(n/2)] = PQ[i + int(n/2)] + PQlh[i]
        PQ[i + int(n/2)] = PQ[i + int(n/2)] + PQhl[i]
        PQ[i + n] = PQ[i + n] + PQhh[i]
    return PQ


def dcMultiplyThree(P, Q, n):
    PQ = np.zeros((2*n))
    if n == 1: 
        PQ[0] = P[0] * Q[0]
        return PQ
    Sll = dcMultiplyThree(P[0:int(n/2)], Q[0:int(n/2)], int(n/2))
    sp = np.zeros(int(n/2))
    sq = np.zeros(int(n/2))
    for i in range(0, int(n/2)):
        sp[i] = P[i] + P[i + int(n/2)]
        sq[i] = Q[i] + Q[i + int(n/2)]
    So = dcMultiplyThree(sp, sq, int(n/2))
    Shh = dcMultiplyThree(P[int(n/2):], Q[int(n/2):], int(n/2))
    middle = np.zeros(n)
    for i in range(0, n):
        middle[i] = So[i] - Sll[i] - Shh[i]
    for i in range(0,n):
        PQ[i] = PQ[i] + Sll[i]
        PQ[i + int(n/2)] = PQ[i + int(n/2)] + middle[i]
        PQ[i + n] = PQ[i + n] + Shh[i]
    return PQ



def runTests():
    size = 32
    spot = 1
    dcRunTimeArray = [0]
    hsRunTimeArray = [0]
    threeRunTimeArray = [0]
    runTimeDC = 0
    runTimeHS = 0
    runTimeThree = 0
    num = 0
    while runTimeDC < 30 and runTimeHS < 1500:
        print("starting dc " + str(num))
        dcRunTimeArray.append(0)
        hsRunTimeArray.append(0)
        threeRunTimeArray.append(0)
        start = time.time()
        for _ in range(1,11):
            one = makePoly(size)
            two = makePoly(size)
            dcMultiply(one, two, len(one))
        runTimeDC = time.time() - start
        dcRunTimeArray[spot] = runTimeDC
        start = time.time()
        print("starting hs " + str(num))
        for _ in range(1,11):
            one = makePoly(size)
            two = makePoly(size)
            multiply(one, two, len(one))
        runTimeHS = time.time() - start
        hsRunTimeArray[spot] = runTimeHS
        start = time.time()
        print("starting three " + str(num))
        for _ in range(1,11):
            one = makePoly(size)
            two = makePoly(size)
            dcMultiplyThree(one, two, len(one))
        runTimeThree = time.time() - start
        threeRunTimeArray[spot] = runTimeThree
        size = size * 2
        spot = spot + 1
        num = num + 1
    makeGraphs(dcRunTimeArray, hsRunTimeArray, threeRunTimeArray, size)

P = [13,2,8,16]
Q = [6,14,9,23]
# print("High School: " + str(multiply(P, Q, len(P))))
# print("DC:          " + str(dcMultiply(P, Q, len(P))))
# P = [5,7,2,1]
# Q = [2,1,1,4]
# print("Three:       " + str(dcMultiplyThree(P, Q, len(P))))
runTests()

