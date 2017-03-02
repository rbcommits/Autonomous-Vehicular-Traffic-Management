import values
import thread
import time
import Intersection
import Queue

queueDoneWaitingX = Queue.Queue()
queueDoneWaitingY = Queue.Queue()


def stopSign(queueX, queueY, gui):

    if(not queueX.empty() and not queueY.empty()):
        values.conventionalStoppedX = True
        values.conventionalStoppedY = True
        carX = queueX.get()
        carY = queueY.get()
        if(carX.positionX >= values.intersection_width / values.intersection_posX - (values.intersection_width / 2)):
            # STOP SIGN STOP THE CAR
            thread.start_new_thread(wait, (carX,))
            carX.velocityX = values.maxVelocity

        if(carY.positionY >= values.intersection_length / values.intersection_posY - (values.intersection_length / 2)):
            # STOP SIGN STOP THE CAR
            thread.start_new_thread(wait, (carY,))
            carY.velocityY = values.maxVelocity

    elif(not queueX.empty()):
        values.conventionalStoppedX = True
        carX = queueX.get()
        thread.start_new_thread(wait, (carX,))

    elif(not queueY.empty()):
        values.conventionalStoppedY = True
        carY = queueY.get()
        thread.start_new_thread(wait, (carY,))

    thread.start_new_thread(process_done_waiting, ())
    # process_done_waiting()


def wait(car):
    ts = time.time()
    car.waiting = True
    xCar = True

    if(car.velocityX > 0):
        car.velocityX = 0
        xCar = True

    else:
        car.velocityY = 0
        xCar = False

    # WAIT THREE SECONDS
    while(True):
        if(time.time() - ts >= values.conventional_stop_sign_wait):
            car.waiting = False

            if(xCar):
                queueDoneWaitingX.put(car)
                values.conventionalStoppedX = False
            else:
                queueDoneWaitingY.put(car)
                values.conventionalStoppedY = False
            return


def process_done_waiting():

    if(not queueDoneWaitingX.empty() and not queueDoneWaitingY.empty()):
        carX = queueDoneWaitingX.get()
        carY = queueDoneWaitingY.get()
        print("in thread")
        carX.velocityX = values.maxVelocity
        time.sleep(1000)
        carY.velocityY = values.maxVelocity

    elif(not queueDoneWaitingX.empty()):
        carX = queueDoneWaitingX.get()
        carX.velocityX = values.maxVelocity

    elif(not queueDoneWaitingY.empty()):
        carY = queueDoneWaitingY.get()
        carY.velocityY = values.maxVelocity

    return
