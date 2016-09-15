
#####################################################################
#@Title: Spam Email Filter - Training Program
#@Author: Robert Herrera
#@Date: 09/06/2016
#@Last-updated:09/14/16
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


# default dictrioary output path
dictionary_output_file = 'dictionary.txt'

def main():
	"""
    @params:
        arg parse params will pass train and key index
	@Description: invokes training 
	"""
	print 'a'
	corpus,key_file,train_file = arg_parse()

	result = raw_input('Warning: Invoking training will clear current dictionary.txt\nContinue:[Y/n] ')

	if result == 'Y' or result == 'y':
		clear_file = open(dictionary_output_file,'w') # clear dictionary file
		clear_file.close()
		parse_files(corpus,key_file,train_file)
	else:
		print 'Program Exited.'


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


def is_ascii(s):
	"""
	 	@params:
        	s - string to teset if current contents are ascii compatiable
        	return - boolean value
		@Description: tests string characters for asciit
	"""

	return all(ord(c) < 128 for c in s)

def new_parser(ptr):
	"""
	"""
	parser = Parser()

	data = parser.parse(ptr).as_string()
	#eliminates duplicate words within the array of words
	words_data = data.strip().split()
	new_string = []
	for elements in words_data:

		if len(elements) < 18 and len(elements) >= 1:
			elements = elements.translate(None,string.punctuation)
			elements = elements.lower()
			elements = elements.translate(None,string.digits)
			if len(elements) >= 1 and is_ascii(elements):
				new_string.append(elements)
	return new_string


def parse_files(corpus,key_file,train_file):
	"""
    Call in a loop to create terminal progress bar
    @params:
        train file - index train file to be iterated
        corpus file - physical file locations of each iterated file path
        key file    - index key file of correpsonding class
    @ouput:
    	dictionary.txt - default path that training dictionary is written to
    """

    #Counter objects: Implements counting of each word and stores in hashed list
	spam_counter = Counter()
	ham_counter  = Counter()

	#file path to corpus
	file = corpus

	#file path to train index and key index files
	companion_train_path = train_file
	companion_key_path   = key_file

	file_paths = open(companion_train_path,'r')
	file_path_stings = file_paths.read().split()

	file_key_path = open(companion_key_path,'r')
	file_keys = file_key_path.read().split()
	count = 0
	for i in range(0,len(file_keys)):

	    with open(file+file_path_stings[i],'r') as filehandle:
	    	words = new_parser(filehandle)
	
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
	destination_file = open(dictionary_output_file, "a")
	###
	total = 0
	for i in final_list:
		total += 1


	sys.stdout.write('Writing to File.\n')
	sys.stdout.flush()

	count = 0
	for index, (key, value) in enumerate(final_list.items()):
		printProgress(count,total,'Progress...')
		destination_file.write('{},{},{}\n'.format(key,ham_counter[key],spam_counter[key]))

			
	   	count += 1
	print count
	print total
	destination_file.close()




def arg_parse():
    
   parser = argparse.ArgumentParser()
     
   parser.add_argument('--corpus', action='store', dest='corpus', help='Absolute path to training corpus file',required=True)

   parser.add_argument('--key_file', action='store', dest='key_file', help='Absolute path to train.key or train key file',required=True)
   
   parser.add_argument('--train_file', action='store', dest='train_file',help='Absolute path to train.idx or train index file',required=True)
   
   parser.add_argument('--version', action='version', version='%(prog)s 1.0.4')

   parser.add_argument('-v', action='version', version='%(prog)s 1.0.4')
   
   
   results = parser.parse_args()
                       
                       
   return (results.corpus,results.key_file,results.train_file)

if __name__ == '__main__':
	main()


