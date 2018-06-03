from util.authentication import Authentication
from util.mongo_client import MongoConnector

if __name__ == "__main__":
    username = 'Consumer_C'
    passwd = username + str(ord(username[0]))

    authentication_object = Authentication(username, passwd)

    status, message = authentication_object.authenticate()
    if not status:
        exit(0)

    extra_data = {
        'dependency': ['Consumer_A', 'Consumer_B'],
        'execution_path': '../consumers/Consumer_C.py'
    }
    authentication_object.create_user(extra_data)

    conn = MongoConnector()
    r = conn.query(data={'username':username, 'topic':'hello'})
    if not r:
        conn.insert(data={'username':username, 'topic':'hello'})

