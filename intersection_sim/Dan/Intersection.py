import Queue
from Car import Car
class Intersection:
	queueX = Queue.Queue() 							# Initialize Queue to hold incoming X cars
	queueY = Queue.Queue()							# Initialize Queue to hold incoming Y cars

	def __init__(self, lengthX, lengthY, widthX, widthY):
		self.lengthX = lengthX
		self.lengthY = lengthY
		self.widthX = widthX
		self.widthY = widthY
		
	def updateIntersectionQueues(self, carList, time):
		for i in range(0, len(carList)):
			# Check to see if car it within range of intersection to be regulated 
			if(abs(carList[i].positionX) < 5 and carList[i].velocityY == 0): 
				print("X Lane: CAR MUST BE REGULATED")
				if(carList[i].inQueue == False): 			# If the car is not already in queue
					carList[i].inQueue = True 				# Raise the car's in queue flag
					carList[i].intersectionTimeStamp = time # Stamp the arrival time
					self.queueX.put(carList[i])				# Place car in queue to be regulated 

			elif(abs(carList[i].positionY) < 5 and carList[i].velocityX == 0):
				print("Y Lane: CAR MUST BE REGULATED")
				if(carList[i].inQueue == False): 			# If the car is not already in queue
					carList[i].inQueue = True 				# Raise the car's in queue flag
					carList[i].intersectionTimeStamp = time # Stamp the arrival time
					self.queueY.put(carList[i])				# Place car in queue to be regulated