from nltk.corpus import wordnet as wn
import csv

__author__ = 'Khaleeq'
import logging
import logging.handlers
SUBJECT_ID = "U"

logger = logging.getLogger('logg')
logger.setLevel(logging.DEBUG)   # set root's level

fh = logging.FileHandler('./logs/'+SUBJECT_ID+'/Basic-full.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

fileformatter = logging.Formatter("[%(asctime)s] [%(levelname)8s] \n  %(message)s", "%Y-%m-%d %H:%M:%S")
fh.setFormatter(fileformatter)
