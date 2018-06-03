import lib.queue_manager as Queue
import redis


class Producer(object):

    def __init__(self, topic, data):
        self.topic = topic
        self.data = data
        self.que_len = 10
        self.redis_conn = redis.StrictRedis(host='localhost', port=6379, db=0)
        self.rpipe = self.redis_conn.pipeline()
        self.queue = Queue.QueueManager(topic= self.topic,
                                         data=self.data)

    def produce(self):
        '''
        This method publishes the data
        :return:
        '''
        try:
            task_length = self.rpipe.llen('task_list').execute()[0]
            if task_length == self.que_len:
                return False
            self.rpipe.lpush('task_list', self.topic)
            self.queue.en_que()
            ##
            # self.rpipe.lpop('task_list', self.topic)
        except Exception as exp:
            raise exp
