#!/usr/bin/env python

#########################################################################
# Paul Salminen
# Program to find Z value of FITS image
# Open from project dir, will ask for image directory
# Creates linked list of each files fluxs and wavelengths
# This will export a file of all the Z values found from images
# It will then give you the option to analyze it
#########################################################################

try:
	import numpy as np
	from astropy.io import fits
except:
	print('WARNING: Required Packages found not be found.')
import os 
import sys
import warnings

warnings.filterwarnings("ignore")
sys.path.append('./bin')
sys.path.append('./docs/')

from Image_Data_Class import image
from Image_Data_Class import imageList
import Finder_Utils
from Spectral_Analysis import z_Analysis as zAnalysis

# Function to find z values of all images
def main():
	originalDir = os.getcwd()
	yn = raw_input('Do you have different files (y or n): ')
	if yn == 'y':
		os.chdir(raw_input('Enter the directory of files: '))
	else:
		os.chdir('./project_Data/')

	files = [x for x in os.listdir(os.getcwd()) if x.endswith('fits')]
	imgList = imageList()
	print('Loading image data...')
	for doc in files:
		imgList.append(doc)
	os.chdir(originalDir)

	restData =  np.genfromtxt('./docs/stationarySpectra.csv', dtype=[('elements', '|S8'), ('waveln', '>f4')], delimiter=',')
	restDict = {k:v for k,v in restData}
	restNums = [v for k,v in restData]
	restDiff = Finder_Utils.findDiffs(restNums)
	for i, x in enumerate(restNums):
		try:
			restDiff.append(restNums[i+1] - x)
		except:
			continue
	
	# This is meant to delete the files peaks that are right next to each other
	# It is used to clean up the data
	heady = imgList.head
	while heady is not None:
		heady.lamClean = Finder_Utils.cleanImg(heady.lamPeaks)
		heady = heady.next

	# Find distance between wavelengths and put it into new array
	# This information will be easier to compare 
	header = imgList.head
	while header is not None:
		header.dataDiff = Finder_Utils.findDiffs(header.lamClean)
		header = header.next
	
	# Go through all images to find z values
	print('Finding Z Values...')
	heady = imgList.head
	zData = np.zeros([(2)]) #Empty array to hold all findings, didn't use zeros to define types'
	while heady is not None:
		matches = Finder_Utils.matchSearch(restDiff, heady.dataDiff).tolist()
		heady.zValue = Finder_Utils.zCalc(matches, restNums, heady.lamClean)
		newFind = np.array([[heady.zValue, np.average(heady.flux)]])
		zData = np.asarray(np.vstack([zData, newFind]))
		heady = heady.next
	
	#Format data, save file, and exit
	zData = np.asarray(zData)
	np.savetxt('./docs/zInfo.csv', zData[1:,], header="z_Value Average_Flux")	

	#Analyze Data if wanted
	analBool = input('Would you like to analyze (y or n) ')
	if analBool[0].lower()==y:
		analBool == True
	else:
		analBool == False
	if analBool:
		fileName = input("Would you like to analyze the Z values you just found?\nIf not, enter filename and path. ")
		if fileName[0].lower() == 'y':
			spec = zAnalysis()
		else:
			spec = zAnalysis(fileName)
	else:	return
	
	keepRun = True
	while keepRun:
		n=0
		for fn in dir(spec):
			if n > 7:
				print str(n-7) + '. ' + fn
			n+=1
		choice = input('Pick your function: ') + 6

		Function_Dict = {
			7: 'spec.basicStatsCalc()', 
			8: 'spec.histogramData()',
			9: 'spec.removeOutliers()',
			10: 'spec.scatterplotData()'
		}
		
		eval(FunctionDict[choice])
		keepRun = input('Would you like to do more (True or False): ')

if __name__ == '__main__':	main()
