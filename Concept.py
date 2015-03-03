__author__ = 'Khaleeq'

class Concept(object):
    def __init__(self, name, wnid, supclass, subclass, freq, features):
        self.name = name
        self.wnid = wnid
        self.supclass = supclass
        self.subclass = subclass
        self.freq = freq
        self.features = features
