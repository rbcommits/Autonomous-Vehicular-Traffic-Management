class Car:

    inQueue = False
    intersectionTimeStamp = 0
    accelerationX = 0           # X Acceleration in meters/(second per second)
    accelerationY = 0           # Y Acceleration in meters/(second per second)
    calculationTime = 0         # Attribute to track the total time spent in calculations

    def __init__(self, length, width, velocityX, velocityY, startX, startY, ID, direction, startTime):
        self.length = length            # Length in meters
        self.width = width              # Width in meters
        self.velocityX = velocityX      # X Velocity in meters/second
        self.velocityY = velocityY      # Y Velocity in meters/second
        self.positionX = startX         # X start coordinate
        self.positionY = startY         # Y start coordinate
        self.ID = ID                    # Give car unique ID
        self.waiting = False            # Set the waiting attribute to false
        self.direction = direction
        self.startTime = startTime      # This is the cars stamped time. We must monitor how much time the car spends inside calculations as well
        self.timeStamped = False

        """ The regulation flag informs the system if the car is currently being regulated by the intersection management module. Once it is released we can bump
        the car up to maximum speed, otherwise it is untouchable. It is false by default """
        self.regulationFlag = False
        self.intersectionFlag = False
        self.guiDeletedFlag = False

    # Print all details of car instance
    def displayCar(self):
        print("Length: " + self.length)
        print("Width: " + self.width)
        print("X Position: " + self.positionX)
        print("Y Position: " + self.positionY)
        print("X Velocity: " + self.velocityX)
        print("Y Velocity: " + self.velocityY)
        print("X Acceleration: " + self.accelerationX)
        print("Y Acceleration: " + self.accelerationY)

    def displayPosition(self):
        print("(" + self.positionX + ", " + self.positionY, ")")

    def displayVelocity(self):
        print("(" + self.velocityX + ", " + self.velocityY, ")")

    def displayAcceleration(self):
        print("(" + self.accelerationX + ", " + self.accelerationX, ")")

    def updatePosition(self, time):
        self.positionX = self.positionX + self.velocityX * time
        self.positionY = self.positionY + self.velocityY * time

    def turn(self, time):
        if(self.direction == "vertical"):
            self.positionX = self.positionX + self.velocityX * time
            self.positionY = self.positionY + self.velocityY * time
        elif(self.direction == "horizontal"):
            self.positionX = self.positionX + self.velocityX * time
            self.positionY = self.positionY + self.velocityY * time

    # Calculate velocity
    def updateVelocity(self, newPositionX, newPositionY):
        self.velocityX = newPositionX - self.positionX
        self.velocityY = newPositionY - self.positionY

    # Calculate acceleartion
    def updateAcceleration(self, newVelocityX, newVelocityY):
        self.accelerationX = newVelocityX - self.velocityX
        self.accelerationY = newVelocityY - self.velocityY

    def getPosition(self):
        return(self.direction + ": (" + str(self.positionX) + ", " + str(self.positionY) + ")")
