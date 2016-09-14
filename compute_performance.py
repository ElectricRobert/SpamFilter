import argparse


def main():
	test_file, target_file = arg_parse()
	compute_performance(test_file,target_file)

def compute_performance(test_file,target_file):
	final_count = 0

	#loaded in dictionary to utilize speed of hash mapping
	#open test file to be compared
	test_file_path = open(test_file,'r')
	test_file_dict = {}
	for index,line in enumerate(test_file_path):
		test_file_dict.update({str(index):line.strip()})
	test_file_path.close()

	#open acutal file to be compared
	key_file_path = open(target_file,'r')
	key_file_dict = {}
	for index,line in enumerate(key_file_path):
		key_file_dict.update({str(index):line.strip()})
	key_file_path.close()



	for key in test_file_dict:
		if test_file_dict[key] == key_file_dict[key]:
			final_count += 1


	print 'Accuracy: ' + str((float(final_count)/float(len(key_file_dict)))*100) + '%'



def arg_parse():
    
	parser = argparse.ArgumentParser()
	parser.add_argument('--test', action='store', dest='test_file',help='file to be compared to actual key',required=True)
	parser.add_argument('--target', action='store', dest='target_file',help='Actual key to be compared',required=True)                      
	parser.add_argument('--version', action='version', version='%(prog)s 1.0')
	parser.add_argument('-v', action='version', version='%(prog)s 1.0')                   
	results = parser.parse_args()
                             
	return (results.test_file,results.target_file)


if __name__ == '__main__':
	main()