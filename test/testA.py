from util.authentication import Authentication
from util.consumer import Consumer
from util.mongo_client import MongoConnector

if __name__=="__main__":
    username = 'Consumer_A'
    passwd = username + str(ord(username[0]))

    authentication_object = Authentication(username, passwd)
    
    status, message = authentication_object.authenticate()
    if not status:  
        exit(0)
    
    extra_data = {
        'dependency': [],
        'execution_path': '../consumers/Consumer_A.py'
    }
    authentication_object.create_user(extra_data)
    #become_consumer = Consumer(username=username, topic='Hello')
    #become_consumer.subscribe()

    conn = MongoConnector()
    r = conn.query(data={'username':username, 'topic':'hello'})
    print (r)
    if not r:
        conn.insert(data={'username':username, 'topic':'hello'})


    