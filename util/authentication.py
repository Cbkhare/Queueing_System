import random

from .mongo_client import MongoConnector

class Authentication(object):

    def __init__(self, username, passwd):
        # create connection
        self.conn = MongoConnector()
        self.username = username
        self.passwd = passwd

    def authenticate(self):
        try:
            passwd = self.passwd.split(self.username)[1]
            if ord(self.username[0]) != int(passwd):
                return False, 'Authentication Failed'
        except Exception as exp:
            return False, 'Exception occurred {0}'.format(exp)
        else:
            return True, 'Success'

    def create_user(self, extra_data=None):
        '''
        :param extra_data: Can be dependency here with URL path to consume
        :return:
        '''
        try:
            # data is inserted in to default collection
            exist = self.conn.query({'username': self.username,
                                     'dependency' :{'$exists':True}})
            if not exist:
                data = {'username': self.username,
                        'token': self.__gen_token()}
                if extra_data:
                    data.update(extra_data)
                self.conn.insert(data)
        except Exception as exp:
            raise exp

    def __gen_token(self):
        bits = [str(random.getrandbits(ord(x))) for x in self.username]
        token = ''.join(bits)
        return token





