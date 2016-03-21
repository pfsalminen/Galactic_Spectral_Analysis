#!/usr/bin/env python

##############
# This is a module created from the ipython notebook analysis.
# This can be run separately if you do not want to create your own notebook.
# There is an option in the main program to perform these operations. 
##############

try:
	import numpy as np
	import matplotlib.pyplot as plt
	import sklearn
	import sys
except:
	print('WARNING: Error importing necessary packages')
sys.path.append('../docs/')

class z_Analysis:
	def __init__(self, filename='../docs/zInfo.csv'):
		self.Zed = np.genfromtxt(filename, delimiter=' ')
		self.Z = [x for x,y in self.Zed]
		self.Z = [y for x,y in self.Zed]
		self.Z_noOutliers = []
		self.F_noOutliers = []

	def basicStatsCalc(self, data=[]):
		# This function returns the mean, std, and median of the data it is given
		# Takes one argument: data to be analyzed.
		# Default data is stored z values
		if data == []:
			data = self.Z
		return np.mean(data), np.median(data), np.std(data)

	def scatterplotData(self,zData=[], fData=[], save=True, fName='zVsF.png'):
		# Creates a scatter plot of Z vs. F
		# Takes 4 arguments: Z value data, Flux data, save image boolean, save name
		# Default values for Z and F are from the initializer
		# Default value is to save image with name zVsF.png
		# Create data to plot
		if zData == []:
			zData = self.Z
		if fData == []:
			fData = self.F

		mu, med, sig = self.basicStatsCalc(zData)
		x = np.arange(-2, 5+max(fData), 1)
		y = np.zeros(x.shape[0])
		z = np.zeros(x.shape[0])
		y.fill(mu)
		z.fill(med)

		# Create Plot
		plt.plot(fData, zData, 'r.', label='Z Data')
		plt.plot(x, y, linewidth=1.0, label=r'$\mu= %s$' %(round(mu, 5)), color = 'b')
		plt.plot(x, z, linewidth=1.0, label=r'$Median= %s$' %(round(med, 5)), color = 'g')
		plt.legend()
		plt.xlim(-2, 350)
		plt.ylim(-.1, 0.05+np.amax(Z))
		plt.title('Redshift vs. Average Flux')

		if(save):
			plt.savefig('../docs/'+fName)
		plt.show()

	def histogramData(self, zData=[], save=True, fName='zHistogram.png'):
		# Creates a histogram of the data given to it, with option to plot it
		if zData == []:
			zData = self.Z

		n, bins, patches = plt.hist(Z, bins=50)
		mu, med, sig = self.basicStatsCalc(zData)

		plt.text(.2, 80, r'$\ \sigma=%s $' %(round(sig, 5)), fontsize=14)
		plt.text(.2, 70, r'$\mu=%s $' %(round(mu, 5)), fontsize=14)
		plt.text(.2, 60, r'$Median=%s $' %(round(med, 5)), fontsize=14)
		plt.grid(True)
		plt.legend()
		plt.ylim(0, max(n)+5)
		plt.xlim(-.1, max(bins)+0.1)
		plt.title('Redshift Occurence')
		
		if(save):
			plt.savefig('../docs/'+fName)
		plt.show()

	def removeOutliers(self, zData=[], fData=[], nSigs=3):
		# Create new info for Z and F without the outliers
		'''
		Three arguments taken:
			-Z Data, default is self
			-Fluz Data, default is self
			-Number of sigmas to keep in, default is 3
		'''
		if zData == []:
			zData = self.Z
		if fData == []:
			fData = self.F
		mu, med, sig = self.basicStatsCalc(zData)
		finds = [q for q, w in enumerate(zData) if w<mu+n*sig]
		self.Z_noOutliers = [f for j, f in enumerate(zData) if f<mu+n*sig]
		self.F_noOutliers = [j for i, j in enumerate(fData) if i in finds]

		return self.basicStatsCalc(Z_noOutliers)
