from pymongo import MongoClient

class MongoConnector(object):

    def __init__(self, db_name='test'):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client[db_name]


    def get_collection(self, collection='queue_test'):
        try:
            return self.db[collection]
        except Exception as e:
            # to be logged
            return None

    def insert(self, data, collection='queue_test'):
        try:
            coll = self.get_collection(collection)
            coll.insert_one(data)
        except Exception as e:
            # to be logged
            return None

    def query(self, data, conditions = None, collection='queue_test'):
        try:
            coll = self.get_collection(collection)
            found_data = coll.find(data)
            # add conditions
            return list(found_data)
        except Exception as e:
            # to be logged
            return None

    def update(self, id, new_data, collection='queue_test'):
        try:
            coll = self.get_collection(collection)
            # should be handled at call data = self.query(update_for)
            coll.update({'_id': id}, new_data, True)
        except Exception as e:
            # to be logged
            return None

    def delete(self, data, collection='queue_test'):
        try:
            coll = self.get_collection(collection)
            output = coll.delete_many(data)
            return output
        except Exception as exp:
            raise exp
