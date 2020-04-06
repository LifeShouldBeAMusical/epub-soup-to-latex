import os
import re
import regex_codes

def find_titlepage(path, logger):
	for root, dirs, files in os.walk(path):
		for name in files:
			if(re.search(regex_codes.title_regex, name)):
				return os.path.join(root, name)
	return None

def identify_fandom(path, logger):
	title_path = find_titlepage(path, logger)
	if(title_path):
		with open(title_path, mode='r', encoding='utf-8') as data:
				readIn = data.read()
				if(re.search(regex_codes.b_fandom, readIn)):
					result = re.search(regex_codes.b_fandom, readIn)
					# print("\tFandom(s): %s" % result.group(1))
					logger.info("\tFandom(s): %s" % result.group(1))
					return result.group(1)
				elif(re.search(regex_codes.strong_fandom, readIn)):
					result = re.search(regex_codes.strong_fandom, readIn)
					# print("\tFandom(s): %s" % result.group(1))
					logger.info("\tFandom(s): %s" % result.group(1))
					return result.group(1)
				elif(re.search(regex_codes.b_categories, readIn)):
					result = re.search(regex_codes.b_categories, readIn)
					# print("\tFandom(s): %s" % result.group(1))
					logger.info("\tFandom(s): %s" % result.group(1))
					return result.group(1)
				elif(re.search(regex_codes.strong_categories, readIn)):
					result = re.search(regex_codes.strong_categories, readIn)
					# print("\tFandom(s): %s" % result.group(1))
					logger.info("\tFandom(s): %s" % result.group(1))
					return result.group(1)
				else:
					logger.info("\tFandom Not Found")
					# print("\t" + "No Fandom Detected")
					return None
	else:
		logger.info("\tFandom Not Found")
		# print("\t" + "No Fandom Detected")
		return None

def status(path, logger):
	title_path = find_titlepage(path, logger)
	if(title_path):
		with open(title_path, 'r', encoding='utf-8') as data:
			readIn = data.read()
		if(readIn):
			if(re.search(regex_codes.b_status, readIn)):
				result = re.search(regex_codes.b_status, readIn)
				#print("\tStatus: %s" % result.group(1))
				logger.info("\tStatus: %s" % result.group(1))
				if(re.search(r"Completed", result.group(1))):
					return True
				else:
					return False
			elif(re.search(regex_codes.strong_status, readIn)):
				result = re.search(regex_codes.strong_status, readIn)
				#print("\tStatus: %s" % result.group(1))
				logger.info("\tStatus: %s" % result.group(1))
				if(re.search(r"Completed", result.group(1))):
					return True
				else:
					return False
			else:
				logger.warning("\tStatus Not Found")
				#print("\tSTATUS NOT FOUND")
				return False
	else:
		#print("\tTITLE PAGE NOT FOUND")
		return False

