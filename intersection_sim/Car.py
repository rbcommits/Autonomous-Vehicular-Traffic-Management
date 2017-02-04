class Car:
	def __init__(self, length, width, velocityX, velocityY, startX, startY):
		self.length = length; 			# Length in meters
		self.width = width;				# Width in meters
		self.velocityX = velocityX; 	# X Velocity in meters/second
		self.velocityY = velocityY;		# Y Velocity in meters/second
		self.accelerationX = 0			# X Acceleration in meters/(second per second)
		self.accelerationY = 0			# Y Acceleration in meters/(second per second)
		self.positionX = startX			# X start coordinate
		self.positionY = startY			# Y start coordinate

	# Print all details of car instance 
	def displayCar(self):
		print "Length: ", self.length
		print "Width: ", self.width
		print "X Position: ", self.positionX
		print "Y Position: ", self.positionY
		print "X Velocity: ", self.velocityX
		print "Y Velocity: ", self.velocityY
		print "X Acceleration: ", self.accelerationX
		print "Y Acceleration: ", self.accelerationY

	def displayPosition(self):
		print "(", self.positionX, ", ", self.positionY, ")"

	# Calculate acceleartion
	def calculateAcceleration(self, newVelocityX, newVelocityY):
		self.accelerationX = newVelocityX - self.velocityX
		self.accelerationY = newVelocityY - self.velocityY

