"""
Name:Bhargavi Poyekar
BE COMPS/ Batch-C
UID: 2018130040
Roll No:45
Date of lab: 15/09/21
Aim: 2b) To implement AHP method for a given problem. [Specific]- (Machinability Evaluation of Work Materials)

"""

# importing libraries
import random
import numpy
import pandas as pd
import csv
from datetime import datetime

# getting input values from csv file 
with open('lab2b_input.csv', mode='r') as file:
    csv_reader=csv.reader(file) # generating the reader 
    l_count=0 # initializing line count to 0 
    m=[] # array for measurement values
    for row in csv_reader: # taking a row at a time
        if l_count==0: # if first row
            attr=row # attributes 
            l_count+=1 # increment line count
        elif l_count==1: # if second row
            imp=row # importance values
            l_count+=1 # increment line count
        elif l_count==2: # if third row
            crit=row # criterias
            l_count+=1 # increment line count
        else:
            m.append(row) # append to measurement
            l_count+=1 # increment line count


#converting string values of list to integers
imp = list(map(int, imp))
crit = list(map(int, crit))
D = [list( map(int,i) ) for i in m]

N=len(D) # Number of alternatives
M=len(attr) # Number of attributes

C = [[1,5,5],[1/5,1,1],[1/5,1,1]]
A1 = numpy.array(C) # Converting 2d list to numpy array
print("\nA1 (Pair-wise Comparison Matrix):") 
print(A1)
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
print("\nGM (Geometric Means):")
print(GM)

A2=[0 for i in range(M)] # initializing array for normalized GM
for i in range(M):
    A2[i]=round(GM[i]/sum,4) # Normalizing GM and rounding off the values
A2=numpy.array(A2) # Converting list to numpy array

A3=numpy.dot(A1,A2) # Matrix multiplication of A1 and A2, A3 = A1 x A2
A3=numpy.round(A3,4) # Rounding off the values of A3
print("\nA3:")
print(A3)

A4=numpy.divide(A3,A2) # Calculating A4 = A3/A2
A4=numpy.round(A4,2) # Rounding off the values of A4
print("\nA4:")
print(A4)
sumA4=numpy.sum(A4) # getting sum of all values of A4
lambdamax=round(sumA4/M,2) # finding lambdamax = sum(A4) / M 
print(f'\nlambdamax={lambdamax}')


CI=(lambdamax-M)/(M-1) # Calculating CI (Consistency Index)
print(f'CI:{CI}')
RI=[0, 0, 0.52, 0.89, 1.11, 1.24, 1.35, 1.4, 1.45, 1.49] # RI values for no. of attribute
CR=CI/RI[M-1] # finding CR (Consistency ratio)
print(f'CR: {CR}') #printing CR value with the iteration loop 

if CR<0.10:
    print("\nMatrix is consistent\n")
    D=numpy.array(D)
    print("\nD:")
    print(D)

    minmax = [0 for i in range(M)]  # initializing minmax array

    trans = D.T  # taking transpose of array

    norm = [[0] * N for i in range(M)]  # initializing normalized array

    for i in range(M):
        if(crit[i] == 0):  # if criteria is non beneficial
            minmax[i] = min(trans[i])  # take min value
            # divide min value by the value
            norm[i] = numpy.round(minmax[i]/trans[i], 2)
        else:  # if criteria is non beneficial
            minmax[i] = max(trans[i])  # take min value
            # divide value by max value
            norm[i] = numpy.round(trans[i]/minmax[i], 2)
    print("\nMinMax:")
    print(minmax)

    norm = numpy.array(norm).T  # take transpose

    scores = [0 for i in range(N)]  # initialize scores array
    for i in range(N):
        for j in range(M):
            # calculating scores (adding)
            scores[i] += norm[i][j]*A2[j]
    
    for i in range(N):
        scores[i] = numpy.round(scores[i], 5)  # rounding off the scores

    # sort the list in descending order and remove repeat values
    sorted_scores = sorted(scores, reverse=True) # sort the scores
    ranks = [0 for i in range(N)]  # initializing array for ranks
    print("\nAi\tScores\t:Rank")
    for i in range(N):
        # get index+1 of values to get rank
        ranks[i] = sorted_scores.index(scores[i])+1
        print(str(i+1)+"\t "+str(scores[i])+" : " + str(ranks[i])+"\n")

    dict = {'Ai': scores, 'Rank': ranks}  # dictionary for dataframe

    best=scores.index(sorted_scores[0])+1 # getting index of best score
    print("\nThe method suggests A" + str(best) + " as the best machinable work material. ") # printing best alternative
    print("\nThe attribute values of best alternative are:")
    # printing the attribute of best working material
    for i in range(M):
        print("B"+str(i+1) + ": " + str(D[best-1][i]), end=" ")

else:
    print("Matrix is inconsistent")


