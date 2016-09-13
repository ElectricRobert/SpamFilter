##############################################################################################################
#                                   Spam Email Filter - Evaluation Program
#                                      created by: Robert Herrera
#                                          last updated: 09/06/2016
#
##############################################################################################################

import idx2numpy
import argparse
import string
import numpy as np
from collections import defaultdict
from collections import Counter
import re
import math
import time
import sys
import json


#subject
#to
#from
#content-type

def main():
    ham_sum,spam_sum,dictionary_array = calculateColumnSums()
    compute_posterior_probability(ham_sum,spam_sum,dictionary_array)


def  calculateColumnSums():
    ham_column_sum = 0
    spam_column_sum = 0
    dictionary_array = {}
    print "Preparing Dictionary..."
    with open('dictionary.txt') as f:
        for l in f:
            a = tuple(l.strip().split(','))
            dictionary_array.update({a[0]:{'ham':a[1],'spam':a[2]}})
            ham_column_sum += int(a[1])
            spam_column_sum += int(a[2])
    # print ham_column_sum,spam_column_sum
    return ham_column_sum,spam_column_sum,dictionary_array

def compute_posterior_probability(ham_sum,spam_sum,array_dict):
    print 'Evaluating e-mails.'
    dest_file = open('output_test.key','w')
    dest_file.close()
    data_paths = open('./CompanionFiles2/test1.idx')
    data = data_paths.read().strip().split()
    data_paths.close()

    write_path = open('output_test.key','a')
    master_path = './trec05p-1/'
    
    total = len(data)
    index = 0

    

    for data_file in data:

        final_ham = -1000
        final_spam = -1000

        with open(master_path + data_file,'r') as filehandle:
            words = str(filehandle.read().strip(string.punctuation))
            # words = ''.join(ch for ch in words if ch not in exclude)
            new_string = re.sub('[^a-zA-Z0-9 \n\.]', '', words) #casting into safe unicode
            words = set(new_string.split())
            words = [ c for c in words if len(c) < 35 ]

            for word in words:
                if word not in array_dict:
                    continue
                else:
                    ham_num = np.float(array_dict[word]['ham'])
                    spam_num = np.float(array_dict[word]['spam'])
            #calculate priors
            #undergo the assumption that 80 percent of email we recieve will be spam
                    p_ham = float(1/5)
                    p_spam = float(4/5)
                    count = 0 
                
                    #Compute conditional probabilities (liklihoods)
                    p_word_given_ham = np.divide(ham_num,ham_sum)   #ham_num / ham_sum
                    p_word_given_spam = np.divide(spam_num,spam_sum) #spam_num / spam_sum

                    # print ham_num,spam_num
                    # print ham_sum,spam_sum
                    # print p_word_given_ham, p_word_given_spam
                    #compute normalization factor (denominator)
                    p1 = np.log1p(p_word_given_ham) + np.log1p(p_ham)
                    p2 = np.log1p(p_word_given_spam) + np.log1p(p_spam)

                    p_word = np.expm1(p1) + np.expm1(p2)

              
                #     #compute posterior probabilities
                    p3 = np.log1p(p_word_given_ham) + np.log1p(p_ham)
                    p4 = np.log1p(p_word_given_spam) + np.log1p(p_spam)
                    
                    p_ham_given_word = p3 - np.log1p(p_word)
                    p_spam_given_word = p4 - np.log1p(p_word)


                    final_ham += p_ham_given_word
                    final_spam += p_spam_given_word
                    count += 1

            if final_ham > final_spam:
                write_path.write('{}\n'.format('ham'))
            else:
                write_path.write('{}\n'.format('spam'))

        index += 1
        printProgress(index,total,'Loading:')
    print 'File Located in output_test.key'    


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
        
#        parser.add_argument('-p', action='store', dest='user_password',
#                            help='Client Credential: Password',required=True)
#            
#                            parser.add_argument('-f', action='store', dest='user_id',
#                                                help='Client Credential: Username (email/lsm)',required=True)
#                            
#                            parser.add_argument('--version', action='version', version='%(prog)s 1.0')
#                            parser.add_argument('-v', action='version', version='%(prog)s 1.0')
#                            
#                            
#                            results = parser.parse_args()
#                            
#                            
#        return (results.user_password,results.user_id)



if __name__ == '__main__':
    print 'Evaluating...\n\n'
    main()
