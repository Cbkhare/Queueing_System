from subprocess import Popen, PIPE
import threading
import time

class WorkerManager(object):
    
    def __init__(self, topic, data, sub_list):
        
        self.topic = topic
        self.data = data 
        self.sub_list = sub_list
        self.workers = 10
        self.thread_count = 0
        self.lock = threading.RLock()
        self.consumers = self.consumers_prioirty = {}


    def start(self):
        try:
            self.resolve()
            done = False
            i = 0
            while not done:
                consumer = self.consumers_prioirty[i]
                #print (self.data, self.consumers[consumer].get('execution_path'))
                if self.thread_count >= 10:
                    print ('waiting for 10 sec to get worker')
                    time.sleep(10)
                else:
                    t = threading.Thread(target=self.start_worker_thread,
                                         args=(self.data,
                                               self.consumers[consumer].get('execution_path')))
                    t.start()
                    i+=1
                if i == len(self.consumers_prioirty):
                    done = True
        except Exception as exp:
            raise exp

    def start_worker_thread(self, data, execution_path):
        try:
            self.lock.acquire()
            self.thread_count +=1
            command = 'python ' + execution_path + ' ' + data
            count = 0   # Retry
            while count <3:
                run = Popen(command, shell=True, stdout=PIPE,
                                      stderr=PIPE)
                stdout, stderr = run.communicate()
                print (stdout.strip())
                if not stderr:
                    break
                count +=1
        finally:
            self.lock.release()
            self.thread_count -=1


    def resolve(self):
        self.consumers = {d['username']:d for d in self.sub_list}
        #print(self.sub_list)
        for d in self.sub_list:
            for dependee  in d['dependency']:
                self.consumers_prioirty[dependee] = \
                    self.consumers_prioirty.get(dependee, 0) + \
                    self.consumers_prioirty.get(d['username'], 0) + 1

            self.consumers_prioirty[d['username']]= self.consumers_prioirty.get(d['username'],0) + 1
        self.consumers_prioirty = sorted(self.consumers_prioirty.__iter__(),
                                         key = lambda val:
                                            self.consumers_prioirty[val], reverse=True)
        #print (self.consumers_prioirty)