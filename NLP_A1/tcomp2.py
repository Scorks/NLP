#########################################################
##  CS 4750 (Fall 2016), Assignment #1, Question #2    ##
##   Script File Name: tcomp1.py                       ##
##       Student Name: Caroline Strickland             ##
##         Login Name: cts321                          ##
##              MUN #: 201215555                       ##
#########################################################

'''
tcomp2.py is responsible for gathering all similar words used within two files, calculating the number of words used, and
using the equation Sim(X, Y) = 1.0 - (SD(X, Y) / (nW(X) + nW(Y))), calculating the similarities between these files (the
master file and a list of files to be compared to it)
'''

import sys

dat_count = len(sys.argv[1:])

file = open(sys.argv[1], 'r')
master_file = file.read().replace('\n', ' ')

def word_set(data, set):
    '''
    function for creating sets of each word within file

    :param data: words separated by spaces (with new lines removed)
    :param set: set for new words to be appended to
    :return: null
    '''
    words = data.split()
    for x in words:
        if not set.__contains__(x): # if the list does not already contain this word, append it to the list
            set.append(x)

def get_unique(master_set, compare_set):
    '''
    function for determining the value of SD(X, Y), the similarity between two sets

    :param master_set: the master set of words
    :param compare_set: the set to compare to the master set
    :return: number of unique words in either set combined
    '''
    total_unique = 0
    for x in master_set:
        if not compare_set.__contains__(x):
            total_unique += 1
    for x in compare_set:
        if not master_set.__contains__(x):
            total_unique += 1
    return total_unique

top_sim = 0.0
top_sim_file = ""

master_set = [ ]
word_set(master_file, master_set)

for x in range(2, dat_count+1):
    file = open(sys.argv[x], 'r')
    compare_file = file.read().replace('\n', ' ')

    compare_set = [ ]
    word_set(compare_file, compare_set)

    SD = get_unique(master_set, compare_set)
    total_words = len(master_set) + len(compare_set)
    similarity = 1 - (float(SD)/float(total_words))
    similarity = format(similarity, '.3f')

    if similarity > top_sim: # check if it is currently the most similar
        top_sim = similarity
        top_sim_file = sys.argv[x]

    print "Sim(\"" + sys.argv[1] + "\", " + sys.argv[x] + "\") = " + str(similarity)

print "File \"" + top_sim_file + "\" is most similar to \"" + sys.argv[1] + "\""
