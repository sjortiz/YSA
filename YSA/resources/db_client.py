from pymongo import MongoClient


class DB:

    db = None

    def __init__(self, db='mongo'):

        if db == 'mongo':

            conection_string = 'mongodb://mongo:27017/'
            client = MongoClient(conection_string)
            DB.db = client.test_database
