import values
import _thread as thread
import time
import queue as Queue
import Simulation

queueDoneWaitingX = Queue.Queue()
queueDoneWaitingY = Queue.Queue()


def stopSign(queueX, queueY, gui, intersection):

    if(not queueX.empty() and not queueY.empty()):
        intersection.stoppedX = True
        intersection.stoppedY = True
        carX = queueX.get()
        carY = queueY.get()
        intersection.IntersectionList.append(carX)
        intersection.IntersectionList.append(carY)

        if(carX.positionX >= intersection.positionX - (intersection.width / 2)):
            # STOP SIGN STOP THE CAR
            thread.start_new_thread(wait, (carX, intersection))
            carX.velocityX = values.maxVelocity

        if(carY.positionY >= intersection.positionY - (intersection.width / 2)):
            # STOP SIGN STOP THE CAR
            thread.start_new_thread(wait, (carY, intersection))
            carY.velocityY = values.maxVelocity

    elif(not queueX.empty()):
        intersection.stoppedX = True
        carX = queueX.get()
        intersection.IntersectionList.append(carX)
        thread.start_new_thread(wait, (carX, intersection))

    elif(not queueY.empty()):
        intersection.stoppedY = True
        carY = queueY.get()
        intersection.IntersectionList.append(carY)
        thread.start_new_thread(wait, (carY, intersection))

    # thread.start_new_thread(process_done_waiting, ())
    process_done_waiting(gui, queueX, queueY, intersection)


def wait(car, intersection):
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
                intersection.stoppedX = False
            else:
                queueDoneWaitingY.put(car)
                intersection.stoppedY = False

            thread.exit()
            return


'''

POISSON ARRIVAL TIMES

'''


def process_done_waiting(gui, queueX, queueY, intersection):

    if(not queueDoneWaitingX.empty() and not queueDoneWaitingY.empty()):
        # Fetch the cars from the done waiting queues
        print("WE HAVE BOTHHHH")
        carX = queueDoneWaitingX.get()
        carY = queueDoneWaitingY.get()

        if(intersection.proceedVert % 2 == 0):
            intersection.proceedVert += 1

            carX.velocityX = values.maxVelocity

            move_lane(carX, gui, queueX, queueY, intersection)
            print("We're asleep")
            # time.sleep(3)
            # carY.velocityY = values.maxVelocity
            move_lane(carY, gui, queueX, queueY, intersection)

            intersection.stoppedX = False
            intersection.stoppedY = False
        else:
            intersection.proceedVert += 1
            carY.velocityY = values.maxVelocity

            move_lane(carY, gui, queueX, queueY, intersection)
            print("We're asleep")
            # time.sleep(3)
            # carX.velocityX = values.maxVelocity
            carX.velocityX = values.maxVelocity
            move_lane(carX, gui, queueX, queueY, intersection)

            intersection.stoppedX = False
            intersection.stoppedY = False

    elif(not queueDoneWaitingX.empty()):
        print("ELIF X NOT EMPTY")
        # time.sleep(1)

        carX = queueDoneWaitingX.get()
        carX.velocityX = values.maxVelocity
        move_lane(carX, gui, queueX, queueY, intersection)

        intersection.stoppedX = False

    elif(not queueDoneWaitingY.empty()):
        print("ELIF Y NOT EMPTY")
        carY = queueDoneWaitingY.get()
        carY.velocityY = values.maxVelocity
        move_lane(carY, gui, queueX, queueY, intersection)

        intersection.stoppedY = False

    return


def move_lane(car, gui, queueX, queueY, intersection):

    curr_time = time.time()

    while(time.time() - curr_time <= 3):
        # stopSign(queueX, queueY, gui)
        timeStart = time.time()             # TIME START

        # While we move the car queued to move next we must also move all cars beyond the intersection limits to maintain the integrity of the system
        for i in range(0, len(Simulation.carList)):
            if(Simulation.carList[i].ID != car.ID):

                if((Simulation.carList[i].positionX >= intersection.width / 4 + intersection.positionX)):
                    print(" past intersection")
                    Simulation.carList[i].updatePosition(values.timeInterval)
                    gui.moveCar(Simulation.carList[i], values.timeInterval)

                    gui.highlightCar(Simulation.carList[i], "yellow")
                    gui.updateCarInformationDisplay(Simulation.carList[i])

                elif(Simulation.carList[i].positionY >= (intersection.length / 4 + intersection.positionY)):
                    Simulation.carList[i].updatePosition(values.timeInterval)
                    gui.moveCar(Simulation.carList[i], values.timeInterval)

                    gui.highlightCar(Simulation.carList[i], "yellow")
                    gui.updateCarInformationDisplay(Simulation.carList[i])

        car.updatePosition(values.timeInterval)

        gui.moveCar(car, values.timeInterval)

        timeEnd = time.time()           # TIME END

        Simulation.update_car_delay(-(timeEnd - timeStart))

        time.sleep(.01)
