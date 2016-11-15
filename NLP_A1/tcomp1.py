#########################################################
##  CS 4750 (Fall 2016), Assignment #1, Question #1    ##
##   Script File Name: tcomp1.py                       ##
##       Student Name: Caroline Strickland             ##
##         Login Name: cts321                          ##
##              MUN #: 201215555                       ##
#########################################################

'''
tcomp1.py is responsible for, given a master data file, a value for n within an n-gram, and x data files containing a
series of characters, calculating the similarity of each data file to the master data file using the equation
Sim(X, Y) = 1.0 - (Diff(X, Y)/2.0)
'''

import sys
import math

# count command line arguments and import their data as a string
# the counting is required because there may be any number of data files to compare with
dat_count = len(sys.argv[1:])

file = open(sys.argv[1], 'r')
master_file = file.read().replace('\n', ' ')

n = int(sys.argv[2]) # getting the value of n for the n-gram

def frequency_calc(str, word_dict):
    '''
    responsible for calculating and storing the frequency vectors of each data file

    :param str: the string (with new lines removed) from the data file to be calculated
    :param word_dict: the dictionary in which to append information to
    :return: null
    '''
    words = str.split()
    total = 0 # later updates to be the denominator
    temp_n = n-1
    for i in words:
        if len(i) - temp_n > 0:
            total += (len(i) - temp_n)

    for i in words:
        if len(i) >= n:
            char_pos = 0
            for c in range(len(i)-1):
                if char_pos + n <= len(i): # collect the sequence of n letters
                    loop_count = 0
                    pos = char_pos
                    word = [] # word that we are creating with the accumulation of characters
                    while loop_count < n:
                        word.append(i[pos])
                        loop_count += 1
                        pos = pos+1
                    if word_dict.__contains__(''.join(word)): # if the dict already contains this key, update the value
                        word_dict[''.join(word)] += 1
                    else:
                        word_dict[''.join(word)] = float(1.0) # if the dict does not contain this key, create it with a val of 1
                    char_pos += 1

    for key in word_dict:
        word_dict[key] /= total # divide all values over the total

def sim(master_dict, compare_dict):
    '''
    the similarity calculating function, which determines the similarity between the master file and the comparator file

    :param master_dict: the first dictionary to compare (remains the same throughout all comparisons)
    :param compare_dict: the dictionary to compare with the master dictionary (changes throughout comparisons)
    :return: the calculated similarity value
    '''
    total = 0

    for key in master_dict:
        if compare_dict.__contains__(key):
            total += math.fabs(master_dict[key] - compare_dict[key])
            compare_dict.pop(key, None)
        else:
            total += master_dict[key]

    for key in compare_dict:
        total += compare_dict[key] # if we are here, this means that the master_list has 0 of these occurrences
    total = total/2
    total = 1 - total

    return total

top_sim = 0.0 # stores the score of the current top similarity to the master file
top_sim_file = "" # stores the name of the file with the current closest similarity to the master file

# creating the master file dictionary
mast_dict = { }
frequency_calc(master_file, mast_dict)

for x in range(3, dat_count+1): # ranging over the number of included comparator files
    file = open(sys.argv[x], 'r')
    compar_file = file.read().replace('\n', ' ')

    # creating the comparator file dictionary
    compar_dict = { }
    frequency_calc(compar_file, compar_dict)

    # similarity testing
    similarity = sim(mast_dict, compar_dict)
    similarity = format(similarity, '.3f')

    if similarity > top_sim: # check and see if it is the top similarity
        top_sim = similarity
        top_sim_file = sys.argv[x]

    print "Sim(\"" + sys.argv[1] + "\", " + sys.argv[x] + "\") = " + str(similarity)

print "File " + top_sim_file + " is most similar to file " + sys.argv[1]



