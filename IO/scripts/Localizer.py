#! /usr/bin/env python


"""
Things to do:
    -> Get Localizer data from Raspberry
    -> Convert data into appropriate Ros msg
    -> Publish to ROS Topic
"""

import rospy
from sensor_msgs.msg import _NavSatFix


NAME = "Localizer"
TOPIC = "CurrentLocation"

class GPS_Data():
    longitude = 0.0
    latitude = 0.0
    altitude = 0.0
    def __init__(self, latitude, longitude, altitude):
        self.longitude = longitude
        self.latitude = latitude
        self.altitude = altitude
def getGPS():
    # Get GPS data and send it back as a ROS msg
    GPS_Data = _NavSatFix()
    GPS_Data.longitude = 0.0
    GPS_Data.latitude = 0.0
    GPS_Data.altitude = 0.0
    return GPS_Data
def DetermineLocation(GPS, IMU, Proximity, ):
    # Fancy Algorithm that determines location using GPS and self corrects it using IMU and Proximity Sensors,
    # computes a final and accurate location of the car and sends it
    FinalLocation = GPS #For now
    return FinalLocation

def main():


