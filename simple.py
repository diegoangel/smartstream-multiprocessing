import time
import random
import os
import multiprocessing as mp
import signal
import db

db.setup()

def signal_handler(signum, frame):
    print("Termination request received!")
    exit()

if not os.name == 'nt':
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
else:
    signal.signal(signal.CTRL_C_EVENT  , signal_handler)
    signal.signal(signal.CTRL_BREAK_EVENT, signal_handler)    
    signal.signal(signal.CTRL_CLOSE_EVENT, signal_handler)    
    signal.signal(signal.CTRL_SHUTDOWN_EVENT, signal_handler)    

def process(file, q):
    q.put(file)
    if file == 'B':
        time.sleep(6)
    db.save(file)
    if file == 'F':
        raise TimeoutError
    print(file, os.getpid())
    return file

if __name__ == '__main__':
    files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']
    
    ''' Windows support only this method '''
    mp.set_start_method('spawn')
    
    PROCESSES = 5

    for file in files:
        try:
            q = mp.Queue()
            p = mp.Process(target=process, args=(file, q))
            p.start()
        
            q.get()
            p.join(timeout=5) 
            if p.exitcode == 1 or p.exitcode == None:
                print(file, 'failed with pid: ', p.pid)
        except TimeoutError as e:
            print(e)
            p.kill()
     
    p.close()
    p.join()
