#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Data File

Purpose: This class is used to observe the data downloaded from AWS CLI. 

Methods: 
    
    __init__ 
    printDataFilePath() 
    printFilesDataFrame() 
    printNumberFiles() 
    createFilesInfoDataFrame() 
    
For a list of method descriptions:
    help(Data)

Created on Wed Jul 27 14:30:17 2022

@author: coreywalker
"""

import os 
import pandas as pd
from datetime import datetime


class Data():
    
    def __init__(self):
        """
        Constructor containing attributes for the class. 

        Returns
        -------
        Self.

        """
        self.filepath = os.getcwd() + "/data/" #a filepath to the data directory containing downloaded files from AWS. 
        self.filesDataFrame = pd.DataFrame() #a dataframe that will contain file metadata.
        self.hourStart = 0 #a number representing the hour the storm was at location one. 
        self.hourEnd = 0 #a number representing the hour the storm was at location two. 
        
    def printDataFilePath(self):
        """

        Returns
        -------
        Str
            Returns a string representing the data directory.

        """
        return self.filepath 
    
    def printFilesDataFrame(self):
        """
        
        Returns
        -------
        Pandas DataFrame
            The dataframe containing the files metadata. The 
            self.filesDataFrame object is empty until filled. 

        """
        print(self.filesDataFrame) #prints the dataframe
    
    def printNumberFiles(self):
        """
        
        Returns
        -------
        str
            prints a string representing the length of the data directory. 

        """
        
        ##print number of files in folder
        for root, dirs, files in os.walk(self.filepath):
            print("The number of file(s) that were downloaded to the data folder are: ", len(files))
            print('\n')
            
    
    def createFilesInfoDataFrame(self):
        """

        Returns
        -------
        Pandas DataFrame 
            Creates a DataFrame of the files metadata that is downloaded from AWS CLI
            containing the file name, file creation time, begin time of sattelite scan, end time of
            sattelite scan and the scan time delta. 

        """
        fileList = [] #list to save the filenames
        creationList = [] #list to store the file creation times. 
        scanEndList = [] #list to store the scan end times. 
        scanBeginList = [] #list to store the scan begin times. 
        
        ##get the file info
        for root, dirs, files in os.walk(self.filepath):
            for f in files:
                if f == '.DS_Store':
                    pass
                else:
                #filepath
                    fileName = os.path.join(self.filepath, f)
                    fileList.append(fileName)
                
                #get the file creation time
                    fileCreationTime = f[-17:-3]
                    dateTimeCreate = datetime.strptime(fileCreationTime, '%Y%j%H%M%S%f')
                    creationList.append(dateTimeCreate)
                
                #get the scan time 
                    scanTime = f[-49:-35]
                    dateTimeScan = datetime.strptime(scanTime, '%Y%j%H%M%S%f')
                    scanBeginList.append(dateTimeScan)
                
                #get the scan end time
                    endTime = f[-33:-19]
                    dateTimeEnd = datetime.strptime(endTime, '%Y%j%H%M%S%f')
                    scanEndList.append(dateTimeEnd)
        
        #create the dataframe containing the apropriate columns
        self.filesDataFrame['File Name'] = fileList
        self.filesDataFrame['File Creation Time'] = creationList
        self.filesDataFrame['File Scan Begin Time'] = scanBeginList
        self.filesDataFrame['File Scan End Time'] = scanEndList
        self.filesDataFrame['Scan Time Delta'] = self.filesDataFrame['File Scan End Time'] - self.filesDataFrame['File Scan Begin Time']
        self.filesDataFrame = self.filesDataFrame.sort_values(by='File Scan Begin Time')
            
    
        
    