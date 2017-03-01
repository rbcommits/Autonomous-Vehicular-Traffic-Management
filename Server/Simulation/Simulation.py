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
        print "direction"
        direction = Direction

    velocity = values.maxVelocity
    ID = randomIDGenerator()

    if(direction == 1):
        # Generate a vertically traveling car
        car = Car(length=5, width=5, velocityX=velocity, velocityY=0, startX=0, startY=0, ID=ID)
        LiveGUI.drawCar(direction, ID)

    elif(direction == 2):
        # Generate a vertically traveling car
        car = Car(length=5, width=5, velocityX=0, velocityY=velocity, startX=0, startY=0, ID=ID)
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


def cleanList(carList, LiveGUI):
    for i in range(len(carList), 0):
        if(carList[i].positionX > 5 or carList[i].positionY > 5):
            carGUI.carIDs.__delitem__(carList[i].ID)
            del LiveGUI.carDict[carList[i].ID]
            del carList[i]


def simulation(gui):
    # Initialize instance of intersection
    currIntersection = Intersection(length=40, wid=40, posX=490, posY=490)

    for i in range(0, len(carList)):
        carList[i].displayCar()

    elapsedTime = 0                                         # initialize time in seconds
    runSim = True                                           # bool to stop simulation

    # Begin simulation:
    while(runSim):
        if(gui.CheckVar.get() == 1):
            values.conventionalSimFlag = True
        else:
            values.conventionalSimFlag = False

        print("WHILE LOOP")
        print("Intvar", gui.CheckVar.get())
        # Remove processed cars from the intersection list
        # cleanList(carList, gui)

        # Check to see if we should end simulation
        if(elapsedTime > values.simluationTime):
            runSim = False                                  # if time condition is true runSim to false
        elapsedTime += values.timeInterval                         # increment 100 mili second

        # Check if cars are in intersection range
        currIntersection.updateIntersectionQueues(carList, elapsedTime, gui)
        print(values.conventionalSimFlag)
        # Check if this is a conventional simulation
        if(values.conventionalSimFlag):
            print("inside values falg")
            Conventional.stopSign(currIntersection.queueX, currIntersection.queueY, gui)

        # Check if this is an optimized simulation
        else:
            # Restore speeds
            currIntersection.restoreVelocities(carList)
            # Check for possible collisions
            Calculations.collisionDetection(currIntersection.queueX, currIntersection.queueY, gui)

        # Update the positions of the cars in the list
        for i in range(0, len(carList)):
            # THIRD update position
            carList[i].updatePosition(values.timeInterval)

        # Update the GUI positions
        gui.moveCars(carList, values.timeInterval)

        # Every seconds generate new cars
        '''
        if(elapsedTime % values.carGenerationModulo is 0):
            rndCar = randint(1, 2)
            if(rndCar == 1):
                # Generate one car
                newCar = randomCarGenerator(gui, False, 0)
                carList.append(newCar)
            elif(rndCar == 2):
                # Genereate two cars
                for i in range(1, 3):
                    newCar = randomCarGenerator(gui, True, i)
                    carList.append(newCar)
        '''
        if(elapsedTime % values.carGenerationModulo is 0):
            # Generate two cars
            for i in range(1, 3):
                newCar = randomCarGenerator(gui, True, i)
                carList.append(newCar)

        time.sleep(.01)

    print len(carList)
