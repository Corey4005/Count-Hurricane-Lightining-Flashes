#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Driver File

Purpose: This is a driver class to help python understand the difference
between class_interpolate and class_command, given they both inherit from 
class_data and manipulate attributes across classes. The driver object 
will be able to see the memory inherited across classes so that the diaomond 
inheritance problem does not occur. 

This class merges the interpolated dataframe with the filesdatframe and uses 
the merged data to process all of the netcdfs into a dictionary structure. From 
the dictonary, a flashcount dataframe can be generated and plotted. 

Methods:
    __init__()
    merge()
    processNetCDFs()
    makeFlashDataFrame()
    plotFlashesByTime()
    
For a list of method descriptions:
    help(Driver)
    
@author: coreywalker
"""

from class_interpolate import interpolate
from class_command import Command 
import pandas as pd
import netCDF4 as nc
import matplotlib.pyplot as plt


class Driver(interpolate, Command):
    def __init__(self):
        """
        constructor for class attributes.

        Returns
        -------
        Self.

        """
        interpolate.__init__(self)
        Command.__init__(self)
        self.mergedDataFrame = ''#a dataframe that is the result of merging self.interpolatedDataFrame and self.filesDataFrame. Default is empty. 
        self.dataDictionary = ''#a dictionary to store data returned from each processed netcdf file.
        self.processedDataFrame = pd.DataFrame() #a dataframe containing concatinated data for plotting.
        
    def merge(self):
        """
    
        Returns
        -------
        Pandas DataFrame
            Returns a dataframe containing the merged self.interpolatedDataFrame and self.dataInfoDataFrame

        """
        filesDataFrame = self.filesDataFrame
        interpolatedDataFrame = self.interpolatedDataFrame
        self.mergedDataFrame = pd.merge(filesDataFrame, interpolatedDataFrame, left_on='File Scan Begin Time', right_on='Interpolated TimeStamps', how='left')
        self.mergedDataFrame.dropna(inplace=True)
        
    def processNetCDFs(self):
        """
        

        Returns
        -------
        Dictionary
            returns a dictionary of all processed netcdfs with flashcount at lat and lon
            by time. The box size for a valid flash count is 111km by 111km or 1 degree up, down, left and 
            right from each lat lon location. 

        """
        
        print('Processing {} netCDF files now!'.format(len(self.filesDataFrame)))
        print('\n')
        
        df = self.mergedDataFrame
        
        flashDic = {}
        fileCount = 0
        fileLength = str(len(self.filesDataFrame))
        for i, row in df.iterrows():
            totalflashCount = 0
            fileName = row['File Name']
            time = row['File Scan Begin Time']
            fileCount += 1
            print("Images Processed: ", str(fileCount) + '/' + fileLength)
            ds = nc.Dataset(fileName)
            lat = row['Interpolated Lats']
            lon = row['Interpolated Lons']
            hugeLatBounds = [lat-1, lat+1]
            hugeLonBounds = [lon-1, lon+1]
            flash_lats = ds.variables['flash_lat']
            flash_lons = ds.variables['flash_lon']
            
            
            #count the flashes in the bounds
            for i in flash_lats[:]:
                for j in flash_lons[:]:
                    if i>=hugeLatBounds[0] and i<=hugeLatBounds[1] and j>=hugeLonBounds[0] and j<=hugeLonBounds[1]:
                        totalflashCount += 1
                        
            flashDic[time] = (lat, lon, totalflashCount)
            
        self.dataDictionary = flashDic
        
    def makeFlashDataFrame(self):
        """
        

        Returns
        -------
        A dataframe of concatinated self.dataDictionary items to be used for plotting
        the flash events by time. 

        """
        
        flashList = []
        timeList = []
        latList = []
        lonList = []
        
        for i in self.dataDictionary:
            time = i
            timeList.append(time)
            lat = self.dataDictionary.get(i)[0]
            latList.append(lat)
            lon = self.dataDictionary.get(i)[1]
            lonList.append(lon)
            flashes = self.dataDictionary.get(i)[2]
            flashList.append(flashes)
        
        self.processedDataFrame['Time of Scan'] = timeList
        self.processedDataFrame['Flash Count'] = flashList
        self.processedDataFrame['Latitude'] = latList
        self.processedDataFrame['Longitude'] = lonList
        
        
    def plotFlashesByTime(self):
        """
        

        Returns
        -------
        Matplotlib Plot
            Plot of flash events by time for the straight line event. 

        """
        print('Plotting the data for the storm!')
        print('\n')
        
        self.processedDataFrame.set_index('Time of Scan', inplace=True)
        plt.plot(self.processedDataFrame['Flash Count'])
        plt.title('Flash Count over Time')
        plt.xlabel('Time')
        plt.ylabel('Flash Count')
        plt.savefig('./plots/flashcounts.png')
        
        print('Plot saved to ./plots/flashcounts.png')
        