import os
import zipfile
import logging

def read_into_files(bookname, cwd, destpath, logger):
	with zipfile.ZipFile(os.path.join(cwd, '%s.epub' % bookname)) as bookIn:
		bookIn.extractall(destpath)
		logger.info("\tFiles Extracted")

