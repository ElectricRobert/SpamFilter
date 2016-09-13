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
import string



def main():
	clean()

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

def clean():
	print 'Cleaning biases...'
	dest_file = open('cleaned_dictionary.txt','w')
	dest_file.close()

	write_file = open('cleaned_dictionary.txt','a')
    
	
	file_path = open('dictionary.txt')
	for line in file_path:
		a = line.strip().split(',')
		if int(a[1]) == 0 and int(a[2]) == 1:
			continue
		elif int(a[1]) == 1 and int(a[2]) == 0:
			continue
		elif int(a[1]) == 1 and int(a[2]) == 1:
			continue
		elif int(a[1]) == 0 or int(a[2]) == 0:
			continue
		else:
			write_file.write('{},{},{}\n'.format(a[0],a[1],a[2]))
	


if __name__ == '__main__':
	main()
	print 'Done.'