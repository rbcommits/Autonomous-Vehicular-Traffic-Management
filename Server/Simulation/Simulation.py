import Calculations
import time
import values
import Conventional
from gui import carGUI
from random import randint
from Car import Car
from Intersection import Intersection


# Initialize array to contain cars
carList = []


def randomCarGenerator(LiveGUI, twoCars, Direction):
    if(not twoCars):
        direction = randint(1, 2)
    else:
        direction = Direction

    velocity = values.maxVelocity
    ID = randomIDGenerator()

    if(direction == 1):
        # Generate a vertically traveling car
        car = Car(length=5, width=5, velocityX=velocity, velocityY=0, startX=0, startY=0, ID=ID, direction="vertical", startTime=time.time())
        LiveGUI.drawCar(direction, ID)

    elif(direction == 2):
        # Generate a vertically traveling car
        car = Car(length=5, width=5, velocityX=0, velocityY=velocity, startX=0, startY=0, ID=ID, direction="horizontal", startTime=time.time())
        LiveGUI.drawCar(direction, ID)

    '''
    elif(direction == 3):
        # Generate cars in both directions
        print ID
        car = Car(length=5, width=5, velocityX=0, velocityY=velocity, startX=0, startY=-20, ID=ID)
        LiveGUI.drawCar(2, ID)
        carList.append(car)
        ID = randomIDGenerator()
        print ID
        car = Car(length=5, width=5, velocityX=velocity, velocityY=0, startX=-20, startY=0, ID=ID)
        LiveGUI.drawCar(1, ID)
        carList.append(car)
    '''

    return car


def randomIDGenerator():
    # Generate a Unique ID
    generateID = True
    while(generateID):
        generateID = False
        ID = randint(0, 10000)
        for i in range(0, len(carGUI.carIDs)):
            if ID == carGUI.carIDs[i]:
                generateID = True
    return ID


def cleanList(carList, gui, currIntersection):
    for i in range(0, len(carList)):
        if((carList[i].positionX > currIntersection.positionX + currIntersection.width * 8) or (carList[i].positionY > currIntersection.positionY + currIntersection.length * 8)):
            if(values.conventionalSimFlag and not carList[i].timeStamped):
                print("THIS CARS POSITION IS: ", carList[i].positionX, carList[i].positionY)
                values.conventional_times.append(time.time() - carList[i].startTime)
                carList[i].timeStamped = True

            elif(not values.conventionalSimFlag and not carList[i].timeStamped):
                print("THIS CARS POSITION IS: ", carList[i].positionX, carList[i].positionY)
                values.optimized_times.append(time.time() - carList[i].startTime)
                carList[i].timeStamped = True

            # del gui.carDict[carList[i].ID]
            # del carList[i]


def simulation(gui):
    # Initialize instance of intersection
    currIntersection = Intersection(length=40, wid=40, posX=490, posY=490)

    elapsedTime = 0                                         # initialize time in seconds
    runSim = True                                           # bool to stop simulation

    # Begin simulation:
    while(runSim):
        if(gui.CheckVar.get() == 1):
            values.conventionalSimFlag = True
        else:
            values.conventionalSimFlag = False

        # Remove processed cars from the intersection list
        cleanList(carList, gui, currIntersection)

        # Check to see if we should end simulation
        if(elapsedTime > values.simluationTime):
            runSim = False                                  # if time condition is true runSim to false
        elapsedTime += values.timeInterval                         # increment 100 mili second

        # Check if cars are in intersection range
        currIntersection.updateIntersectionQueues(carList, elapsedTime, gui)

        currIntersection.restoreVelocities(carList)

        # Check if this is a conventional simulation
        if(values.conventionalSimFlag):
            Conventional.stopSign(currIntersection.queueX, currIntersection.queueY, gui)

        # Check if this is an optimized simulation
        else:
            # Check for possible collisions
            Calculations.collisionDetection(currIntersection.queueX, currIntersection.queueY, gui)

        # Update the positions of the cars in the list
        for i in range(0, len(carList)):
            # THIRD update position
            carList[i].updatePosition(values.timeInterval)

        # Update the GUI positions
        gui.moveCars(carList, values.timeInterval)

        if(not values.conventionalStoppedX and not values.conventionalStoppedY):
            if(elapsedTime % values.carGenerationModulo is 0):
                # Generate two cars
                for i in range(1, 3):
                    newCar = randomCarGenerator(gui, True, i)
                    carList.append(newCar)

        time.sleep(.01)

    if(values.conventionalSimFlag):
        size_conv = len(values.conventional_times)
        sum_conv = 0
        for i in range(0, size_conv):
            sum_conv = sum_conv + values.conventional_times[i]

        avg_conv = sum_conv / size_conv

        print("CONVENTIONAL AVERAGE: ", avg_conv)

    else:
        size_opt = len(values.optimized_times)
        sum_opt = 0
        for i in range(0, size_opt):
            sum_opt = sum_opt + values.optimized_times[i]

        avg_opt = sum_opt / size_opt

        print("OPTIMIZED AVERAGE: ", avg_opt)
