import random
import numpy as np
numSims = 100000 #Number of simulations to run
M = 20
diff=[] #sum minus M for each trial
num = [] #number of rolls for each trial
for x in range(numSims):
    runtot = 0
    numrolls = 0
    while runtot < M:
        roll = random.randrange(1,7)
        runtot += roll
        numrolls += 1
    diff.append(runtot-M)
    num.append(numrolls)
diff = np.array(diff)
num = np.array(num)
print("Mean of total minus M for M=20: ",np.mean(diff))
print("Mean number of rolls for M=20: ",np.mean(num))
print("Standard Deviation of total minus M for M=20: ",np.std(diff))

M = 5000
diff=[]
num = []
for x in range(numSims):
    runtot = 0
    numrolls = 0
    while runtot < M:
        roll = random.randrange(1,7)
        runtot += roll
        numrolls += 1
    diff.append( runtot-M)
    num.append(numrolls)
diff = np.array(diff)
num = np.array(num)
print("Mean of total minus M for M=5000: ",np.mean(diff))
print("Mean number of rolls for M=5000: ",np.mean(num))
print("Standard Deviation of total minus M for M=5000: ",np.std(diff))


