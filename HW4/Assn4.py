import numpy as np
import re

PATH="C:/Users/Woo Kei Cheung/Desktop/CSHW/CS5050/HW4/"

editSteps = np.array([[5,-1,-2,-1,-3],
            [-1,5,-3,-2,-4],
            [-2,-3,5,-2,-2],
            [-1,-2,-2,5,-1],
            [-3,-4,-2,-1,0]])

validSequences = ['a', 'c', 'g', 't']

fromDna = [(0,['a']), ('c',[1]), (2,['g']), (3,['t']), (4,[''])]

def getInt(letter):
    if letter == 'a':
        return 0
    if letter == 'c':
        return 1
    if letter == 'g':
        return 2
    if letter == 't':
        return 3
    if letter == '-': 
        return 4

def dnaEditDistance(seqOne, seqTwo, dest):
    i = len(seqOne)
    j = len(seqTwo)
    
    cache = np.full((j + 1, i + 1), None)
    cache[0,0] = 0
    for k in range(1, i+1):
        cache[0,k] = cache[0,k-1] + editSteps[4, getInt(seqOne[k - 1])]
    for k in range(1,j+1):
        cache[k,0] = cache[k-1,0] + editSteps[4, getInt(seqTwo[k - 1])]
    for x in range(1, i+1):
        for q in range(1,j+1):
            cache[q,x] = max(cache[q-1,x] + (editSteps[4, getInt(seqTwo[q-1])]), #add
                                cache[q,x-1] + (editSteps[getInt(seqOne[x-1]), 4]), #remove
                                cache[q-1,x-1] + (editSteps[getInt(seqOne[x-1]), getInt(seqTwo[q-1])])) #change
    getTraceback(seqOne, seqTwo,cache, dest)
    print("Done")


def getTraceback(seqOne, seqTwo, cache, dest):
    writeTo = open(PATH + dest, "w")
    i = len(seqOne)
    j = len(seqTwo)
    s1 = ""
    s2 = ""
    while i >= 1 and j >= 1:
        if cache[j, i] - editSteps[4, getInt(seqTwo[j-1])] == cache[j-1,i]:
            s1 = '_' + s1
            s2 = seqTwo[j-1] + s2
            j = j - 1
        elif cache[j,i] - editSteps[getInt(seqOne[i-1]), 4] ==  cache[j,i-1]:
            s1 = seqOne[i - 1] + s1
            s2 = '_' + s2
            i = i - 1
        elif cache[j,i] - editSteps[getInt(seqOne[i-1]), getInt(seqTwo[j-1])] == cache[j-1,i-1]:
            s1 = seqOne[i - 1] + s1
            s2 = seqTwo[j - 1] + s2
            j = j - 1
            i = i - 1
    while j >= 1:
        s1 = s1 + '_'
        s2 = seqTwo[j-1] + s2
        j = j - 1
    while i >= 1:
        s1 = seqOne[i - 1] + s1
        s2 = s2 + '_'
        i = i - 1
    writeTo.write("String One: " + seqOne + "\n")
    writeTo.write("String Two: " + seqTwo + "\n")
    writeTo.write("Score: " + str(cache[len(seqTwo), len(seqOne)]) + "\n")
    for l in range(0, len(s1)):
        if s1[l] == s2[l]:
            writeTo.write(s1[l] + " = " + s2[l] + "\n")
        else:
            writeTo.write(s1[l] + " -> " + s2[l] + "\n")

def getWords(fileName):
    fileInput = ""
    file = open(PATH + fileName, "r")
    for f in file:
        f.replace('\n', '').replace(' ', '')
        for i in f:
            if i in validSequences:
                fileInput = fileInput + i
    return fileInput

# first = "aaaaacg"
# second = "gaaaaag"
# dnaEditDistance(first, second)
gorilla = getWords("/GorillaMitochondion.txt")
nean = getWords("/NeanderthalensisMito.txt")
human = getWords("/HomoSapiensMito.txt")

dnaEditDistance(human, nean, "/human_nean.txt")
print()
dnaEditDistance(human, gorilla, "/human_gorilla.txt")
print()
dnaEditDistance(nean, gorilla, "/nean_gorilla.txt")