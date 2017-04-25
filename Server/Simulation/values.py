import copy
# Here we declare global values that are used throughout
# the interesection management module


# CAR VALU6
maxVelocity = 1
maxAcceleration = 1
maxDeacceleration = 0.5

# SIMULATION VALUES
timeInterval = 1
simluationTime = 3000
carGenerationModulo = 50

# INTERSECTION VALUES
intersection_length = 40
intersection_width = 40
intersection_posX = 490
intersection_posY = 490

intersection2_length = 40
intersection2_width = 40
intersection2_posX = 1020
intersection2_posY = 490

# CONVENTIONAL VALUES
conventionalSimFlag = False
conventional_stop_sign_wait = 3
conventionalStoppedX = False
conventionalStoppedY = False
proceedVert = 0

# STATISTICAL VALUES
optimized_times = []					# Container for time spent in an intersection for an optimized vehicle minus the calculation time
conventional_times = []					# Container for the time spent in an intersection for a conventional vehicle minus the calculation time

optimized_calculation_times = []		# Times a optimized vehicle runs in the intersection
conventional_calculation_times = []		# Times a conventional vehicle spends in an intersection


def deaccelerate(velocityChange):
    desiredChange = copy.copy(velocityChange)
    # print("Desired Change = " + str(desiredChange))
    deaccelerationTime = 0
    timeMili = 0.001
    while(True):
        # print("looping")
        desiredChange = desiredChange - maxDeacceleration * timeMili   # We want to reduce it by the deacceleration in miliseconds to find out precisely how long it takes to changes
        deaccelerationTime += timeMili
        if(desiredChange <= 0):
            return deaccelerationTime

    # print("Change Time = " + str(deaccelerationTime))


def accelerate(velocityChange):
    desiredChange = copy.copy(velocityChange)
    # print("Desired Change = " + str(desiredChange))
    accelerationTime = 0
    timeMili = 0.001
    while(True):
        # print("looping")
        desiredChange = desiredChange - maxAcceleration * timeMili
        accelerationTime += timeMili
        if(desiredChange <= 0):
            return accelerationTime

    # print("Change Time = " + str(accelerationTime))
