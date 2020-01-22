import redis
import myconf
import re
import json

queue = "result_queue"
r = redis.Redis(host=myconf.redis_host, port=myconf.redis_port, db=myconf.redis_db)

d = {}

while 1:
	data = r.brpop(queue,2) #for for 2 seconds
	if data:
		json_data = json.loads(data[1])
		for word,count in json_data.items():
			if word in d:
				d[word] += count
			else:
				d[word] = count
	else:
		break

if '' in d:
	d.pop('')

first_five_highest = sorted(d.items(), key=lambda x: x[1], reverse=True)[:5]
print(first_five_highest)