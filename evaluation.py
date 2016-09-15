##############################################################################################################
#                                   Spam Email Filter - Evaluation Program
#                                      created by: Robert Herrera
#                                          last updated: 09/06/2016
#
##############################################################################################################

import argparse
import string
import numpy as np
from collections import defaultdict
from collections import Counter
from email.parser import Parser
import re
import math
import sys

#default dictionary text file
dictionary_file = 'dictionary.txt'
#default output key file
# output_key_file = 'output.key'

def main():
    """
    """
    test_file,corpus,dict_text,output_text = arg_parse()
    ham_sum,spam_sum,dictionary_array = calculateColumnSums(dict_text)
    compute_posterior_probability(ham_sum,spam_sum,dictionary_array,test_file,corpus,dict_text,output_text)


def  calculateColumnSums(dict_file):
    """
        @params: 
            dict_file - name of dictionary file or path to dictionary file
        @description:
            - function returns column sum parameters of both ham and spam as well as dictionary to avoid reloading dictionary

    """
    ham_column_sum = 0
    spam_column_sum = 0
    dictionary_array = {}
    print "Preparing Dictionary..."
    with open(dict_file) as f:
        for l in f:
            a = tuple(l.strip().split(','))
            dictionary_array.update({a[0]:{'ham':a[1],'spam':a[2]}})
            ham_column_sum += int(a[1])
            spam_column_sum += int(a[2])
    # print ham_column_sum,spam_column_sum
    return ham_column_sum,spam_column_sum,dictionary_array

def is_ascii(s):
    """
        @params: 
         s - string to be test if non-ascii characters are present
    """
    return all(ord(c) < 128 for c in s)

def email_parser(ptr):
    """
        @params: 
            ptr - file pointer that will be passed. This will read in the current text file 
        @description: email parser will strip word of newlines, digits (numbers), certain length of words and lowercase all words. Special
        and non-printable characters (i.e. hex value 0xff) will be omitted as well
    """
    email_parser = Parser()

    data = email_parser.parse(ptr).as_string()
    words_data = set(data.strip().split())
    #new string list to append to 
    new_string = []
    for elements in words_data:
        if len(elements) < 15 and len(elements) >= 1:
            elements = elements.translate(None,string.punctuation) #strip away punctuation
            elements = elements.lower() # uniformly make all words lowercase
            elements = elements.translate(None,string.digits) # strip all digits 
            if len(elements) >= 1 and is_ascii(elements):
                new_string.append(elements)
    # returns list of filtered words
    return new_string


def compute_posterior_probability(ham_sum,spam_sum,array_dict,test_file,corpus,dict_file,output_file):
    """
        @params: 
            ham_sum - total ham column count returned from calculate columns to reference for probability
            spam_sum - total spam column count returned from calculate columns to reference for probability 
            array_dict - loaded dictionary from text file.
            test_file - file to be evaluated
            corpus - corpus data file
            dict_file - file path to dictionary 
            output_file - desired name of output text
        @description: 
                - function computes posterior probability of each word within a passed email. Overall likelihood 
                is written to desired output file as specifed in output_file upon invocation of evaluation script
    """
    #np.seterr(divide='ignore')
    print 'Evaluating e-mails.'
    dest_file = open(output_file,'w')
    dest_file.close()
    data_paths = open(test_file)
    data = data_paths.read().strip().split()
    data_paths.close()

    write_path = open(output_file,'a')
    master_path = corpus
    
    total = len(data)
    index = 0


    for data_file in data:

        final_ham = 0
        final_spam = 0
        #open master path files
        with open(master_path + data_file,'r') as filehandle:
            words = email_parser(filehandle)

            for word in words:
                if str(word) not in array_dict:
                    continue #if word is not in dict index is skipped to improve speed performance
                else:
                    ham_num = np.float(array_dict[word]['ham'])
                    spam_num = np.float(array_dict[word]['spam'])
            #calculate priors
            #undergo the assumption that 80 percent of email we recieve will be spam
                    p_ham = 0.451  #.55 59-> .94
                    p_spam = 0.549 #.45 41

                    # must re-assign very small value if zero since there is still a small chance
                    if ham_num == 0:
                    # here we make the assuption that even if the word did not occur as spam, there is still a very small probability that 
                    # the word should still contribute to improve accuracy
                        p_word_given_ham = np.divide((1/np.exp(ham_num)),ham_sum) #ham_num / ham_sum 
                    elif spam_num == 0:
                        p_word_given_spam = np.divide((1/np.exp(spam_num)),spam_sum) #spam_num / spam_sum 
                    else:
                        #Compute conditional probabilities (liklihoods)
                        p_word_given_ham = np.divide(ham_num,ham_sum)   #ham_num / ham_sum
                        p_word_given_spam = np.divide(spam_num,spam_sum) #spam_num / spam_sum
                    # p_x = 
                #     #compute posterior probabilities (non-normalized!!!)
                    p3 = np.log(p_word_given_ham) + np.log(p_ham)
                    p4 = np.log(p_word_given_spam) + np.log(p_spam)
                    
                    p_ham_given_word = p3
                    p_spam_given_word = p4

                    final_ham += p_ham_given_word
                    final_spam += p_spam_given_word
 
            # print final_ham,final_spam
            if final_ham > final_spam:
                write_path.write('{}\n'.format('ham'))
            else:
                write_path.write('{}\n'.format('spam'))

        index += 1
        printProgress(index,total,'Loading:')
    print 'File Located in ' + str(output_file)    


def printProgress (iteration, total, prefix = '', suffix = '', decimals = 1, barLength = 100):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        barLength   - Optional  : character length of bar (Int)
    """
    formatStr       = "{0:." + str(decimals) + "f}"
    percents        = formatStr.format(100 * (iteration / float(total)))
    filledLength    = int(round(barLength * iteration / float(total)))
    bar             = '*' * filledLength + '-' * (barLength - filledLength)
    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix)),
    sys.stdout.flush()
    if iteration == total:
        sys.stdout.write('\n')
        sys.stdout.flush()    


#parser arguments to obtain valid input via shell command
def arg_parse():
    
    parser = argparse.ArgumentParser()

    parser.add_argument('--file', action='store', dest='test_file',help='file to be evaluated by spam filter',required=True)
    parser.add_argument('--corpus', action='store', dest='corpus',help='file path to corpus data',required=True)
    parser.add_argument('-d', action='store', dest='dictionary_text_file',help='insert desired dictionary to evaluate',required=True)
    parser.add_argument('--output', action='store', dest='output_key_file',help='desired output text file name',required=True)
    parser.add_argument('--version', action='version', version='%(prog)s 1.0')
    parser.add_argument('-v', action='version', version='%(prog)s 1.0')

    results = parser.parse_args()


    return (results.test_file,results.corpus,results.dictionary_text_file,results.output_key_file)



if __name__ == '__main__':
    main()
