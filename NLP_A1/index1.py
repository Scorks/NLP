#########################################################
##  CS 4750 (Fall 2016), Assignment #1, Question #3    ##
##   Script File Name: tcomp1.py                       ##
##       Student Name: Caroline Strickland             ##
##         Login Name: cts321                          ##
##              MUN #: 201215555                       ##
#########################################################

'''
index1.py takes a text file, a file containing ignored words, and an index file (in which to output data to) and
determined the lines that all of the non-ignored words appear in
'''

import sys

final_dict = { } # dictionary for holding all of the words and their associated lines

# collect all lines of text file into a list
with open(sys.argv[2], "r") as ins:
    array = []
    for line in ins:
        array.append(line)
    ins.close()

for x in range(len(array)): # replacing all irrelevant syntax
    array[x] = array[x].replace(',', '')
    array[x] = array[x].replace('!', '')
    array[x] = array[x].replace('.', '')
    array[x] = array[x].replace('\"', '')
    array[x] = array[x].replace('?', '')
    array[x] = array[x].replace(':', '')

# creating the list of words to ignore
file = open(sys.argv[1], 'r')
ignore_file = file.read().replace('\n', ' ')
ignore_file = ignore_file.split()

# for each word, check if it is or isn't in the ignore list. If not, add it to the final dictionary
for x in range(len(array)):
    words = array[x].split()
    for word in words:
        if not ignore_file.__contains__(word): # if the word is not in the ignore list, add it to the final dictionary
            final_dict.setdefault(word, []).append(x+1)

# sorting the words in alphabetical order
keylist = final_dict.keys()
keylist.sort()

index_file = open(sys.argv[3], "w") # open the index file

for key in keylist:
    index_file.write("%s: " % (key))
    index_file.write(','.join(str(x) for x in final_dict[key])) # removing the square brackets
    index_file.write("\n")