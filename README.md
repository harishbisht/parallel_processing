# Python word count program with parallel processing

### Tech Used:
-  python3
-  Redis for the message queue

#### How to use:
1. create a virtualenv in python3
2. Now run  ```pip install -r requirements.txt```
3. Install Redis and fill the configuration details in myconf.py file
4. now run ```python split_file.py ``` it will split your big file into multiple small files
5. Now run ``` python push_to_queue.py``` it will read the split files and push to the Redis queue. Maximum it will push 4 files data to the queue and wait for the worker process to read from the queue. (using this it will not overflow the Redis queue)
6. Now run ```python worker.py ``` it will start reading from the queue and aggregate the words. You can run worker.py in multiple terminals or in multiple servers. It will start 2 threads in every execution
7. For aggregated results run ```python aggregate_result.py ``` it will print top 5 most used words in the book


If the data size is 1TB then we can optimise the file splitter code and increase number of executor