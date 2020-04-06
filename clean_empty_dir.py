#python modules
import os
import logging
import datetime
import shutil

time_first = datetime.datetime.now()

cwd = os.getcwd()

log_folder = os.path.join(cwd, "Logs")
if not os.path.exists(log_folder):
	os.makedirs(log_folder)

logger = logging.getLogger('myapp')
hdlr = logging.FileHandler(os.path.join(log_folder, "log_%d-%02d-%02d_%02d-%02d-%02d.log" % (time_first.year, time_first.month, time_first.day, time_first.hour, time_first.minute, time_first.second)))
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

total = 0
for root, dirs, files in os.walk(cwd):
	for dir in dirs:
		total += 1

scanned = 0
deleted = 0
for root, dirs, files in os.walk(cwd):
	for dir in dirs:
		scanned += 1
		if not os.listdir(os.path.join(root, dir)):
			shutil.rmtree(os.path.join(root, dir))
			print("EMPTY")
			
