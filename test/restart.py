from util.mongo_client import MongoConnector

conn = MongoConnector()
conn.delete(data={'username':{'$exists':True}})
output = conn.query(data={'username':{'$exists':True}})
print (output)