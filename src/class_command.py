#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Class Command File

Purpose:
    This class is used to generate download strings and interact with a bash shell 
    to download the NOAA, netCDFs using AWS CLI commands. 
    
Methods:
    __init__()
    printDownloadStartString()
    createDownloadStartStopString()
    createDownloadList()
    getGLMData()
    removeDat()
    
For a list of method descriptions:
    help(Command)
    
Created on Fri Jul 29 11:59:41 2022

@author: coreywalker
"""

from class_data import Data
import os

dataDir = os.getcwd() + '/data/'

class Command(Data):
    
    def __init__(self):
        """
        constructor containing class attributes

        Returns
        -------
        self. 

        """
        Data.__init__(self)
        self.lookupList = '' #a list of strings to use for data downloads from AWS CLI. 
        self.DownloadStart = '' #a string to use for AWS CLI start download
        self.DownloadEnd = '' #a string to use for AWS CLI end download
    
    def printDownloadStartStopString(self):
        """
        

        Returns
        -------
        Str.
            Prints the download start and stop string that is sent to AWS CLI. 

        """
        print('Start: ', self.DownloadStart, 'End: ', self.DownloadEnd)
        
    def createDownloadStartStopString(self):
        """

        Returns
        -------
        self.DownloadStart
            str.
                A string representing the AWS bucket containing all of the start
                hour GLM netcdfs 
        self.DownloadEnd
            str. 
                A string representing the AWS bucket containing all of the end
                hour GLM netcdfs 

        """
        #get the start and end hour from the interpolated dataframe
        start = self.interpolatedDataFrame.iloc[0]['Interpolated TimeStamps']
        end = self.interpolatedDataFrame.iloc[-1]['Interpolated TimeStamps']
        
        #set up the variables for the appropriate call format
        startt = start.timetuple().tm_yday
        endtt = end.timetuple().tm_yday
        startYear = start.year
        endYear = end.year
        bucket = 'noaa-goes16'
        product = 'GLM-L2-LCFA'
        self.hourStart = start.hour
        hourStartFormatted = '{0:02d}'.format(self.hourStart)
        self.hourEnd = end.hour 
        hourEndFormatted = '{0:02d}'.format(self.hourEnd)
        
        #generate the start and end strings for the AWS CLI call
        self.DownloadStart = 's3://{}/{}/{}/{}/{}/'.format(bucket, product, startYear, startt, hourStartFormatted)
        self.DownloadEnd = 's3://{}/{}/{}/{}/{}/'.format(bucket, product, endYear, endtt, hourEndFormatted)
    
    def createDownloadList(self):
        """
        

        Returns
        -------
        List
            Returns a list of strings representing the AWS buckets containing 
            the necessary for downloading data automatically. 

        """
        
        start = self.interpolatedDataFrame.iloc[0]['Interpolated TimeStamps']
        
        startt = start.timetuple().tm_yday
        startYear = start.year
        bucket = 'noaa-goes16'
        product = 'GLM-L2-LCFA'
        totalHours = self.hourEnd-self.hourStart+1
        hourStartObj = self.hourStart
        hourStartFormatted = '{0:02d}'.format(hourStartObj)
        
        LookupList = []
        for i in range(totalHours):
            downloadObj = 's3://{}/{}/{}/{}/{}/'.format(bucket, product, startYear, startt, hourStartFormatted)
            LookupList.append(downloadObj)
            hourStartObj += 1
            hourStartFormatted = '{0:02d}'.format(hourStartObj)
            
        self.lookupList = LookupList
        
        
    def getGLMData(self):
        """
        

        Returns
        -------
        Filled Directory
            Downloads all of the data necessary for the flash analysis based on 
            the lookup list generated by .createDownloadList()

        """
        print('Downloading all data now!')
        print('\n')
        
        for i in range(len(self.lookupList)):
            print('Downloading from:', self.lookupList[i])
            print('\n')
            
            os.system('aws s3 cp' + ' ' + self.lookupList[i] + ' ' +dataDir + ' ' + '--no-sign-request' + ' ' +'--recursive')
            
            print('\n')
            print('Done!')
            
            print('\n')
    
    def removeData(self):
        """
        

        Returns
        -------
        Empty Directory
            Removes all of the files from the datadirectory recursively.

        """
        print('Removing {} files now!'.format(len(self.filesDataFrame)))
        print('\n')
        
        for root, dirs, files in os.walk(dataDir):
            for f in files:
                file = os.path.join(dataDir, f)
                os.system('rm' + ' ' + file)
                print('removing: ' + file + '!')
                
        print('\n')
        print('All files are cleared!')