__author__ = 'Khaleeq'
import DatabaseManager as db


# class ConceptList:
    # concepts = ""
    # def __init__(self):
    #     self


print db.query("SELECT featureId, brainRegion, wbClass, wbType FROM features", "")


