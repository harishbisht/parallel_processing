import myconf
import re
import json
import threading
import time
import redis

queue = "q"
r = redis.Redis(host=myconf.redis_host, port=myconf.redis_port, db=myconf.redis_db)


class counting_thread (threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		print("Starting thread")
		_wait = 0
		while 1:
			data = r.brpop("q",5) #5 second timeout
			if not data:
				if _wait > 5:
					raise Exception("No data coming in queue, Exiting Worker")
				_wait += 1
				continue
			push_results_to_temp_list(count_occurance(data[1]))
			print(data)


def count_occurance(string):
	tmp_dict = {}
	nested_string_list = string.decode("utf-8").split("\n")
	for string_list in nested_string_list:

		#removing everthing except char
		string_list = re.sub(r'[^a-zA-Z ]+', '', string_list)

		for word in string_list.replace("\r","").split(" "):
			if word in tmp_dict:
				tmp_dict[word] += 1
			else:
				tmp_dict[word] = 1
	return tmp_dict


def push_results_to_temp_list(results):
	r.lpush("result_queue",json.dumps(results))


# Create new threads
thread1 = counting_thread()
thread2 = counting_thread()

# Start new Threads
thread1.start()
thread2.start()