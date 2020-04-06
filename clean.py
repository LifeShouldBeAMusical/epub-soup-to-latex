#python modules
import os
import logging
import datetime
import shutil

#my files
import progress_bar
import build_logger

time_first = datetime.datetime.now()

cwd = os.getcwd()

logger = build_logger.build_logger(cwd, time_first)

total = 0

for root, dirs, files in os.walk(cwd):
	for file in files:
		if file.endswith(".epub"):
			time_last = datetime.datetime.now()
			total += 1
print("Total epubs: %d" % total)

scanned = 0

for root, dirs, files in os.walk(cwd):
	for file in files:
		if file.endswith(".epub"):
			time_last = datetime.datetime.now()
			scanned += 1
			filename = file[:-5]
			#print(filename)
			logger.info(filename)
			sourcepath = os.path.join(root, filename)
			if os.path.exists(sourcepath):
				shutil.rmtree(sourcepath)
				logger.info("\tRemoved source files")
			destpath = os.path.join(root, "LaTeX")
			if os.path.exists(destpath):
				shutil.rmtree(destpath)
				logger.info("\tRemoved destination files")
			elapsed = datetime.datetime.now() - time_last
			logger.info("Time: %02d:%02d.%03d" % (elapsed.seconds // 60, elapsed.seconds % 60, elapsed.microseconds // 1000))
			#print(filename + ": %02d:%02d.%03d" % (elapsed.seconds // 60, elapsed.seconds % 60, elapsed.microseconds // 1000))
			progress_bar.print_progress_bar(scanned, total)

elapsed = datetime.datetime.now() - time_first
logger.info("Total Time: %02d:%02d.%03d" % (elapsed.seconds // 60, elapsed.seconds % 60, elapsed.microseconds // 1000))
print("Total Time: %02d:%02d.%03d" % (elapsed.seconds // 60, elapsed.seconds % 60, elapsed.microseconds // 1000))
print("%d Books Scanned" % scanned)
logger.info("%d Books Scanned" % scanned)
