from .mongo_client import MongoClient

def validate():
    pass

class Consumer(object):

    def __init__(self, username, topic):
        self.conn = MongoClient()
        self.username = username
        self.topic = topic
        

    def subscribe(self):
        try:
            exist = self.if_subscribed()
            if not exist:
                self.conn.insert({'username':self.username, 'topic':self.topic})
        except Exception as exp:
            raise exp

    def if_subscribed(self):
        try:
            found = self.conn.query(data={'username':self.username,
                                          'topic':self.topic})
            if not found:
                return False
            else:
                return True
        except Exception as exp:
            raise exp
