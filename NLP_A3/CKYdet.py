#########################################################
##  CS 4750 (Fall 2016), Assignment #3                 ##
##   Script File Name: CKYdet.py                       ##
##       Student Name: Caroline Strickland             ##
##         Login Name: cts321                          ##
##              MUN #: 201215555                       ##
#########################################################

import sys
import io

# import the grammar and extract the information into a matrix
grammar_file = open(sys.argv[1], 'r') # importing the grammar file from the project folder

set_of_left_values = []
list_of_right_values = []
list_of_rules = []

# filling up the set of left values and the list of right values
for line in grammar_file:
    line_split = line.split() # splits the text into a list of each of the characters

    line_split[2] = line_split[2].replace('"', '') # removing the quotation marks
    list_of_rules.append(line_split)

    left_value = line_split[0]
    if ( set_of_left_values.__contains__(left_value)):
        pass
    else: # if it does not already exist in our set
        set_of_left_values.append(left_value)
    concatenated_string = "" # string that will be added to the columns
    for x in range(2, len(line_split)):
        line_split_addition = line_split[x].replace('"', '') # removing the quotation marks
        if (x == 2):
            concatenated_string += line_split_addition
        else:
            concatenated_string += ", " + line_split_addition
    list_of_right_values.append(concatenated_string)

def print_tbl(s, table):
    '''
    Prints tables in a formatted fashion for easy viewing if user needs it.
    :param s: name of the table to print, for labelling purposes
    :param table: matrix to print (in form of lists nested within lists)
    :return: a formatted printout of the table
    '''
    print s + " TABLE: "
    for list in table:
        print list
    print ""

# populating the empty matrix of the proper size
grammar_matrix = []
for i in range(len(set_of_left_values) +1): # create a list with nested lists
    grammar_matrix.append([])
    for n in range(len(list_of_right_values) +1):
        grammar_matrix[i].append("O") # fills nested lists with data

# filling in the row and column headers
# column headers:
for x in range(0, len(list_of_right_values)):
    grammar_matrix[0][x+1] = list_of_right_values[x]
# row headers
for x in range (0, len(set_of_left_values)):
    grammar_matrix[x+1][0] = set_of_left_values[x]

# populate the table with information from the grammar
row_index = 0
column_index = 0

for list in list_of_rules:
    right_hand_concat = ""
    if (len(list) > 2):
        for x in range(2, len(list)):
            if (x == 2):
                right_hand_concat += list[x]
            else:
                right_hand_concat += ", " + list[x]
        list[2] = right_hand_concat

    # right hand side
    for x in grammar_matrix[0]:
        if (right_hand_concat == x):
            column_index = grammar_matrix[0].index(x)

    # left hand side
    for x in range(0, len(set_of_left_values) + 1):
        if (grammar_matrix[x][0] == list[0]):
            row_index = x

    grammar_matrix[row_index][column_index] = 1

#print_tbl("GRAMMAR MATRIX", grammar_matrix)

# searches for matches within the grammar double matrix
def grammar_searcher(s):
    '''
    Searches grammar for matches and returns a list of the matching row values (LHS values of the given grammar).
    :param s: string to match in the column and search the matrix for
    :return: return_str -list of matches
    '''
    return_str = []
    for x in range(len(grammar_matrix[0])):
        if (s == grammar_matrix[0][x]):
            for y in range(len(set_of_left_values)+1): # go down the column checking for '1's
                if grammar_matrix[y][x] == 1:
                    return_str.append(grammar_matrix[y][0])
    return return_str

def stringify(list1, list2):
    '''
    Unioning together elements of two lists.
    :param list1: list
    :param list2: list
    :return: return_list - a list of strings from unioning together LHS grammar values
    '''
    return_list = []
    if (len(list1) == 0):
        for i in list2:
            return_list.append(i)
    elif (len(list2) == 0):
        for i in list1:
            return_list.append(i)
    else:
        for item in list1:
            for i in list2:
                str = item + ", " + i
                return_list.append(str)
    return return_list

# CKY algorithm function
def CKY_algorithm(utterance_words):
    '''
    Main functionality of the program, uses the CKY algorithm and creates a triangular matrix and fills it following
    the CKY pattern. Also, creates a parse matrix that creates possible parses structured into strings. Also detects
    if a parse can or cannot be reduced to a string.
    :param utterance_words: a list of ordered words in the utterance
    :return:
    '''
    # creating the empty table of n * n (where 'n' is the number of words in the utterance)
    n_value = len(utterance_words)
    cky_table = [] # table to store the CKY triangular matrix
    parsing_table = []
    final_parse_list = [] # list to contain the final parse strings

    for i in range(n_value +1): # create a list with nested lists
        cky_table.append([])
        parsing_table.append([]) # creating empty parsing table
        for n in range(n_value):
            cky_table[i].append([]) # fills nested lists with lists within each cell
            parsing_table[i].append([]) # creating empty parsing table

    # populate the initial (top) row with the words from the utterance file
    for x in range(0, len(utterance_words)):
        cky_table[0][x] = utterance_words[x]
        parsing_table[0][x] = utterance_words[x]

    # populate the next (second) row with the corresponding values for each individual word
    for x in range(len(utterance_words)):
        rule_list = grammar_searcher(utterance_words[x])
        cky_table[1][x] = rule_list

    # check that all words are in the grammar, otherwise it is an automatic fail
    for x in range(len(utterance_words)):
        if (len(cky_table[1][x]) == 0):
            print "No valid parse! The word '" + utterance_words[x] + "' in utterance has no corresponding grammatical values.\n"
            return # if there does not exist a grammar rule for this word, exit automatically

    #populate the second row of the parsing table
    for x in range (len(utterance_words)):
        for y in cky_table[1][x]:
            parser_cell_value = y + " " + cky_table[0][x]
            parsing_table[1][x].append(parser_cell_value)

    # make the matrix diagonal for easier reading in both matrices
    counter = 1
    for x in range(2, len(utterance_words) +1):
        del cky_table[x][:counter]
        del parsing_table[x][:counter]
        counter += 1

    # begin actual algorithm for CKY algorithm
    for x in range(2, len(utterance_words)+1): # for every ROW in the CKY table
        for y in range(len(cky_table[x])): # for every CELL in that row
            diag_list = [] # cells diagonal to the current cell (closest to furthest)
            adj_list = [] # cells adjacent to the current cell (closest to furthest)

            parse_diag_list = []
            parse_adj_list = []
            parse_rules_to_verify = []

            x_index = x
            y_index = y
            # get the diagonal cell values
            for z in range (x-1):
                x_index = x_index - 1
                y_index = y_index + 1
                diag_list.append(cky_table[x_index][y_index])
                parse_diag_list.append(parsing_table[x_index][y_index]) # for parsing purposes

            x_index = x
            y_index = y
            # get the adjacent cell values
            for z in range (x-1):
                x_index = x_index - 1
                adj_list.append(cky_table[x_index][y_index])
                parse_adj_list.append(parsing_table[x_index][y_index]) # for parsing purposes

            # we have both the list of diagonal and adjacent cell values, now we union
            rules_to_verify = []
            diag_index = 0
            for item in range(len(adj_list), 0, -1):
                rules_to_verify.append(stringify(adj_list[item-1], diag_list[diag_index]))

                if (len(parse_adj_list[item-1]) == 0):
                    parse_rules_to_verify.append(parse_diag_list[diag_index])
                elif (len(parse_diag_list[diag_index]) == 0):
                    parse_rules_to_verify.append(parse_adj_list[item-1])
                else:
                    j = str(parse_adj_list[item-1])
                    k = str(parse_diag_list[diag_index])
                    l = j + k # the concatenation of both elements for parsing
                    parse_rules_to_verify.append(l)

                diag_index += 1

            # verify whether or not the 'rules_to_verify' list contains any grammar rules
            for item in rules_to_verify:
                for inner_list in item:
                    n = rules_to_verify.index(item)
                    for a in grammar_searcher(inner_list):
                        cky_table[x][y].append(a)
                        l =  a + ''.join(parse_rules_to_verify[n])
                        #l = a + parse_rules_to_verify[n]
                        l = l.replace("\\", '')
                        l = l.replace('"', '')
                        if (a == 'S' and x == len(utterance_words) and y == len(cky_table[x])-1):
                            final_parse_list.append(l)
                        parsing_table[x][y].append(l) # adding values to the parse table cell

            # double checking to make sure that none of the current cell items can be reduced down to an 'S'
            for item in cky_table[x][y]:
                n = cky_table[x][y].index(item)
                for a in grammar_searcher(item):
                    cky_table[x][y].append(a)
                    l =  a + ''.join(parse_rules_to_verify[n])
                    #l = a + parse_rules_to_verify[n]
                    l = l.replace("\\", '')
                    l = l.replace('"', '')
                    if (a == 'S' and x == len(utterance_words) and y == len(cky_table[x])-1):
                        final_parse_list.append(l)
                    parsing_table[x][y].append(l) # adding values to the parse table cell


    # printing all valid parses
    if (len(final_parse_list) == 0):
        print "No valid parse! \n"
    else:
        count = 1
        for x in final_parse_list:
            print "parse #" + str(count) + ": " + x
            count += 1
            print ""

    #print_tbl("CKY", cky_table)
    print_tbl("PARSING", cky_table)
    print_tbl("CKY", parsing_table)

utterance_words_line = []

# import and add all words in the utterance to a list

# main---------------------------------------------------------------------------------------

utterance_file = open(sys.argv[2], 'r')

count = 0
for line in utterance_file:
    count += 1
    line_split = line.split()
    prnt = str(line_split)
    # removing all extra symbols
    prnt = prnt.replace('[', '')
    prnt = prnt.replace(']', '')
    prnt = prnt.replace(',', '')
    prnt = prnt.replace("'", '')
    print "Utterance #" + str(count) +": " + prnt
    for x in line_split:
        utterance_words_line.append(x)
    CKY_algorithm(utterance_words_line)
    utterance_words_line = []