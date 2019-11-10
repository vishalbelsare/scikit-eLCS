'''
Name: eLCS.py
Authors: Robert Zhang in association with Ryan Urbanowicz
Contact: robertzh@wharton.upenn.edu
Description: This module creates a class that takes in data, and cleans it up to be used by another machine learning module
'''

import numpy as np
import pandas as pd

class StringEnumerator:
    def __init__(self, inputFile, classLabel):
        self.classLabel = classLabel
        self.map = {} #Dictionary of header names: Attribute dictionaries
        data = pd.read_csv(inputFile, sep=',')  # Puts data from csv into indexable np arrays
        data = data.fillna("NA")
        self.dataFeatures = data.drop(classLabel, axis=1).values
        self.dataPhenotypes = data[classLabel].values
        self.dataHeaders = data.drop(classLabel, axis=1).columns.values
        self.deleteAllInstancesWithoutPhenotype()

    def changeClassName(self,newName):
        self.map[self.newName] = self.map.pop(self.classLabel)
        self.classLabel = newName

    def changeHeaderName(self,currentName,newName):
        if (currentName in self.dataHeaders):
            headerIndex = np.where(self.dataHeaders == currentName)[0][0]
            self.dataHeaders[headerIndex] = newName
            if currentName in self.map.keys():
                self.map[newName] = self.map.pop(currentName)

    def addAttributeConverter(self,headerName,array):#map is an array of strings, ordered by how it is to be enumerated enumeration
        newAttributeConverter = {}
        for index in range(len(array)):
            newAttributeConverter[array[index]] = index
        self.map[headerName] = newAttributeConverter

    def addAttributeConverterRandom(self,headerName):
        headerIndex = np.where(self.dataHeaders == headerName)[0][0]
        uniqueItems = np.array([])
        for instance in self.dataFeatures:
            if not(instance[headerIndex] in uniqueItems):
                uniqueItems = np.append(uniqueItems,instance[headerIndex])
        self.addAttributeConverter(headerName,uniqueItems)

    def addClassConverter(self,array):#assumes no other
        newAttributeConverter = {}
        for index in range(len(array)):
            newAttributeConverter[array[index]] = index
        self.map[self.classLabel] = newAttributeConverter

    def convertAllAttributes(self):
        for attribute in self.dataHeaders:
            if attribute in self.map.keys():
                i = np.where(self.dataHeaders == attribute)[0][0]
                for state in self.dataFeatures:#goes through each instance's state
                    if (state[i] in self.map[attribute].keys()):
                        state[i] = self.map[attribute][state[i]]

        if self.classLabel in self.map.keys():
            for state in self.dataPhenotypes:
                if (state in self.map[self.classLabel].keys()):
                    i = np.where(self.dataPhenotypes == state)
                    self.dataPhenotypes[i] = self.map[self.classLabel][state]

    def deleteAttribute(self,headerName):
        i = np.where(headerName == self.dataHeaders)[0][0]
        newFeatures = np.array([[2,3]])
        self.dataHeaders = np.delete(self.dataHeaders,i)

        for instanceIndex in range(len(self.dataFeatures)):
            instance = np.delete(self.dataFeatures[instanceIndex],i)
            if (instanceIndex == 0):
                newFeatures = np.array([instance])
            else:
                newFeatures = np.concatenate((newFeatures,[instance]),axis=0)
        self.dataFeatures = newFeatures

    def deleteAllInstancesWithoutHeaderData(self,headerName):
        newFeatures = np.array([[2,3]])
        newPhenotypes = np.array([])
        attributeIndex = np.where(self.dataHeaders == headerName)[0][0]

        firstTime = True
        for instanceIndex in range(len(self.dataFeatures)):
            instance = self.dataFeatures[instanceIndex]
            if instance[attributeIndex] != "NA":
                if firstTime:
                    firstTime = False
                    newFeatures = np.array([instance])
                else:
                    newFeatures = np.concatenate((newFeatures,[instance]),axis = 0)
                newPhenotypes = np.append(newPhenotypes,self.dataPhenotypes[instanceIndex])

        self.dataFeatures = newFeatures
        self.dataPhenotypes = newPhenotypes

    def deleteAllInstancesWithoutPhenotype(self):
        newFeatures = np.array([[2,3]])
        newPhenotypes = np.array([])
        firstTime = True
        for instanceIndex in range(len(self.dataFeatures)):
            instance = self.dataPhenotypes[instanceIndex]
            if instance != "NA":
                if firstTime:
                    firstTime = False
                    newFeatures = np.array([self.dataFeatures[instanceIndex]])
                else:
                    newFeatures = np.concatenate((newFeatures,[self.dataFeatures[instanceIndex]]),axis = 0)
                newPhenotypes = np.append(newPhenotypes,instance)

        self.dataFeatures = newFeatures
        self.dataPhenotypes = newPhenotypes

    def print(self):
        isFullNumber = self.checkIsFullNumeric()
        print("Converted Data Features and Phenotypes")
        for header in self.dataHeaders:
            print(header,end="\t")
        print()
        for instanceIndex in range(len(self.dataFeatures)):
            for attribute in self.dataFeatures[instanceIndex]:
                if attribute != "NA":
                    if (isFullNumber):
                        print(float(attribute), end="\t")
                    else:
                        print(attribute, end="\t\t")
                else:
                    print("NA", end = "\t")
            if (self.dataPhenotypes[instanceIndex] != "NA"):
                if (isFullNumber):
                    print(float(self.dataPhenotypes[instanceIndex]))
                else:
                    print(self.dataPhenotypes[instanceIndex])
            else:
                print("NA")
        print()

    def printAttributeConversions(self):
        print("Changed Attribute Conversions")
        for headerName,conversions in self.map:
            print(headerName + " conversions:")
            for original,numberVal in conversions:
                print("\tOriginal: "+original+" Converted: "+numberVal)
            print()
        print()

    def checkIsFullNumeric(self):
        try:
            for instance in self.dataFeatures:
                for value in instance:
                    if value != "NA":
                        float(value)
            for value in self.dataPhenotypes:
                if value != "NA":
                    float(value)

        except:
            return False

        return True

    def getParams(self):
        if not(self.checkIsFullNumeric()):
            print("Data set must be fully numeric")
            return

        newFeatures = np.array([])
        newPhenotypes = np.array([])
        for instanceIndex in range(len(self.dataFeatures)):
            newInstance = np.array([])
            for attribute in self.dataFeatures[instanceIndex]:
                if attribute == "NA":
                    newInstance = np.append(newInstance, np.nan)
                else:
                    newInstance = np.append(newInstance,float(attribute))
            newFeatures = np.append(newFeatures,newInstance)

            if self.dataPhenotypes[instanceIndex] == "NA":
                newPhenotypes = np.append(newPhenotypes, np.nan)
            else:
                newPhenotypes = np.append(newPhenotypes,float(self.dataPhenotypes[instanceIndex]))



        return self.dataHeaders,self.classLabel,self.dataFeatures,self.dataPhenotypes