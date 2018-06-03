import uuid

from .worker_manager import WorkerManager
from util.mongo_client import MongoConnector

class QueueManager(object):


    def __init__(self, topic, data):
        self.topic = topic
        self.data = data
        self.id = self.gen_pid()
        self.conn = MongoConnector()
        self.stack = []

    def en_que(self):
        '''
        This method instantiates the Worker Manager and steps to execute Worker
        :return:
        '''
        try:
            self.sub_list = self.subscriber_list()
            worker = WorkerManager(self.topic, self.data, self.sub_list)
            worker.start()
        except Exception as exp:
            raise

    def subscriber_list(self):
        '''
        This method fetches all the subscribers according to the topic
        :return:
        '''
        #list = self.conn.query({'topic':{'$exists':True}})
        list = self.conn.query({'topic' : self.topic})
        sub_list = []
        for sub in list:
            username = sub['username']
            data = self.conn.query({'username' : username,
                                    'dependency' :{'$exists':True}})
            if data:
                sub_list.append(data[0])
        return sub_list

    def gen_pid(self):
        return str(uuid.uuid4())