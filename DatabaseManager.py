__author__ = 'Khaleeq'

import pymysql
import Learner

class DatabaseManager():
    def __init__(self):
        self.all_features = {}
        self.all_concepts = {}
        self.name ="XS"
        connection = pymysql.connect('localhost', 'root', '', 'objectdb');
        cursor = connection.cursor()


    # Fetch and store all features from db WHERE wbClass != 'taxonomic'
        cursor.execute(""" SELECT *
                        FROM features
                    """)
        features = cursor.fetchall()

    ### Fetch and store all concepts from db
        cursor.execute(""" SELECT *
                        FROM concepts
                    """)
        concepts = cursor.fetchall()
        # print str(features)
        # for feature in features:
        #     print feature[0]
        # for concept in concepts:
        #     print concept[0]
        #
            #
            #     for feature in features:
            # cursor.execute("SELECT f.featureId, f.brainRegion, f.wbClass, f.wbType, cf.conceptId, cf.agreementFreq"
            #             + " FROM features AS f, concept_features AS cf"
            #             + " WHERE f.featureId = '" + feature[0] + "'"
            #             + " AND cf.featureId = f.featureId")

    ### Store all features on an array of Features
        for feature in features:
            # print feature[0]
            cursor.execute("SELECT cf.conceptId, cf.agreementFreq"
            + " FROM features AS f, concept_features AS cf"
            + " WHERE f.featureId = \"" + feature[0] + "\""
            + " AND cf.featureId = f.featureId")

            featCons = dict(map(list, cursor.fetchall()))

            new_feat = {feature[0] : dict(brainregion=feature[1], wbclass=feature[2], wbtype=feature[3], isDisting=feature[5], distinctiveness=feature[6], concepts=featCons)}
            self.all_features.update(new_feat)
            # print type(self.all_concepts)


        # for concept in concepts:

    ### Get subfeatures for each concept, then store each conept as an array of Concepts
        for concept in concepts:
            cursor.execute("SELECT cf.featureId, cf.agreementFreq"
                        + " FROM concepts AS c, concept_features AS cf"
                        + " WHERE c.conceptId = \"" + concept[0] + "\""
                        + " AND cf.conceptId = c.conceptId")
            conFeats = dict(map(list, cursor.fetchall()))


            new_conc = {concept[0] : dict(wnid=concept[1], superclass=concept[2], subclass=concept[3], freq=concept[7],  features=conFeats) }
            self.all_concepts.update(new_conc)


            # print table?
            # print len(table)
            # this_feat = Feature(feature[0], feature[1], feature[2], feature[3], conceptTable)
            # self.all_features.append(this_feat)
            # print all_features

        # ### Concepts
        # cursor.execute(""" SELECT conceptId, bncFreq
        #                 FROM concepts
        #             """)
        # concepts = cursor.fetchall()
        # for concept in concepts:
        #     name = concept[0]
        #
        #     cursor.execute("SELECT featureId, agreementFreq FROM concept_features WHERE conceptId = '" + name + "'")
        #     featTable = cursor.fetchall()
        #     # featTable = None
        #
        #     this_conc = Concept(concept[0], concept[1], featTable)
        #     self.all_concepts.append(this_conc)


        # print all_features

        # def get_features_for(concept):
        #     cursor.execute(""" SELECT conceptId, featureId, agreementFreq
        #                     FROM concept_features
        #                     WHERE conceptId =%s
        #                 """, concept)
        #     data = cursor.fetchall()
        #     return data


### test
print("Fetching from Database...")
database = DatabaseManager()
print("Fetching complete.");
