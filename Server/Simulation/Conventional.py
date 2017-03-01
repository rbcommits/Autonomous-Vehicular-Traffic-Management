import values
import thread
import time


def stopSign(queueX, queueY, gui):
    print("first stop sign line")
   
    if(not queueX.empty() or not queueY.empty()):
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
        carX = queueX.get()
        thread.start_new_thread(wait, (carX,))

    elif(not queueY.empty()):
        carY = queueY.get()
        thread.start_new_thread(wait, (carY,))

    else:
        return


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
        print("WE ARE WAITING")
        if(time.time() - ts >= values.conventional_stop_sign_wait):
            car.waiting = False

            if(xCar):
                car.velocityX = values.maxVelocity
            else:
                car.velocityY = values.maxVelocity

            return
