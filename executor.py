import multiprocessing

class Executor:
    def __init__(self, process_num):
        self.args = []
        self.error = 0
        self.results = []
        self.pool = multiprocessing.Pool(process_num)

    def prompt(self, result):
        print(result)
        if result:
            print("prime")
            self.results.append(result)
            #self.pool.terminate()

    def schedule(self, function, args):
        
        self.r = self.pool.apply_async(function, args=args, callback=self.prompt, error_callback= self.cb_error)
        self.args.append(args)

    def wait(self):
        self.pool.close()
        self.pool.join() 

    def cb_error(self, result):
        print(self.args)

        self.error += 1
        self.results.append('error')
        print(self.error)
        print('error')

def g(q, r):
    if q == 3:
        raise('chau')    
    if q == 6:
        raise('chau 2')
    print('g function', q, r)
    return q

def main(process_num):
    executor = Executor(process_num)
    for i in range(process_num):
        executor.schedule(g, [i, 4])
    executor.wait()
    print(executor.results)

main(8)