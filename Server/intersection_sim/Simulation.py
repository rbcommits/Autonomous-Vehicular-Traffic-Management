import Calculations
from Car import Car
from Intersection import Intersection


# Initialize instance of intersection
currIntersection = Intersection(100, 100, 10, 10)


# Declare cars:
# (self, length, width, velocityX, velocityY, startX, startY)
car1 = Car(5, 5, 3, 0, -5, 0)
car2 = Car(5, 5, 0, 3, 0, -5)


# Initialize array to contain car
carList = []											# initialize car array
carList.append(car1)									# place car in array
carList.append(car2)									# place car in array

for i in range(0, len(carList)):
	carList[i].displayCar()


elapsedTime = 0											# initialize time in seconds
intervalTime = 1.1
runSim = True 											# bool to stop simulation

# Begin simulation:
while(runSim):

	# Check to see if we should end simulation
	if(elapsedTime > 50):
		runSim = False									# if time condition is true runSim to false
	elapsedTime += intervalTime							# increment 100 mili second


	# FIRST check if car is in the intersection
	currIntersection.updateIntersectionQueues(carList, elapsedTime)
	# SECOND alert Calculations file cars that are in intersection
	Calculations.collisionDetection(currIntersection.queueX, currIntersection.queueY)



	for i in range(0, len(carList)):
		carList[i].displayCar()

	for i in range(0, len(carList)):
		# THIRD update position
		carList[i].updatePosition(intervalTime)
		# FOURTH print new position
		carList[i].displayPosition()
