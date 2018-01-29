import threading
from helper import threadsafe

import queue

class Foo(object):
    instance_count = queue.Queue()



#@threadsafe
def inc_by(n):
    for i in range(n):
        Foo.instance_count.put(1)


threads = [threading.Thread(target=inc_by, args=(100000,)) for thread_nr in range(100)]
for thread in threads: thread.start()
for thread in threads: thread.join()

print(Foo.instance_count.qsize())  # Expected 10M for threadsafe ops, I get around 5M
