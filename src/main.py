#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Main Implementation File

Purpose: The purpose of this module is to calculate the number of 
flash events that occured along a straight line during hurricane Ana in 2021. 

The starting location is 30.30, -55.50 and the final is 30.86, -55.11.

The start time for this event is 20210520000000 YYYYMMDDHHMMSS 
and the storm was observed for 3 consecutive hours. 

Data comes from all data in 3 AWS buckets which are 
automatically generated and called by the code below. 

The buckets include:
    s3://noaa-goes16/GLM-L2-LCFA/2021/140/00/
    s3://noaa-goes16/GLM-L2-LCFA/2021/140/01/
    s3://noaa-goes16/GLM-L2-LCFA/2021/140/02/

The data for this storm event was taken from this website and represents the first
two rows: 
    
    http://ibtracs.unca.edu/index.php?name=v04r00-2021140N30305
    
Created on Wed Jul 27 20:32:58 2022

@author: coreywalker
"""

#import class driver
from class_driver import Driver

#instantiate a driver object
obj = Driver()

#calculate the distance from point 1 to point 2
obj.calculateDistance(30.30, -55.50, 30.86, -55.11)

#calculate the speed the hurricane is traveling
obj.calculateSpeedPerHour(3)

#ratio that speed for each 20 second scan interval
obj.calculate20SecondDistance()

#get the number of interpolation points based on 20 second scans
obj.getNpointsForInterpolation()

#calculate a straight line between the two points with new lat lons every 20 seconds
obj.interpolateLatLons()

#create approximate scan timestamps for each lat lon 
obj.createInterpolatedTimeStamps(2021, 5, 20, 0, 0, 0)

#create the start and stop data download strings to use on AWS CLI
obj.createDownloadStartStopString()

#create the list of buckets that AWS CLI will use to download files
obj.createDownloadList()

#download the data from AWS
obj.getGLMData() #comment this out if you alredy have the data

#create the file info dataframe to categorize downloaded data
obj.createFilesInfoDataFrame()

#merge the data downloaded with the interpolated data based on scan timestamp
obj.merge()

#go through each image and count number of lightning flashes
obj.processNetCDFs()

#create a dataframe of the flash counts by time and location from each file. 
obj.makeFlashDataFrame()

#remove the data if you do not want it anymore 
obj.removeData() #clear out the memory used for storage. Comment this out if you want to keep the data.  

#make the plot
obj.plotFlashesByTime()