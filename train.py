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
from unidecode import unidecode
import sys
import argparse
import codecs
import string
import re
import evaluation #bayesian evaluation script
import os
from twilio.rest import TwilioRestClient
import time



def main():
	result = promptUser()
	if result == 'Y' or result == 'y':
		clear_file = open('dictionary.txt','w') # clear dictionary file
		clear_file.close()
		corpus,key_file,train_file = arg_parse()
		parse_files()
		evaluation.main()
	else: 
		print 'Program Exited.'
	# else:
	# print 'Program Exited.'
	# sendMessage()
	# os.system('cls' if os.name == 'nt' else 'clear')
	# print 'Done.'

def promptUser():
	return raw_input('Warning: Invoking script will erase current dictionary.txt\nContinue? [Y/n]')



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

def isAscii(s):
    for c in s:
        if c not in string.ascii_letters:
            return False
    return True

def remove_non_ascii(text):
    return unidecode(unicode(text, encoding = "utf-8"))

def strip_non_ascii(string):
    ''' Returns the string without non ASCII characters'''
    stripped = (c for c in string if 0 < ord(c) < 127)
    return ''.join(stripped)


def parse_files():

	# sys.stdout.write('Forming Dictionary...\n')
 #    sys.stdout.flush()
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
	exclude = set(string.punctuation)
	transtab = string.maketrans(",", " ")

	for i in range(0,len(file_keys)):

	    with open(file+file_path_stings[i],'r') as filehandle:
	        words = str(filehandle.read().strip())
	        # words = ''.join(ch for ch in words if ch not in exclude)
	        new_string = re.sub('[^a-zA-Z0-9 .:?!#@$%&\n\.]', '', words) #casting into safe unicode
	        words = new_string.split()
	        # words = [ c for c in words if len(c) < 45]
            
            
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
		if len(key) < 35:
			try:
				destination_file.write('{},{},{}\n'.format(str(key).decode('utf-8'),str(ham_counter[key]),str(spam_counter[key])))
			except:
				sys.stdout.write('Encountered non-ascii occurences.\n')
				sys.stdout.flush()
			
	   	count += 1

	destination_file.close()


def sendMessage():
# Use sms gateway provided by mobile carrier:
    account_sid = "AC2dd04a4cc4e5f67588dd2552e16a1a8d" # Your Account SID from www.twilio.com/console
    auth_token  = "06125ba3b642dee5fb3f391fe867a64b"  # Your Auth Token from www.twilio.com/console

    client = TwilioRestClient(account_sid, auth_token)
    
    if time > 60:

        message = client.messages.create(body="Script Complete.\n Training took .",
                                     to="+19153289455",    # Replace with your phone number
                                     from_="+19152065132") # Replace with your Twilio number
    else:
        message = client.messages.create(body="Script Complete.\n Training took.",
                                         to="+19153289455",    # Replace with your phone number
                                         from_="+19152065132") # Replace with your Twilio number
    print(message.sid)



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


