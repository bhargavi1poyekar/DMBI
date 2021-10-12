"""
Name:Bhargavi Poyekar
BE COMPS/ Batch-C
UID: 2018130040
Roll No:45
Date of lab: 22/09/21
Aim: 2c) To implement TOPSIS method using AHP (for weights) for a given problem.
 
"""

# importing libraries
import random
import numpy
import pandas as pd
import csv
from datetime import datetime
import math

RN = int(input("Enter roll no:\n"))  # input roll no
N = 10+RN % 3  # calculating N: Number of alternatives.
M = 7+RN % 3   # calculating M: Number of attributes.

D = [[0] * M for i in range(N)]  # initializing array for decision matrix
s = 15-RN%16  # start value of range
e = 30+RN%16  # end value of range

f=1 # setting lag as 1
for k in range(10000):
    C = [[0] * M for i in range(M)]  # initializing array for comparison matrix
    
    # assigning random values from 2-9 for pairwise comparison matrix

    for i in range(M):
        for j in range(M):
            if i<j: # i<j  value between 2-9
                C[i][j] = random.randint(2, 9)
            elif i==j: # i==j value =1
                C[i][j] = 1
            else: # i>j then inverse value
                C[i][j] = round(1/C[j][i],3)

    A1=numpy.array(C) # Converting 2d list to numpy array
    GM=[1 for i in range(M)] # initializing Geometric Means array 
    exp=1/M # exponential value

    # Calculating geometric means 
    for i in range(M):
        for j in range(M):
            GM[i]*=A1[i][j]
        GM[i]=GM[i]**exp

    GM=numpy.array(GM) # converting list to numpy array
    GM=numpy.round(GM,2) # rounding of the values till 2 decimals
    sum=numpy.sum(GM) # sum of all values of GM array
    

    A2=[0 for i in range(M)] # initializing array for normalized GM
    for i in range(M):
        A2[i]=round(GM[i]/sum,2) # Normalizing GM and rounding off the values
    A2=numpy.array(A2) # Converting list to numpy array

    A3=numpy.dot(A1,A2) # Matrix multiplication of A1 and A2, A3 = A1 x A2
    A3=numpy.round(A3,2) # Rounding off the values of A3

    A4=numpy.divide(A3,A2) # Calculating A4 = A3/A2
    A4=numpy.round(A4,2) # Rounding off the values of A4

    sumA4=numpy.sum(A4) # getting sum of all values of A4
    lambdamax=round(sumA4/M,2) # finding lambdamax = sum(A4) / M 

    CI=(lambdamax-M)/(M-1) # Calculating CI (Consistency Index)
    RI=[0, 0, 0.52, 0.89, 1.11, 1.24, 1.35, 1.4, 1.45, 1.49] # RI values for no. of attribute
    CR=CI/RI[M-1] # finding CR (Consistency ratio)
    print(f'CR_{k}: {CR}') #printing CR value with the iteration loop 
    
    if CR<0.10:
        f=0 # setting flag as 0 to indicate that matrix is consistent
        print("\nMatrix is consistent\n")
        # printing all values
        print("\nA1 (Pair-wise Comparison Matrix):") 
        print(A1)
        print("\nGM (Geometric Means):")
        print(GM)
        print("\nA2 (Normalized GM):")
        print(A2)
        print("\nA3:")
        print(A3)
        print("\nA4:")
        print(A4)
        print(f'lambdamax={lambdamax}')
        print(f'CI:{CI}')
        break

if f==1: # If matrix not consistent, equal weights for all attributes
    print("Matrix is not consistent")
    weight=1/M # equal weights
    A2=[round(weight,4) for i in range(M)]

total = 50*M/100  # equal distribution of beneficial and nonbeneficial criteria
bcount = 0  # keeping count of beneficial
nbcount = 0  # keeping count of non beneficial

crit = [0 for i in range(M)]  # initiliazing criteria array

for i in range(M):
    if(bcount >= total):  # if beneficial more than 50% assign non beneficial
        crit[i] = 0
        nbcount += 1  # inc nbcount
    elif(nbcount >= total):  # if non beneficial more than 50% assign beneficial
        crit[i] = 1
        bcount += 1  # dec nbcount
    else:  # else randomly assign
        crit[i] = random.randint(0, 1)
        if(crit[i] == 0):
            nbcount += 1  # increase count for non beneficial
        else:
            bcount += 1  # increase count for beneficial

random.seed(45)
# assigning random measurements in the given range
for i in range(N):
    for j in range(M):
        D[i][j] = random.randint(s, e)

D=numpy.array(D) # converting list to numpy array
print("\nD:") # print Decision Matrix
print(D)

DT=D.T # Transpose of Decision Matrix

Denom=[0 for i in range(M)] # initializing the denominator array

for i in range(len(DT)):
    sum=0
    for j in range(N):
        sum+=DT[i][j]**2 # calculate summation of sqaures 
    Denom[i]=round(math.sqrt(sum),4) # taking square root of summation and save to denominator array

print("\nDenom:")
print(Denom) # print denominator array 

RT=[[0] * N for i in range(M)] # initializing the transposed normalized matrix

for i in range(len(DT)):
    RT[i]=list(DT[i]/Denom[i]) # dividing all the meaasurements by the respective denominators 

RT=numpy.round(RT,3) # rounding the transposed normalized matrix
Rij=RT.T # Taking transpose to get the normalized matrix
print("\nRij (Normalized Decision Matrix): ")
print(Rij) # print Normalized Matrix
print(f'\nA2 (Weights):\n{A2}') # print weights
weigh_normT=[[0] * N for i in range(M)] # initializing transposed weighted normalized matrix

for i in range(len(RT)):
    weigh_normT[i]=RT[i]*A2[i] # Multiplying the normalized matrix with weights

weigh_norm=numpy.array(weigh_normT).T # get the weighted normalized matrix
print("\nVij (Weighted Normalized Decision Matrix): ")
print(weigh_norm) # print weighted Normalized Matrix

Vp=[0 for i in range(M)] # initializing V+ (ideal) best solutions
Vm=[0 for i in range(M)] # initializing V- (negative ideal) worst solutions

print("\nCriteria (1 for benefecial and 0 for non-beneficial):")
print(crit) # printing Criteria

for i in range(M):
    if crit[i]==1: # if beneficial
        Vp[i]=max(weigh_normT[i]) # V+ = max
        Vm[i]=min(weigh_normT[i]) # V- = min
    else: # if non-beneficial
        Vm[i]=max(weigh_normT[i]) # V- =min
        Vp[i]=min(weigh_normT[i]) # V+ =max
print(f'\nV+:{Vp}') # Print V+
print(f'V-:{Vm}') # Print V-

Sp=[0 for i in range(N)] # initializing S+
Sm=[0 for i in range(N)] # initializing S-

for i in range(N):
    sum1=sum2=0
    for j in range(M):
        sum1+=(weigh_norm[i][j]-Vp[j])**2 # Calculating Eucledian distance from ideal best
        sum2+=(weigh_norm[i][j]-Vm[j])**2 # Calculating Eucledian distance from ideal worst
    Sp[i]=round(math.sqrt(sum1),4) # taking square root and rounding off to 4 decimal places
    Sm[i]=round(math.sqrt(sum2),4)

print(f'\nS+:\n{Sp}') # print S+
print(f'\nS-:\n{Sm}') # print S-

Pi=[0 for i in range(N)] # initializing array for scores

for i in range(N):
    Pi[i]=round(Sm[i]/(Sp[i]+Sm[i]),4) # Calculating Scores

# sort the list in descending order and remove repeat values
sorted_scores = sorted(Pi, reverse=True) # sort the scores
ranks = [0 for i in range(N)]  # initializing array for ranks
print("\nAi\tPi (Scores)\t:Rank")
for i in range(N):
    # get index+1 of values to get rank
    ranks[i] = sorted_scores.index(Pi[i])+1
    print(str(i+1)+"\t "+str(Pi[i])+" :\t " + str(ranks[i])+"\n")

best=Pi.index(sorted_scores[0])+1 # getting index of best score
print("\nThe Topsis method suggests A" + str(best) + " as the best machinable work material. ") # printing best alternative
print("\nThe attribute values of best alternative are:")
# printing the attribute of best working material
for i in range(M):
    print("B"+str(i+1) + ": " + str(D[best-1][i]), end=" ")

