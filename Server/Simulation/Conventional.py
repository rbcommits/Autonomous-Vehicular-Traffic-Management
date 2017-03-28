import values
import thread
import time
import Queue
import Simulation

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

    # thread.start_new_thread(process_done_waiting, ())
    process_done_waiting(gui, queueX, queueY)


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

            thread.exit()
            return


def process_done_waiting(gui, queueX, queueY):

    if(not queueDoneWaitingX.empty() and not queueDoneWaitingY.empty()):
        # Fetch the cars from the done waiting queues
        print("WE HAVE BOTHHHH")
        carX = queueDoneWaitingX.get()
        carY = queueDoneWaitingY.get()

        if(values.proceedVert % 2 == 0):
            values.proceedVert += 1

            carX.velocityX = values.maxVelocity
            # .conventionalStoppedX = False
            # values.conventionalStoppedY = True
            move_lane(carX, gui, queueX, queueY)
            print("We're asleep")
            # time.sleep(3)
            # carY.velocityY = values.maxVelocity
            move_lane(carY, gui, queueX, queueY)

            values.conventionalStoppedX = False
            values.conventionalStoppedY = False
        else:
            values.proceedVert += 1
            carY.velocityY = values.maxVelocity
            # values.conventionalStoppedX = True
            # values.conventionalStoppedY = False
            move_lane(carY, gui, queueX, queueY)
            print("We're asleep")
            # time.sleep(3)
            # carX.velocityX = values.maxVelocity
            carX.velocityX = values.maxVelocity
            move_lane(carX, gui, queueX, queueY)

            values.conventionalStoppedX = False
            values.conventionalStoppedY = False

    elif(not queueDoneWaitingX.empty()):
        print("ELIF X NOT EMPTY")
        # time.sleep(1)

        carX = queueDoneWaitingX.get()
        carX.velocityX = values.maxVelocity
        move_lane(carX, gui, queueX, queueY)

    elif(not queueDoneWaitingY.empty()):
        print("ELIF Y NOT EMPTY")
        print("STOPPEDX = ", values.conventionalStoppedX, " STOPPED Y = ", values.conventionalStoppedY)
        # time.sleep(1)

        carY = queueDoneWaitingY.get()
        carY.velocityY = values.maxVelocity
        move_lane(carY, gui, queueX, queueY)

    return


def move_lane(car, gui, queueX, queueY):

    curr_time = time.time()

    while(time.time() - curr_time <= 1.4):
        print("SPECIAL MOVE")

        # stopSign(queueX, queueY, gui)
        timeStart = time.time()             # TIME START

        # While we move the car queued to move next we must also move all cars beyond the intersection limits to maintain the integrity of the system
        for i in range(0, len(Simulation.carList)):
            if(Simulation.carList[i].ID != car.ID):

                if((Simulation.carList[i].positionX >= values.intersection_width + values.intersection_posX) / 1.11):
                    Simulation.carList[i].updatePosition(values.timeInterval)
                    gui.moveCar(Simulation.carList[i], values.timeInterval)

                    gui.highlightCar(Simulation.carList[i], "yellow")
                    gui.updateCarInformationDisplay(Simulation.carList[i])

                elif(Simulation.carList[i].positionY >= (values.intersection_length + values.intersection_posY) / 1.11):
                    Simulation.carList[i].updatePosition(values.timeInterval)
                    gui.moveCar(Simulation.carList[i], values.timeInterval)

                    gui.highlightCar(Simulation.carList[i], "yellow")
                    gui.updateCarInformationDisplay(Simulation.carList[i])

        car.updatePosition(values.timeInterval)

        gui.moveCar(car, values.timeInterval)

        timeEnd = time.time()           # TIME END

        Simulation.update_car_delay(-(timeEnd - timeStart))

        time.sleep(.01)
