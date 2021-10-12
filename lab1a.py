"""
Name:Bhargavi Poyekar
BE COMPS/ Batch-C
UID: 2018130040
Roll No:45
Date of lab: 25/08/21
Aim: 1a) To implement SAW and WPM method for a given problem [General]
 
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
    return

# WPM method


def wpm():
    for i in range(N):
        for j in range(M):
            # calculating scores (Multiplying)
            scores[i] *= pow(norm[i][j], Wi[j])
    return


choice = int(input("Enter the method:\n1.SAW\n2.WPM\n"))  # choice for method

RN = int(input("Enter roll no:\n"))  # input roll no
N = 93+RN % 11  # calculating N: Number of alternatives.
M = 70+RN % 11  # calculating M: Number of attributes.

m = [[0] * M for i in range(N)]  # initializing array for measurements
s = RN-RN % 11  # start value of range
e = RN+RN % 11  # end value of range
random.seed(20)  # for getting same values each time

Wi=[0 for i in range(M)]
for i in range(M):
    Wi[i]=random.randint(10,M+10) # random weights 

Wi=numpy.array(Wi) # convert list to numpy array
sum=numpy.sum(Wi) # sum of weights
Wi=numpy.divide(Wi,sum) # divide each element by sum 

# assigning random measurements in the given range
for i in range(N):
    for j in range(M):
        m[i][j] = random.randint(s, e)

# for i in range(N):
#     print(m[i])  # printing the measurements

with open('lab1a_data.csv', 'w', newline="") as f:
    write = csv.writer(f)
    write.writerows(m)

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
print("\nCriteria (1 for benefecial and 0 for non-beneficial):")
print(crit)  # print criteria

minmax = [0 for i in range(M)]  # initializing minmax array

trans = numpy.array(m).T  # taking transpose of array

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

# for i in range(N):
#     print(norm[i])  # print normalized array

# exporting normalized array to csv file
with open('lab1a_norm.csv', 'w', newline="") as f:
    write = csv.writer(f)
    write.writerows(norm)


# menu
if(choice == 1):
    scores = [0 for i in range(N)]  # initialize scores array
    saw()  # call saw method
else:
    scores = [1 for i in range(N)]  # initialize scores array
    wpm()  # call wpm method

for i in range(N):
    scores[i] = numpy.round(scores[i], 5)  # rounding off the scores

# sort the list in descending order and remove repeat values
sorted_scores = list(set(sorted(scores, reverse=True)))
ranks = [0 for i in range(N)]  # initializing array for ranks
print("\nAi\tScores\t:Rank")
for i in range(N):
    # get index+1 of values to get rank
    ranks[i] = sorted_scores.index(scores[i])+1
    print(str(i+1)+"\t "+str(scores[i])+" : " + str(ranks[i])+"\n")

dict = {'Ai': scores, 'Rank': ranks}  # dictionary for dataframe
df = pd.DataFrame(dict)  # Creating pandas dataframe
df.index += 1  # start index in csv file from 1
# saving the dataframe to csv file
df.to_csv('lab1a.csv')

best=scores.index(sorted_scores[0])+1 # getting index of best score
print("\nThe method suggests A" + str(best) + " as the best machinable work material. ") # printing best alternative
print("\nThe attribute values of best alternative are:")
# printing the attribute of best working material
for i in range(M):
    print("B"+str(i+1) + ": " + str(m[best-1][i]), end=" ")