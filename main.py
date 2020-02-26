from skrebate import ReliefF
from DataCleanup import *
from eLCS import *
import time
import numpy as np
from sklearn.model_selection import cross_val_score

'''Separates out features into np_array of shape [number of items, number of features per item] 
and labels into np_array of shape [number of items]'''

converter = StringEnumerator("Datasets/Real/Multiplexer11.csv", "class")
headers, classLabel, dataFeatures, dataPhenotypes = converter.getParams()
clf = eLCS(learningIterations=5000,evalWhileFit=True,learningCheckpoints=np.array([99,999,3999]),trackingFrequency=100)

#clf.fit(dataFeatures,dataPhenotypes)

#Standard Getters
# print(clf.getMacroPopulationSize(iterationNumber=299))
# print(clf.getFinalMacroPopulationSize())
#
# print(clf.getMicroPopulationSize(iterationNumber=299))
# print(clf.getFinalMicroPopulationSize())
#
# print(clf.getPopAvgGenerality(iterationNumber=299))
# print(clf.getFinalPopAvgGenerality())
#
# print(clf.getTimeToTrain(iterationNumber=299))
# print(clf.getFinalTimeToTrain())
#
# #Eval Getters
# print(clf.getFinalAccuracy())
# print(clf.getAccuracy(iterationNumber=4999))
#
# clf.exportIterationTrackingDataToCSV()
# clf.exportRulePopulationAtIterationToCSV(4999,headerNames=headers,className=classLabel)
#clf.exportFinalRulePopulationToCSV(headers,classLabel)

#A manual shuffle is needed to perform a proper CV, because CV trains on the first 2/3 of instances, and tests on the last 1/3 of instances. While the algo will shuffle
#the 2/3 of instances, the original set needs to be shuffled as well.

formatted = np.insert(dataFeatures,dataFeatures.shape[1],dataPhenotypes,1)
np.random.shuffle(formatted)
dataFeatures = np.delete(formatted,-1,axis=1)
dataPhenotypes = formatted[:,-1]

clf = clf.fit(dataFeatures,dataPhenotypes)
print(clf.predict_proba(dataFeatures))
#
# print(clf.score(dataFeatures,dataPhenotypes))
# print(clf.timer.reportTimes())
# clf.printPopSet()

print(np.mean(cross_val_score(clf,dataFeatures,dataPhenotypes,scoring="roc_auc"))) #Example use of external scorer

#print(np.mean(cross_val_score(clf,dataFeatures,dataPhenotypes)))



