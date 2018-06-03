from util.producer import Producer

topic = 'hello'
data = 'Hello World'
publisher = Producer(topic=topic, data=data)
publisher.produce()