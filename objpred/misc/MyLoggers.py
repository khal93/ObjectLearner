__author__ = 'Khaleeq'
import logging
import logging.handlers
import os

SUBJECT_ID = "10" #TODO TODO @@@@ SUBJECT NUMBER


logger = logging.getLogger('logg')
logger.setLevel(logging.DEBUG)   # set root's level

logFile = '../logs/'+SUBJECT_ID+'/full-logs.log'

if os.path.exists(logFile) ==  False:
    f = open(logFile, 'w+')

# file = open(logFile, 'w')
# file.close()

fh = logging.FileHandler(logFile)
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

fileformatter = logging.Formatter("[%(asctime)s] [%(levelname)8s] \n  %(message)s", "%Y-%m-%d %H:%M:%S")
fh.setFormatter(fileformatter)
