#######################################################################
#Paul Salminen
#ASTR3800
#exportZfile.py
#Program to find Z value of FITS image
#Open from project dir, will ask for image directory
#Creates linked list of each files fluxs and wavelengths
#This will export a file of all the Z values found from images
#Along with their avererage flux
#######################################################################

import numpy as np
from astropy.io import fits
from os import listdir
from os import chdir
from os import getcwd

#######################################################################
#This is the Definition of the image class, which each holds 
#information about a single image, along with information leading
#to the next image. It was very good for holding a lot of 
#information about a lot of similar items
#######################################################################

class image(object):
	def __init__(self, filename, next):
		self.flux = fits.open(filename)[1].data.flux	#All flux list
		self.lams = 10**(fits.open(filename)[1].data.loglam)	#List of all wavelengths
		self.lamPeaksHi = self.lams[np.where(self.flux>=(np.mean(self.flux) + 2*np.std(self.flux)))]	#Emission and absorption
		self.lamPeaksLo = self.lams[np.where(self.flux<=(np.mean(self.flux) - 2*np.std(self.flux)))]
		self.lamPeaks = self.lamPeaksHi.tolist() + self.lamPeaksLo.tolist()	#Combine lists
		self.lamPeaks.sort()	#Put combined list in order
		self.lamClean = []	#Used later to furfer clean lamPeaks
		self.dataDiff = [0]	#Empty list to hold differences of important wavelengths, used later
		self.zValue = 0		#To be found an updated later
		self.next = next	#Pointer to next file info

########################################################################
#Class to connect all image data together, making going through them 
#all a whole lot easier. This may not be a very pythonic mentality,
#but I found this to be extremely helpful
#######################################################################

class imageList(object):
	head = None	#To have/use as a linked list
	tail = None

	#Add new node(image) to linked list
	def append(self, filename):
		newNode = image(filename, None)	#Create new image instance
		if self.head is None:	#If its the first image, make it so
			self.head = self.tail = newNode
		else:	#Otherwise just add it to the list
			self.tail.next = newNode
			self.tail = newNode


#####################################################################
#This begins the beginning of individual functions to call from 
#main. This turned out to be faster, and cleaner looking
#in my opinion
#####################################################################

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

#Main function to find z values of all images
def main():
	#Get the location of files from user and go to it
	originalDir = getcwd()	#Save current director for later
	yn = raw_input('Do you have different files (y or n): ')
	if yn == 'y':
		chdir(raw_input('Enter the directory of files: '))
	else:
		chdir('projData')

	#Get all desired file names to look at, then created new list
	#Finally, go through all files and add their info to list
	#Essentially, initializing the imageList class
	files = [x for x in listdir(getcwd()) if x.endswith('fits')]	#create array of all FITS files
	imgList = imageList()	#Create instance of class/linked list
	print('Loading image data...')	#update print
	for doc in files:	#Go through all files to create linked list of fluxs and wavelengths
		imgList.append(doc)
	chdir(originalDir)	#Change back to main project dir

	#This imports a csv file of the major spectroscopic lines when at rest
	#It is compared to the files info later to find Z 
	restData =  np.genfromtxt('stationarySpectra.csv', dtype=[('elements', '|S8'), ('waveln', '>f4')], delimiter=',')
	restDict = {k:v for k,v in restData} #Dictionary of elements
	restNums = [y for x,y in restData]	#Array of rest wavelengths
	restDiff = findDiffs(restNums)	#Find difference between wavelengths
	for i, x in enumerate(restNums):
		try:	#Used for i+1 on last iteration
			restDiff.append(restNums[i+1] - x)
		except:
			continue
	
	#This is meant to delete the files peaks that are right next to each other
	#It is used to clean up the data
	heady = imgList.head
	while heady is not None:
		heady.lamClean = cleanImg(heady.lamPeaks)
		heady = heady.next

	#Find distance between wavelengths and put it into new array
	#This information will be easier to compare 
	header = imgList.head
	while header is not None:
		header.dataDiff = findDiffs(header.lamClean)
		header = header.next
	
	#Go through all images to find z values
	print('Finding Z Values...')
	heady = imgList.head
	zData = np.zeros([(2)]) #Empty array to hold all findings, didn't use zeros to define types'
	while heady is not None:
		matches = matchSearch(restDiff, heady.dataDiff).tolist()
		heady.zValue = zCalc(matches, restNums, heady.lamClean)
		newFind = np.array([[heady.zValue, np.average(heady.flux)]])
		zData = np.asarray(np.vstack([zData, newFind]))
		heady = heady.next
	
	#Format data, save file, and exit
	zData = np.asarray(zData)
	np.savetxt('zInfo.csv', zData[1:,], header="z_Value Average_Flux")
	print('\tComplete\nGoodbye')
main()
