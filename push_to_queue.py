import os, time
import redis
import queue #queue is used for splitted file names
import myconf

#getting all files name in a queue
local_queue = queue.Queue()
[local_queue.put(i) for i in os.listdir(myconf.split_folder)]


#distributed redis queue for distributed processing
queue = "q"
r = redis.Redis(host=myconf.redis_host, port=myconf.redis_port, db=myconf.redis_db)


#now pushing the splitted files data to global redis queue, so every worker can read in distributed way 
sleep_time = 0
while local_queue.qsize():
	if r.llen(queue) > 4: #checking queue length so that it will not spam or overfilled the queue
		print("queue size exceeded. waiting for worker. sleeping for %s seconds"%(sleep_time))
		sleep_time += 1
		time.sleep(sleep_time)
	else:
		filename = local_queue.get_nowait()
		with open(os.path.join(myconf.split_folder,filename), 'rb') as f:
			r.lpush(queue,f.read())
		print(filename)
		sleep_time=0
