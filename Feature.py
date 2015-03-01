__author__ = 'Khaleeq'

class Feature(object):
    def __init__(self, name, brainRegion, wbClass, wbType, concepts):
        self.name = name
        self.brainRegion = brainRegion
        self.wbClass = wbClass
        self.wbType = wbType
        self.concepts = concepts