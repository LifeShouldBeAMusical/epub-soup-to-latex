import os
import logging

def build_logger(cwd, time_first):
	log_folder = os.path.join(cwd, "Logs")
	if not os.path.exists(log_folder):
		os.makedirs(log_folder)
	
	logger = logging.getLogger('myapp')
	hdlr = logging.FileHandler(os.path.join(log_folder, "log_%d-%02d-%02d_%02d-%02d-%02d.log" % (time_first.year, time_first.month, time_first.day, time_first.hour, time_first.minute, time_first.second)))
	formatter = logging.Formatter("%(levelname)s %(message)s")
	hdlr.setFormatter(formatter)
	logger.addHandler(hdlr)
	logger.setLevel(logging.INFO)
	return logger

