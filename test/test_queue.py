from lib.queue_manager import QueueManager

q = QueueManager(topic='hello', data = "Hello World")

print(q.subscriber_list())
