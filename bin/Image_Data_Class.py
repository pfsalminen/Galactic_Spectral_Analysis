#!/usr/bin/env python

#####################
# Paul Salminen
# This is the Definition of the image class, which each holds 
# information about a single image, along with information leading
# to the next image. It was very good for holding a lot of 
# information about a lot of similar items
#####################

try:
	import numpy as np
	from astropy.io import fits
except:
	print('WARNING: Could not load necessary packages')
import os
import sys

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

