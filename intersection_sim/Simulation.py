import Calculations
import Queue
from Car import Car
from Intersection import Intersection


# Initialize instance of intersection
currIntersection = Intersection(100, 100, 10, 10)


# Declare cars:
# (self, length, width, velocityX, velocityY, startX, startY)
car1 = Car(5, 5, 3, 0, -5, 0)
car2 = Car(5, 5, 0, 3, 0, -5)

# Initialize Queue to hold incoming X cars
queueX = Queue.Queue() 
queueY = Queue.Queue()

# Initialize array to contain car
carList = []											# initialize car array
carList.append(car1)									# place car in array
carList.append(car2)									# place car in array

for i in range(len(carList)):
	carList[i].displayCar() 




elapsedTime = 0											# initialize time in seconds
runSim = True 											# bool to stop simulation

# Begin simulation:
while(runSim):

	# Check to see if we should end simulation
	if(elapsedTime > 50):
		runSim = False									# if time condition is true runSim to false
	elapsedTime += 0.1									# increment 100 mili second


	for i in range(len(carList)):
		# Check to see if car it within range of intersection to be regulated 
		if(abs(carList[i].positionX) < 5 and carList[i].velocityY == 0): 
			print("X Lane: CAR MUST BE REGULATED")
			if(carList[i].inQueue == False): 			# If the car is not already in queue
				carList[i].inQueue = True 				# Raise the car's in queue flag
				queueX.put(carList[i])					# Place car in queue to be regulated 

		elif(abs(carList[i].positionY) < 5 and carList[i].velocityX == 0):
			print("Y Lane: CAR MUST BE REGULATED")
			if(carList[i].inQueue == False): 			# If the car is not already in queue
				carList[i].inQueue = True 				# Raise the car's in queue flag
				queueY.put(carList[i])					# Place car in queue to be regulated


		# Print old position 
		#carList[i].displayPosition()
		# Now update position
		carList[i].positionX = carList[i].positionX + carList[i].velocityX*0.1
		carList[i].positionY = carList[i].positionY + carList[i].velocityY*0.1
		# Print new position
		carList[i].displayPosition()



