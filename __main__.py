
import db
import ray
import time
import os, os.path
import psutil
import logging

timeout = 30
num_cpus = psutil.cpu_count()
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',filename='app.log',level=logging.DEBUG) 

if not ray.is_initialized():
    ray.init(include_webui=True)

@ray.remote
class Handler(object):
    def __init__(self):
        logging.info('Initiate actor')

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

def some(i):
    time.sleep(2)
    print(i)
    
''' TODO: Error handling, os termination, app errors. Termination over certain conditions reached '''

def main(): 

    files = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M']

    db.setup()

    with ray.profile('Event'):

        for _ in range(4):
            ray.get(worker.remote(i))

        #results = [worker.remote(file) for file in (files)]
        #ray.get(results)

if __name__ == '__main__':
    main()
    ray.timeline(filename='timeline.dump')
    print(ray.errors())
