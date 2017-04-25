import values
import copy
import random

carList = []

def collisionDetection(queueX, queueY, gui, intersection, globalCarList):

    carList = globalCarList

    intersectionList = intersection.IntersectionList

    if(not queueX.empty() and not queueY.empty()):
        carX = queueX.get()     # attain x car enterint intersection
        carY = queueY.get()     # attain y car entering intersection

        intersectionList.append(carX)
        intersectionList.append(carY)

        print(intersectionList)
        input()

        # Now determine which car entered the inersection first
        if(abs(carX.positionX) < abs(carY.positionY)):
            # X is the first car
            gui.highlightCar(carY, "black")
            slowCar(carSlow=carY, carFull=carX, slowY=True, intersection=intersection)
            return

        elif(abs(carY.positionY) < abs(carX.positionX)):
            # Y is the first car
            gui.highlightCar(carX, "black")
            slowCar(carSlow=carX, carFull=carY, slowY=False, intersection=intersection)
            return

        else:

            """ Both cars have the same position on their relative axis """
            rollSlow = random.randint(1, 2)                     # Randomly decide which car to slow down
            if(rollSlow == 1):
                slowCar(carSlow=carY, carFull=carX, slowY=True, intersection=intersection)
                return
            elif(rollSlow == 2):
                slowCar(carSlow=carX, carFull=carY, slowY=False, intersection=intersection)
                return

    # If the cars in the queue and past the intersection without being regulated yet pop it
    # We dont need it
    elif(not queueX.empty()):
        carX = queueX.get()
        intersectionList.append(carX)

        """ We must make sure the intersection is safe to fly through! """
        checkSafePassage(car=carX, intersection=intersection)

    elif(not queueY.empty()):
        carY = queueY.get()
        intersectionList.append(carY)

        """ We must make sure the intersection is safe to fly through! """
        checkSafePassage(car=carY, intersection=intersection)

""" Function to reduce velocity of a car """
def slowCar(carSlow, carFull, slowY, intersection):

    ''' Both these cars are now untouchable by other parts of the program '''
    carSlow.regulationFlag = True
    carFull.regulationFlag = True

    """ Here we slow the car from the Y direction """
    if(slowY):
        while(True):
            carSlow.velocityY = carSlow.velocityY - 0.01
            if(collide(carX=carFull, carY=carSlow, intersection=intersection) is False):
                break

    # Here we slow the car from the X direction
    elif(not slowY):
        while(True):
            carSlow.velocityX = carSlow.velocityX - 0.01
            if(collide(carX=carSlow, carY=carFull, intersection=intersection) is False):
                break


    """ We can now release these cars to the rest of the program """
    carSlow.regulationFlag = False
    carFull.regulationFlag = False

""" Function to detect a possible collision """
def collide(carX, carY, intersection):

    # Create two copies of cars to test
    carTestX = copy.copy(carX)
    carTestY = copy.copy(carY)


    # print(carTestX.getPosition())
    # print(carTestY.getPosition())
    # print("searching for good route")

    while(True):

        # print(str(carTestX.positionX) + " <= " + str(carTestY.positionX + 1) + " and " + str(carTestX.positionX) + " >= " + str(carTestY.positionX - 1))
        if(((carTestX.positionX <= carTestY.positionX + 10) and (carTestX.positionX >= carTestY.positionX - 10)) and 
            ((carTestX.positionY <= carTestY.positionY + 10) and (carTestX.positionY >= carTestY.positionY - 10))):
            return True

        if(abs(carTestX.positionX) > intersection.positionX + intersection.width):
            return False

        carTestX.updatePosition(values.timeInterval)
        carTestY.updatePosition(values.timeInterval)

        # if(((carTestX.positionX >= carTestY.positionX + 1) and (carTestX.positionX <= carTestY.positionX - 1)) or ((carTestX.positionY >= carTestY.positionY + 1) and (carTestX.positionY <= carTestY.positionY - 1))):


def checkSafePassage(car, intersection):

    if(car.direction == "vertical"):
        while(True):
            print("SAFE PASSAGE LOOPING VERTICAL")
            if(collisionSingle(car=car, intersection=intersection)):
                car.velocityY = car.velocityY - 0.01
            else:
                break
    elif(car.direction == "horizontal"):
        while(True):
            print("SAFE PASSAGE LOOPING HORIZONTAL")
            if(collisionSingle(car=car, intersection=intersection)):
                car.velocityX = car.velocityX - 0.01
            else:
                break


def collisionSingle(car, intersection):
    testCar = copy.copy(car)
    copyList = []

    for i in range(len(intersection.IntersectionList)):
        if(car == intersection.IntersectionList[i]):
            continue
        else:
            copyList.append(copy.copy(intersection.IntersectionList[i]))

    while(True):
        if(len(copyList) != 0):
            for i in range(len(copyList)):
                if(((testCar.positionX <= copyList[i].positionX + 11) and (testCar.positionX >= copyList[i].positionX - 11)) and
                   ((testCar.positionY <= copyList[i].positionY + 11) and (testCar.positionY >= copyList[i].positionY - 11))):
                    return True

                if(testCar.direction == "horizontal" and testCar.positionX > intersection.positionX + intersection.width):
                    return False
                if(testCar.direction == "vertical" and testCar.positionY > intersection.positionY + intersection.length):
                    return False

            for i in range(len(copyList)):
                copyList[i].updatePosition(values.timeInterval)
            testCar.updatePosition(values.timeInterval)
        else:
            return False
