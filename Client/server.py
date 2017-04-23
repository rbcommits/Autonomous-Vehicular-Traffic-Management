import zmq
import sys
import threading
import time
from Car import Car
from Queue import *
# import Queue
import zlib, pickle as pickle
import signal

PORT = 'tcp://*:5570'   # change this to whatever port you want your server to run on

# define a list of server workers
server_workers = []
car_queue = Queue()         # feel free to change the name! I just needed a dummy placeholder to send messages back lol
velocity_queue = Queue()


def tprint(msg):
    """like print, but won't get newlines confused with multiple threads"""
    sys.stdout.write(msg + '\n')
    sys.stdout.flush()





def simulate(ID, msg):
    # start simulation here

    velocity_queue = car_queue                      # remove this once you start populating this queue via the algorithm

    worker_ID, car = velocity_queue.get()

    worker = object()

    print("server for loop")
    for workers in server_workers:
        print("workers.ID = ", workers.ID, "worker_ID = ", worker_ID)
        if worker_ID == workers.ID:
            worker = workers

    # Create packet
    # msg = "Hello from worker " + str(worker.ID)

    # Send packet to car
    print("about to send message")
    worker.worker.send_multipart([ID, msg])


def update_queue(object):
    print("OBJECT TUPLE = ", object)
    car_queue.put(object)
    # simulate()


def deserialize(msg):
    """inverse of send_zipped_packet"""
    p = zlib.decompress(msg)
    return pickle.loads(p)


class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind(PORT)

        backend = context.socket(zmq.DEALER)
        backend.bind('inproc://backend')

        global server_workers
        for i in range(5):
            worker = ServerWorker(context, i)           # i will be the unique worker ID
            worker.start()
            server_workers.append(worker)

        zmq.proxy(frontend, backend)

        frontend.close()
        backend.close()
        context.term()


class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context, ID):
        threading.Thread.__init__(self)
        self.context = context
        self.ID = ID
        self.worker = self.context.socket(zmq.DEALER)
        self.worker.connect('inproc://backend')

    def run(self):
        tprint('Worker started')
        while True:
            ID, msg = self.worker.recv_multipart()
            msg = deserialize(msg)


            # Add to queue here (both ID and message as an object)
            # or update queue if car ID already exixts

            # We include the ID of the worker who received the request so we can later use the same
            # worker to send the updated velocity back
            #car = Car(length=msg.length, width=msg.width, velocityX=msg.velocityX, velocityY=msg.velocityY, startX=msg.positionX, startY=msg.positionY, ID=msg.ID, direction=msg.direction, startTime=msg.startTime)
            #update_queue(car)
            print "got data from client: ", msg.in_intersection
            #  car_queue.queue(car)
            # somequeue.queue(car)
            # worker.send_multipart([ID, msg])

        self.worker.close()



# def main_func():
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    server = ServerTask()
    server.start()
    server.join()
