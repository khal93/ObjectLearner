__author__ = 'Khaleeq'

from GlobalDb import *
import numpy as np


def middle(nums):
    nums.sort()
    length = len(nums)
    half = length//2
    # if length % 2:                  #if even, return the half
    # print half #TODO LOG THIS
    return nums[half]
    # else:                            #if odd
    #     return (nums[half] + nums[half-1] )/2



def topObjects(d, nots):

    tops = d.copy()
    # limit = int(np.mean(tops.values()))
    limit = int(np.percentile(d.values(), 75))

    for o in tops.keys():
        if (int(tops.get(o)) < limit):# or (o in nots):
            del tops[o]
        # if (len(d) > 0): #and (o in nots):
        #      del d[o]
    # print str(nots)+"::NOTS"
    # print str((limit)) +":"+ str(len(tops))

    if len(tops) > 0:
        return tops
    else:
        return d

def modifyScore(d, key, value):
    if key in d.keys():
        if isinstance( value, ( int, long, float ) ):
            d[key] = d.get(key) + value
        # print "\t :" + key + " +" + str(value) + "\t : "+ str(d.get(key))

def removeObject(d, key):
    del d[key]
    print "\t :" + key + " X"

def getEffected(objects, question, all_features):
    effected = all_features[question]['concepts']
    # intersection = effected.viewkeys() & objects.viewkeys()
    # for o in effected.keys():
    #     if not (o in intersection):
    #         del effected[o]

    # print effected.keys()
    return effected
