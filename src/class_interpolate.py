#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Interpolate File

Purpose: This class is used to interpolate the points between two latitude and longitude 
locations and create the start and stop download strings for AWS CLI based on the input
data. 

Methods:
    
    __init__()
    printDistance()
    printSpeed()
    print20SecondDistance()
    printDownloadStartStopString()
    calculateDistance()
    calculateSpeedPerHour()
    calculate20SecondDistance()
    getNpointsForInterpolation()
    interpolateLatLons()
    createInterpolatedTimeStamps()
    createDownloadStartStopString()
    createDownloadList()
    plotInterpolation()
    
For a list of method descriptions:
    help(interpolate)

Created on Thu Jul 28 12:06:13 2022

@author: coreywalker
"""

from geopy.distance import geodesic
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from class_data import Data
import pandas as pd

class interpolate(Data):
    
    def __init__(self):
        """
        constructor containing attributes for the class. 

        Returns
        -------
        Self.

        """
        #get the data dataframe
        Data.__init__(self)
        self.distanceBetweenPoints = 0 #the distance between lat1,lo1, lat2, lon2. Default is 0. 
        self.lat1 = 0 #the latitude of point 1
        self.lon1 = 0 #the longitude of point 1
        self.lat2 = 0 #the latitude of point 2
        self.lon2 = 0 #the longitude of point 2
        self.speed = 0 #speed of storm between point 1, and 2 calculated in km/h
        self.distanceIn20seconds = 0 #distance the storm is assumed to travel in 20 seconds 
        self.nPoints = 0 #the number of interpolated points needed between point 1, and point 2
        self.newLats = 0 #new, interpolated latitudes between point 1 and point 2
        self.newLons = 0 #new, interpolated longitudes between point 2 adn point 2
        self.interpolatedDataFrame = pd.DataFrame() #dataframe containing interpolation metadata. Default is empty. 
       
        
    
    def printDistance(self):
        """ 

        Returns
        -------
        Str. 
            Returns a string describing the distance between point 1 and point 2. 

        """
        if self.distanceBetweenPoints ==0:
            print('No Distance has been calculated! Use the .calculateDistance method first!')
        else:
            print('Distance is:', self.distance, 'Km between ({},{}) and ({}, {})'.format(self.lat1, self.lon1, self.lat2, self.lon2))
            
    def printSpeed(self):
        """

        Returns
        -------
        Str. 
            returns a string containing the assumed speed of the storm over a straight, interpolated line. 

        """
        if self.speed == 0:
            print('No Speed has been calculated! Use the .calculateSpeed() method and pass the number of hours to point 2.')
        else:
            print('The speed for the storm event was {} km / h'.format(self.speed))
    
    def print20SecondDistance(self):
        """
    
        Returns
        -------
        Str.
            Prints the assumed distance traveled by the storm in 20 seconds. 

        """
        if self.distanceIn20Seconds== 0:
            print('No Speed has been calculated! Use the .calculate20SecondDistance() method and pass the number of hours to point 2.')
        else:
            print('The distance traveled in 20 seconds was {} km'.format(self.distanceIn20Seconds))
            
            
    def calculateDistance(self, lat1, lon1, lat2, lon2):
        """
        

        Parameters
        ----------
        lat1 : Int
            Latitude of point 1
        lon1 : Int
            Longitude of point 1
        lat2 : Int
            Latitude of point 2
        lon2 : Int
            Longitude of point 2

        Returns
        -------
        Float
            The distance between point 1 and point 2 in km. 

        """
        #grab the positions
        position1 = (lat1, lon1)
        position2 = (lat2, lon2)
        
        #set the lats and lons 
        self.lat1 = lat1
        self.lon1 = lon1
        self.lat2 = lat2
        self.lon2 = lon2
        
        #calculate the distance
        self.distanceBetweenPoints = (geodesic(position1, position2).km)
        
        
    def calculateSpeedPerHour(self, hoursToPoint2):
        """
        

        Parameters
        ----------
        hoursToPoint2 : Int
            The number of hours it takes for the storm to travel from point 1
            to point 2. 

        Returns
        -------
        Int
            Returns the speed per hour of the storm assuming it travels in a straight line
            from point 1 to point 2 over the observed time period.

        """
        
        self.speed = self.distanceBetweenPoints / hoursToPoint2
        
        
    def calculate20SecondDistance(self):
        """
        

        Returns
        -------
        The assumed distance the storm travels in 20 seconds. 

        """
        if self.speed ==0:
            print('Calculate the speed of the storm per hour first using .calculateSpeedPerHour()!')
        #Equation: speed * 20s / 3600s in one hour
        else:
            self.distanceIn20Seconds = (self.speed*20) / 3600
            
    def getNpointsForInterpolation(self):
        """
        

        Returns
        -------
        The number of interpolation points needed given the distance between the two
        points and the 20 second distance the storm travels. 

        """
        self.nPoints = self.distanceBetweenPoints / self.distanceIn20Seconds
        
    def interpolateLatLons(self):
        """
        

        Returns
        -------
        A list of interpolated lats and lons based on the calcuated nPoints 
        and stores these in the interpolation dataFrame. 

        """
        self.newLats = np.linspace(self.lat1, self.lat2, int(self.nPoints))
        self.newLons = np.linspace(self.lon1, self.lon2, int(self.nPoints))
        self.interpolatedDataFrame['Interpolated Lats'] = self.newLats
        self.interpolatedDataFrame['Interpolated Lons'] = self.newLons
    
    def createInterpolatedTimeStamps(self, startYear, startMonth, startDay, startHour, startMin, startSec):
        """
        

        Parameters
        ----------
        startYear : Int
            four digit year - ex:
                2021
        startMonth : Int
            one digit month - ex:
                5 = May
            or two digit month - ex:
                11 = November
        startDay : Int
            one digit day - ex:
                5 = 5th day of the startMonth
            or two digit day - ex:
                20 = 20th day of the startMonth
            Do not pass anything over 31
        startHour : Int
            24 hour digit - ex:
                13 = 1 o'clock
            If digit is less than 10, pass a single digit - ex:
                9 = 9 o'clock
        startMin : Int
            if startMin is less than 10, pass a one digit time - ex:
                5 = 5 minutes passed the startHour.
            else:
                25 = 25 minutes passed the startHour. 
        startSec : Int
            if startSec is less than 10, pass a one digit time - ex:
                4 = 4 seconds passed the startMin
            else:
                40 = 40 seconds passed the startMin
            

        Returns
        -------
        A list of interpolated timestamps corresponding to the assumed location 
        of the storm (lat, lon), based on the number of calculated nPoints from 
        point 1 to point 2. 

        """
        beginMilisec = 00
        startDate = datetime(startYear, startMonth, startDay, startHour, startMin, startSec, beginMilisec)
        
        timeDelta = timedelta(seconds=20)
       
        timeStampList = []
        
        for i in range(int(self.nPoints)):
            timeStampList.append(startDate)
            startDate += timeDelta
            
            
        self.interpolatedDataFrame['Interpolated TimeStamps'] = timeStampList
    
        
    def plotInterpolation(self):
        """
        

        Returns
        -------
        A straight line plot of the interpolated lat lons of point one to point two. 

        """
        
        GLMLONS = self.newLons
        GLMLATS = self.newLats
        for i in range(len(GLMLONS)):
            plt.scatter(GLMLONS[i], GLMLATS[i])
        
        plt.xlabel('Longitude')
        plt.ylabel('Latitude')
        plt.title(str(int(self.nPoints)) + ' ' + 'Interpolated Points between' + ' ' + str(self.lat1) + ',' + str(self.lon1) + ' ' + 'and' + ' ' + str(self.lat2) + ',' + str(self.lon2))
        plt.savefig('./plots/lineInterpolation.png')
        
        print('Plot saved to ./plots/lineInterpolation.png')
        print('\n')
        
    
        
        