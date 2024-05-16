from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import urllib.parse
import stringConverter
import os
import logging
from dotenv import load_dotenv
load_dotenv()

class MongoDB:
    def __init__(self):
        self.username = urllib.parse.quote_plus(str(os.getenv('MONGO_USER')))
        self.password = urllib.parse.quote_plus(str(os.getenv('MONGO_PASSWORD')))
        self.uri = f"mongodb+srv://{self.username}:{self.password}@dbwebcrawler.zowkqmu.mongodb.net/?retryWrites=true&w=majority&appName=dbWebCrawler"
        self.db_name = str(os.getenv('MONGO_DB_NAME'))
        self.collection = str(os.getenv('MONGO_COLLECTION'))

    def get_db(self):
        # Create a new client and connect to the server
        client = MongoClient(self.uri, server_api=ServerApi('1'))
        db = client[self.db_name]
        db = db[self.collection]
        return db

    def write_to_db(self, input_dict):
        db = self.get_db()
        input_dict["_id"] = f'{input_dict["date"]}{input_dict["destination"]}'

        # check if cancellation exists
        my_query = {"_id": input_dict["_id"]}
        output = db.find(my_query)
        if output.explain().get("executionStats").get("nReturned") != 0:
            db.delete_one(my_query)

        # insert new cancellation
        db.insert_one(input_dict)


    def read_from_db(self, date, station):
        db = self.get_db()

        # format id for search
        date = str(stringConverter.convertDate(date))
        key = date + station + " "
        my_query = {"_id": key}

        # read data
        output = db.find(my_query)
        if output.explain().get("executionStats").get("nReturned") != 1:
            raise Exception

        return output[0]


if __name__ == "__main__":
    test = MongoDB()
    print(test.read_from_db(1, 2))

#{'explainVersion': '1', 'queryPlanner': {'namespace': 'dbWebCrawler.cancellations', 'indexFilterSet': False, 'parsedQuery': {'_id': {'$eq': '22.03.24Muenchen Hbf '}}, 'queryHash': '58F0F49D', 'planCacheKey': 'C14009FE', 'maxIndexedOrSolutionsReached': False, 'maxIndexedAndSolutionsReached': False, 'maxScansToExplodeReached': False, 'winningPlan': {'stage': 'IDHACK'}, 'rejectedPlans': []}, 'executionStats': {'executionSuccess': True, 'nReturned': 0, 'executionTimeMillis': 0, 'totalKeysExamined': 0, 'totalDocsExamined': 0, 'executionStages': {'stage': 'IDHACK', 'nReturned': 0, 'executionTimeMillisEstimate': 0, 'works': 1, 'advanced': 0, 'needTime': 0, 'needYield': 0, 'saveState': 0, 'restoreState': 0, 'isEOF': 1, 'keysExamined': 0, 'docsExamined': 0}, 'allPlansExecution': []}, 'command': {'find': 'cancellations', 'filter': {'_id': '22.03.24Muenchen Hbf '}, '$db': 'dbWebCrawler'}, 'serverInfo': {'host': 'ac-oxzysxr-shard-00-02.zowkqmu.mongodb.net', 'port': 27017, 'version': '7.0.7', 'gitVersion': 'cfb08e1ab7ef741b4abdd0638351b322514c45bd'}, 'serverParameters': {'internalQueryFacetBufferSizeBytes': 104857600, 'internalQueryFacetMaxOutputDocSizeBytes': 104857600, 'internalLookupStageIntermediateDocumentMaxSizeBytes': 16793600, 'internalDocumentSourceGroupMaxMemoryBytes': 104857600, 'internalQueryMaxBlockingSortMemoryUsageBytes': 33554432, 'internalQueryProhibitBlockingMergeOnMongoS': 0, 'internalQueryMaxAddToSetBytes': 104857600, 'internalDocumentSourceSetWindowFieldsMaxMemoryBytes': 104857600, 'internalQueryFrameworkControl': 'trySbeRestricted'}, 'ok': 1.0, '$clusterTime': {'clusterTime': Timestamp(1710930586, 24), 'signature': {'hash': b'f\xe2\xc1\xee\xbb\xf1\x1d\xf1\xc4w%d\xf3P\xa3\xe3v\x02%\x9b', 'keyId': 7289290375896760322}}, 'operationTime': Timestamp(1710930586, 24)}

