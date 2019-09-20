import time
import random
import os
from multiprocessing import Process, Queue, current_process, freeze_support

#
# Function run by worker processes
#

def worker(input, output, q):
    for func, args in iter(input.get, 'STOP'):
        result = calculate(func, args)
        print(os.getpid())
        output.put(result)

#
# Function used to calculate result
#

def calculate(func, args):
    result = func(*args)
    return '%s says that %s%s = %s' % \
        (current_process().name, func.__name__, args, result)

#
# Functions referenced by tasks
#

processed_files = []

def process_file(file):
    processed_files.append(file)
    return file

def do_something_else(a, b):
    time.sleep(0.5*random.random())
    return a + b

def watchdog(q):
    """
    This check the queue for updates and send a signal to it
    when the child process isn't sending anything for too long
    """
    while True:
        try:
            msg = q.get(timeout=10.0)
        except queue.Empty as e:
            print("[WATCHDOG]: Maybe WORKER is slacking")
            q.put("KILL WORKER")
#
#
#
def test(files):
    NUMBER_OF_PROCESSES = 4
    TASKS1 = [(process_file, file) for file in range(len(files))]
    TASKS2 = [(do_something_else, None) for i in range(10)]

    q = Queue()

    wdog = Process(target=watchdog, args=(q,))

    # run the watchdog as daemon so it terminates with the main process
    wdog.daemon = True

    # Create queues
    task_queue = Queue()
    done_queue = Queue()

    # Submit tasks
    for task in TASKS1:
        task_queue.put(task)

    # Start worker processes
    for i in range(NUMBER_OF_PROCESSES):
        Process(target=worker, args=(task_queue, done_queue, q)).start()

    wdog.start()
    
    # Get and print results
    print('Unordered results:')
    for i in range(len(TASKS1)):
        print('t1 done \t', done_queue.get(), os.getpid())

    # Add more tasks using `put()`
    for task in TASKS2:
        task_queue.put(task)

    # Get and print some more results
    for i in range(len(TASKS2)):
        print('t2 done\t', done_queue.get())

    # Tell child processes to stop
    for i in range(NUMBER_OF_PROCESSES):
        task_queue.put('STOP')


if __name__ == '__main__':
    files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
    freeze_support()
    test(files)