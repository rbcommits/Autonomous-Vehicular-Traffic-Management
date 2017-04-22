from gui import carGUI
# Here we declare global values that are used throughout
# the interesection management module

# Global carList container
global carList
carList = []


# CAR VALUES
maxVelocity = 1

# SIMULATION VALUES
timeInterval = 1
simluationTime = 10000000
carGenerationModulo = 50

# INTERSECTION VALUES
intersection_length = 40
intersection_width = 40
intersection_posX = 490
intersection_posY = 490


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

def init(root):
	global gui
	gui = carGUI(root)