import numpy as np
import re

PATH="C:/Users/Woo Kei Cheung/Desktop/CSHW/CS5050/HW3/"

def med(i, j):
    if i == 0:
        return j
    if j == 0:
        return i
    return min(med(i-1, j) + 1, med(i, j-1) + 1, med(i-1, j-1) + (A[i-1]!=B[j-1]))

def medDP(wordOne, wordTwo):
    i = len(wordOne)
    j = len(wordTwo)
    cache = np.full((i + 1, j + 1), None)
    for k in range(0, i+1):
        cache[k,0] = k
    for k in range(0,j+1):
        cache[0,k] = k
    for x in range(1, i+1):
        for q in range(1,j+1):
            cache[x,q] = min(cache[x-1,q] + 1, cache[x,q-1] + 1, cache[x-1,q-1] + (wordOne[x-1]!=wordTwo[q-1]))
    return cache[i,j]    

def getWords():
    num = 0
    high = 0
    results = []
    results.append(0)
    file = open(PATH + "/WordList.txt", "r")
    for f in file:
        words = re.split("->|, |\n|\r", f)
        if len(words) > 2:
            for i in range(1, len(words) - 1):
                num = medDP(words[0], words[i])
                while num > high:
                    results.append(0)
                    high = high + 1
                results[num] = results[num] + 1
        else:
            num = medDP(words[0], words[1])
            while num > high:
                results.append(0)
                high = high + 1
            results[num] = results[num] + 1
    writeTo = open(PATH + "/WriteTo.txt", "w")
    for i in range(1, len(results)):
        writeTo.write(str(i) + " " + str(results[i]) + "\n")
        

A="abc"
B="bbc"


wordOne = "abilties"
wordTwo = "abilities"
getWords()
#medDP(wordOne, wordTwo)