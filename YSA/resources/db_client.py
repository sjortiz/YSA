from pymongo import MongoClient


class DB:

    db = None

    def __init__(self, db='mongo'):

        if db == 'mongo':

            conection_string = 'mongodb://0.0.0.0:32770/'
            client = MongoClient(conection_string)
            DB.db = client.test_database
