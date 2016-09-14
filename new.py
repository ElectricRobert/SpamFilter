
#####################################################################
#@Title: Spam Email Filter - Training Program
#@Author: Robert Herrera
#@Date: 09/06/2016
#@Last_Updated: 09/08/2016
#@Description: Bayesian Spam Filter
#@Version: 1.0.4
###################################################################
from __future__ import unicode_literals
from collections import Counter
from email.parser import Parser
import sys
import argparse
import string
import re
import os


def main():
	clear_file = open('dictionary.txt','w') # clear dictionary file
	clear_file.close()
	corpus,key_file,train_file = arg_parse()
	parse_files()


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

def email_parser(ptr):
	parser_instance = Parser()
	words = parser_instance.parse(ptr).as_string().lower()
	words = re.sub('[^A-Za-z]', ' ', words)
	return words.split()


def parse_files():

	spam_counter = Counter()
	ham_counter  = Counter()
	file = './trec05p-1/'
	companion_train_path = './CompanionFiles2/train.idx'
	companion_key_path   = './CompanionFiles2/train.key'

	file_paths = open(companion_train_path,'r')
	file_path_stings = file_paths.read().split()

	file_key_path = open(companion_key_path,'r')
	file_keys = file_key_path.read().split()
	count = 0
	for i in range(0,len(file_keys)):

	    with open(file+file_path_stings[i],'r') as filehandle:
	    	words = email_parser(filehandle)

	        if file_keys[i] == 'ham':
	        	ham_counter.update(words)
	        else:
	        	spam_counter.update(words)
	        count += 1

	        printProgress(count,len(file_path_stings),'Forming Dictionary:')



	sys.stdout.write('Finalizing Dictionary.\n')
	sys.stdout.flush()
	# combine ham and spam hash lists
	final_list = spam_counter + ham_counter

	# Close file instances
	file_paths.close()
	file_key_path.close()

	# write to dictioanry
	destination_file = open("dictionary.txt", "a")
	###
	total = 0
	for i in final_list:
		total += 1


	sys.stdout.write('Writing to File.\n')
	sys.stdout.flush()

	count = 0
	for index, (key, value) in enumerate(final_list.items()):
		printProgress(count,total,'Progress...')
		
		destination_file.write('{},{},{}\n'.format(str(key),str(ham_counter[key]),str(spam_counter[key])))
	
			
	   	count += 1
	print count
	print total
	destination_file.close()




def arg_parse():
    
   parser = argparse.ArgumentParser()
     
   parser.add_argument('--corpus', action='store', dest='corpus', help='Absolute path to training corpus file',required=False)

   parser.add_argument('--key_file', action='store', dest='key_file', help='Absolute path to train.key or train key file',required=False)
   
   parser.add_argument('--train_file', action='store', dest='train_file',help='Absolute path to train.idx or train index file',required=False)
   
   parser.add_argument('--version', action='version', version='%(prog)s 1.0.4')

   parser.add_argument('-v', action='version', version='%(prog)s 1.0.4')
   
   
   results = parser.parse_args()
                       
                       
   return (results.corpus,results.key_file,results.train_file)

if __name__ == '__main__':
	main()


