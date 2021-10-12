"""
Name:Bhargavi Poyekar
BE COMPS/ Batch-C
UID: 2018130040
Roll No:45
Date of lab: 01/09/21
Aim: 1b) To implement SAW and WPM method for a given problem [Specific]-(Machinability Evaluation of Work Materials)
 
"""
# importing libraries
import random
import numpy
import pandas as pd
import csv

# SAW method 

def saw():
    for i in range(N):
        for j in range(M):
            # calculating scores (adding)
            scores[i] += norm[i][j]*Wi[j]
    best=rank() # calling rank function to get the index of best score
    print("\nThe SAW method suggests W" + str(best) + " as the best machinable work material. ") # printing best alternative
    return best # return index of best score

# WPM method


def wpm():
    for i in range(N):
        for j in range(M):
            # calculating scores (Multiplying)
            scores[i] *= pow(norm[i][j], Wi[j])
    best=rank()  # calling rank function to get the index of best score
    print("\nThe WPM method suggests W" + str(best) + " as the best machinable work material. ") # printing best alternative
    return best # return index of best score


# rank function to rank the alternatives acc to scores
def rank():
    for i in range(N):
        scores[i] = numpy.round(scores[i], 4)  # rounding off the scores

    sorted_scores = sorted(scores, reverse=True) # sort the scores
    
    ranks = [0 for i in range(N)]  # initializing array for ranks
    print("\nAi\tScores\t:Rank")
    for i in range(N):
        # get index+1 of values to get rank
        ranks[i] = sorted_scores.index(scores[i])+1
        print(str(i+1)+"\t "+str(scores[i])+"  : " + str(ranks[i])+"\n") # print alternative and their rank

    best=scores.index(sorted_scores[0])+1 # getting index of best score
    return best # return index of best score


#start
choice = int(input("Enter the method:\n1.SAW\n2.WPM\n"))  # choice for method
best=0 # variable for best score index

# getting input values from csv file 
with open('lab1b_input.csv', mode='r') as file:
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
m = [list( map(int,i) ) for i in m]

N=len(m) # Number of alternatives
M=len(attr) # Number of attributes

# calculatin weights
imp_tot=0
for i in imp:
    imp_tot+=i #getting total of importance values

Wi=[]
for i in imp:
    Wi.append(round(i/imp_tot,4))  #calculating weights for each attribute 

minmax = [0 for i in range(M)]  # initializing minmax array

trans = numpy.array(m).T  # taking transpose of array

norm = [[0] * N for i in range(M)]  # initializing normalized array

for i in range(M):
    if(crit[i] == 0):  # if criteria is non beneficial
        minmax[i] = min(trans[i])  # take min value
        # divide min value by the value
        norm[i] = numpy.round(minmax[i]/trans[i], 4)
    else:  # if criteria is non beneficial
        minmax[i] = max(trans[i])  # take min value
        # divide value by max value
        norm[i] = numpy.round(trans[i]/minmax[i], 4)
print("\nMinMax:")
print(minmax) # print MinMax values of each attribute


norm = numpy.array(norm).T  # take transpose
print("\nNormalized array:")
print(norm) #print normalized array

if(choice == 1):
    scores = [0 for i in range(N)]  # initialize scores array
    best=saw()  # call saw method
else:
    scores = [1 for i in range(N)]  # initialize scores array
    best=wpm()  # call wpm method

print("\nThe attribute values of best alternative are:")
# printing the attribute of best working material
for i in range(M):
    print("\n" + attr[i] + " : " + str(m[best-1][i]))