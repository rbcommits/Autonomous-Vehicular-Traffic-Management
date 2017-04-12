import values
import random


def collisionDetection(queueX, queueY, gui):

    if(not queueX.empty() and not queueY.empty()):
        carX = queueX.get()     # attain x car enterint intersection
        carY = queueY.get()     # attain y car entering intersection

        # Now determine which car entered the inersection first
        if(abs(carX.positionX) < abs(carY.positionY)):
            # X is the first car
            gui.highlightCar(carY, "black")
            slowCar(carSlow=carY, carFull=carX, slowY=True)

        elif(abs(carY.positionY) < abs(carX.positionX)):
            # Y is the first car
            gui.highlightCar(carX, "black")
            slowCar(carSlow=carX, carFull=carY, slowY=False)

        else:
            # Both cars have the same position on their relative axis'
            rollSlow = random.randint(1, 2)
            if(rollSlow == 1):
                slowCar(carSlow=carY, carFull=carX, slowY=True)
            elif(rollSlow == 2):
                slowCar(carSlow=carX, carFull=carY, slowY=False)

    # If the cars in the queue and past the intersection without being regulated yet pop it
    # We dont need it
    elif(not queueX.empty()):
        if(queueX.queue[0].positionX > 490):
            carX = queueX.get()

    elif(not queueY.empty()):
        if(queueY.queue[0].positionY > 490):
            carY = queueY.get()


# Function to reduce velocity of a car
def slowCar(carSlow, carFull, slowY):
    if(slowY):
        while(True):
            carSlow.velocityY = carSlow.velocityY - 0.4
            print("Slowed")
            if(collide(carX=carFull, carY=carSlow) is False):
                break

    elif(not slowY):
        while(True):
            carSlow.velocityX = carSlow.velocityX - 0.4
            print("Slowed")
            if(collide(carX=carSlow, carY=carFull) is False):
                break


# Function to detect a possible collision
def collide(carX, carY):
    # Create two copies of cars to test
    carTestX = carX
    carTestY = carY

    while(True):
        # for i in range(0, 100):
        if(((carTestX.positionX >= carTestY.positionX - 1) and (carTestX.positionX <= carTestY.positionX + 1)) or ((carTestX.positionY >= carTestY.positionY - 1) and (carTestX.positionY <= carTestY.positionY - 1))):
            return True
        if(abs(carTestX.positionX > 600)):
            return False

        carTestX.updatePosition(values.timeInterval)
        carTestY.updatePosition(values.timeInterval)
