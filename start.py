from Queue import Queue
from threading import Threading
import datetime
import time
import os
import sys
import pulse

def __main__():
    q = Queue(10000)	#tinker with the size
    producer = Thread(Target=pulse.stream_thread, (args=q,))
    consumer = Thread(Target=pulse.remove_thread, (args=q,))
    #analyzer = Thread(Target=pulse.analysis_thread, (args=q,))

    producer.start()
    consumer.start()
    #analyzer.start()
