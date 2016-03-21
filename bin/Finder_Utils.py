#!/usr/bin/env python

#####################
# Paul Salminen
# This is a module that contains
# all of the functions written to 
# find the z-value of the galaxy image
#####################

try:
	import numpy as np
except:
	print('WARNING: Could not load necessary packages')

#Cleans the lamPeaks of all image nodes
def cleanImg(lamPeaks):
	nums = []
	for i, x in enumerate(lamPeaks):
		try:	#Used for last iteration
			if abs(lamPeaks[i+1] - x) < 3:
				nums.append(x)
		except:
			continue
	lamClean = [x for x in lamPeaks if x not in nums]
	return lamClean

#Function to find the difference betweein important wvlns
def findDiffs(lambs):
	diffs = [0]
	for i, x in enumerate(lambs):	#Goes through whole list
		try:	#Used for last iteration
			diffs.append(lambs[i+1] - x)
		except:
			continue
	return diffs

#Finds matching wavelength differences, thus wavelengh
def matchSearch(rest, data):
	foundInfo = np.zeros([2]).astype(int)
	for i in range(len(rest)):
		for n in range(i):
			numTest = np.cumsum(rest[n:i+1])
			for j in range(i-n+1):	#Size of arrays created
				for k in range(len(data)):	#Go through data array
					if data[k] == numTest[j]:
							foundInfo =np.vstack([foundInfo, np.array([[n+j, k]])]).astype(int)
	return foundInfo[1:,].astype(int)

#Finds z value from matches
def zCalc(matches, rest, data):
	zAll = []
	for x,y in matches:
		try:
			zAll.append(abs((data[y]-rest[x]) / rest[x]))
		except:
			continue
	return np.average(zAll).astype(np.float64)

if __name__ == '__main__': main()
