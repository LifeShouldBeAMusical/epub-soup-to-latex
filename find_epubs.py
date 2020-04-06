#python modules
import os
import re
import logging
import datetime
import shutil
import progressbar
#my files
import detect_stuff
import read_epub_into_files
import format_files
import build_logger

time_first = datetime.datetime.now()

print("Initializing")

cwd = os.getcwd()

logger = build_logger.build_logger(cwd, time_first)

total = 0

for root, dirs, files in os.walk(cwd):
	for file in files:
		if file.endswith(".epub"):
			total += 1
print("Total epubs: %d" % total)

scanned = 0
# bar = progressbar.ProgressBar(max_value = total)

for root, dirs, files in os.walk(cwd):
	for file in files:
		filename, ext = os.path.splitext(file)
		if ext == '.epub':
			# print(ext)
			time_last = datetime.datetime.now()
			scanned += 1
			print(filename)
			logger.info(re.sub(r"[^A-z0-9\-]", r"_", filename))
			destpath = os.path.join(root, re.sub(r"[^A-z0-9\-]", r"_", filename))
			if not os.path.exists(destpath):
				os.makedirs(destpath)
			read_epub_into_files.read_into_files(filename, root, destpath, logger)
			fandom = detect_stuff.identify_fandom(destpath, logger)
			format_files.format_files(destpath, fandom, logger)
			elapsed = datetime.datetime.now() - time_last
			logger.info("Time: %02d:%02d.%03d" % (elapsed.seconds // 60, elapsed.seconds % 60, elapsed.microseconds // 1000))
			#print(filename + ": %02d:%02d.%03d" % (elapsed.seconds // 60, elapsed.seconds % 60, elapsed.microseconds // 1000))
			# bar.update(scanned)

elapsed = datetime.datetime.now() - time_first
logger.info("Total Time: %02d:%02d.%03d" % (elapsed.seconds // 60, elapsed.seconds % 60, elapsed.microseconds // 1000))
print("Total Time: %02d:%02d.%03d" % (elapsed.seconds // 60, elapsed.seconds % 60, elapsed.microseconds // 1000))
print("%d Books Scanned" % scanned)
logger.info("%d Books Scanned" % scanned)
