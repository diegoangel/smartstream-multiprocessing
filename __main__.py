
import db
import ray
import time
import os, os.path
import psutil
import logging
from random import randint
import signal

@ray.remote
class Handler(object):
    def __init__(self):
        logging.info('Initiate actor')
        print('f %d', os.getpid())
        print('f %d', os.getppid())

    def validate(self):
        print(ray.actor.exit_actor())
        logging.info('Validate file')

    def move(self):
        logging.info('Move file')

    def split_content(self):
        logging.info('Split file content')

    def return_file_chunks(self):
        logging.info('Return file chunks')


@ray.remote
def worker(file):
    time.sleep(1)
    db.save(file)
    handler = Handler.remote()
    handler.validate.remote()
    handler.move.remote()
    handler.split_content.remote()
    handler.return_file_chunks.remote()
    print(file)
    print(os.getpid())
    print(os.getppid())
    if file == 4:
        p = psutil.Process(os.getpid())
        #os.kill(os.getpid(), signal.SIGTERM)
    time.sleep(15)


@ray.remote
def some(i):
    print(i)
    print(os.getpid())
    if i == 4:
        p = psutil.Process(os.getpid())
        p.terminate()
        
''' TODO: Error handling, os termination, app errors. Termination over certain conditions reached '''

def main(): 
    timeout = 30
    num_cpus = psutil.cpu_count()
    logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',filename='app.log',level=logging.DEBUG) 
    print(os.getpid())
    print(os.getppid())
    if not ray.is_initialized():
        ray.init(include_webui=True)

    files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

    db.setup()
    print(os.getpid())
    print(os.getppid())
    with ray.profile('Event'):

        for i in range(10):
            time.sleep(randint(0, 4))
            try:
                ray.get(worker.remote(i))
            except Exception as e:
                raise e
                print(e.message)
            finally:
                print('finally')

        #results = [worker.remote(file) for file in (files)]
        #ray.get(results)

if __name__ == '__main__':
    main()
    ray.timeline(filename='timeline.dump')
    print(ray.errors())
