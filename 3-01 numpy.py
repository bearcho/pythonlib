import random as rd
import numpy as np

LA = [rd.randint(1,9) for _ in range(10)]
NA = np.array(LA)
LB= [[rd.randint(1,9) for _ in range(5)] for _ in range(5)]
print(LB)
# NB = np.

NB = np.array(LB)
print(NB.shape)
LC= [[rd.randint(1,9) for _ in range(5)] for _ in range(5)]
NC = np.array(LC)

print(NC)
print(NC*NC)

NA.reshape(5,2)
# print(NA)
# print(NA.reshape(5,2))
#
# print(NB*NC)

ND = np.dot(NB,NC)
print(ND)

print(type(NB))

NE = np.array([1,2,3,4,5])
# print(LB[0][4])
# print(NB[0][4])
# print(LB[0,4])
# print(NB)
print(NB[0:2,1:4])


NF = np.array([1,2,3],dtype=np.float16)
print(NF)
inImage = np.array([1,2,3], dtype=np.uint8)
print(type(inImage))
print(min(LB))
print(NB.min())
print(NB.max())