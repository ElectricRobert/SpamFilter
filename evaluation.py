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
from email.parser import Parser
import re
import math
import sys


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

def email_parser(ptr):
    parser_instance = Parser()
    words = parser_instance.parse(ptr).as_string().lower()
    words = re.sub('[^A-Za-z]', ' ', words)
    return words.split()


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

        final_ham = 0
        final_spam = 0

        with open(master_path + data_file,'r') as filehandle:
            words = email_parser(filehandle)
            # words = [ c for c in words if len(c) < 50 ]
            for word in words:
                if str(word) not in array_dict:
                    continue
                else:
                    ham_num = np.float(array_dict[word]['ham'])
                    spam_num = np.float(array_dict[word]['spam'])
            #calculate priors
            #undergo the assumption that 80 percent of email we recieve will be spam
                    p_ham = 0.58    #.55 -> .94
                    p_spam = 0.42 #.45

                    # print p_ham,p_spam
                    # return
                    
                    #Compute conditional probabilities (liklihoods)
                    p_word_given_ham = np.divide(ham_num,ham_sum)   #ham_num / ham_sum
                    p_word_given_spam = np.divide(spam_num,spam_sum) #spam_num / spam_sum
              
                #     #compute posterior probabilities
                    p3 = np.log(p_word_given_ham) #+ np.log(p_ham)
                    p4 = np.log(p_word_given_spam) #+ np.log(p_spam)
                    # p3 = np.logaddexp(p_word_given_ham,(1/np.exp(p_ham)))
                    # p4 = np.logaddexp(p_word_given_spam,(1/np.exp(p_spam)))
                    
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
