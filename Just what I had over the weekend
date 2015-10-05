import json
import urllib
from datetime import date
import matplotlib.pyplot as plt

class dataTrend:

	def __init__(self, data, lowest=0, highest=0):
		self.data = data    #dictionary
		self.lowest = lowest
		self.highest = highest


lowestFile = open("lowestDifference.txt", "a")

dataCollection = {}

candList = [444, 445, 446, 448, 733, 839, 540, 717, 729, 447]
oldest = 444 #433 oldest
count = oldest
while (count <= 444):
	if count not in candList:
		continue

	myurl = urllib.urlopen("https://www.predictit.org/Home/GetChartPriceData?contractId=" + str(count) + "&timespan=90D")

	data = json.loads(myurl.read())

	#data of lowest point within 90 days 
	lowest = [99, None, 0]
	highest = [0, None, 0]
	latestDate = None
	dataPriceIndexed = []
	mA = []
	eMA = []
	emaN = 4
	mAN = 10

	for i, item in enumerate(data):
		if item['PricePerShare'] <= lowest[0]:
			lowest[0] = item['PricePerShare']
			lowest[1] = item['Date']
			lowest[2] += 1
		if item['PricePerShare'] >= highest[0]:
				highest[0] = item['PricePerShare']
				highest[1] = item['Date']
				highest[2] += 1
		if i == len(data)-1:
			latestDate = item['Date']
		dataPriceIndexed.append(item['PricePerShare'])

	for i, item in enumerate(dataPriceIndexed):
		if i >= (mAN-1):
			sum = 0.0
			for j in range(mAN):
				sum += dataPriceIndexed[i-j]
			mA.append(round(sum/mAN, 5))
		else:
			mA.append(dataPriceIndexed[i])

	eMA.append(dataPriceIndexed[0])
	k = 2.0/(emaN+1)
	for i, item in enumerate(dataPriceIndexed):
		if i != 0:
			eMA.append(round(item*k + eMA[i-1]*(1-k), 5))

	for i in range(len(mA)):
		lowestFile.write("Price: " + str(dataPriceIndexed[i]) + "   MA: " + str(mA[i]) + "   EMA: " + str(eMA[i]) +"\n")

	#if count == candList[0]:
	plt.plot(range(len(dataPriceIndexed)), dataPriceIndexed, color='r')
	plt.plot(range(len(dataPriceIndexed)), mA, color='b')
	plt.plot(range(len(dataPriceIndexed)), eMA, color='g')
	plt.title('Price = red, MA = blue, EMA = green')
	plt.show()
	#this extracts the source data into dictionary, key:date, value:price, one with len, len-10
	#dataDict = {}

	#for item in data:
	#	dataDict[item['Date']] = item['PricePerShare']

	#calculating difference between lowest and recent, and write on the file
	#if (dataDict[latestDate] != None) and (lowest[0]!= None) and (highest[0]!= None):
	#	lowestDiff = dataDict[latestDate] - lowest[0]
	#	highestDiff = highest[0] - dataDict[latestDate]

	#	recentDateArray = latestDate.split('/')
	#	lowestDateArray = lowest[1].split('/')
	#	highestDateArray = highest[1].split('/')

	
	#	recentDateObject = date(int(recentDateArray[2]), int(recentDateArray[0]), int(recentDateArray[1]))
	#	lowestDateObject = date(int(lowestDateArray[2]), int(lowestDateArray[0]), int(lowestDateArray[1]))
	#	highestDateObject = date(int(highestDateArray[2]), int(highestDateArray[0]), int(highestDateArray[1]))

	#	if ((recentDateObject - lowestDateObject).days != 0.0) and ((recentDateObject - highestDateObject).days != 0.0) and (lowestDiff != 0.0 and highestDiff!= 0.0):
	#		lowestString = "Contract#" + str(count) + "  Price between lowest and latest: " + str(lowestDiff) + ", " + str((recentDateObject - lowestDateObject).days)+ " Days ago"
	#		highestString = "              Price between highest and latest: " + str(highestDiff) + ", " + str((recentDateObject - highestDateObject).days) + " Days ago" +"\n"

	#		lowestFile.write(lowestString + highestString)


	#	elif ((latestDate == lowest[1]) and (latestDate != highest[1])) or ((latestDate != lowest[1]) and (latestDate == highest[1])):
	#		lowestString = "Contract#" + str(count) + "  Price between lowest and latest: " + str(lowestDiff) + ", " + str((recentDateObject - lowestDateObject).days) + " Days ago" 
	#		highestString = "              Price between highest and latest: " + str(highestDiff) + ", " + str((recentDateObject - highestDateObject).days) + " Days ago" +"\n"

	#		lowestFile.write(lowestString + highestString)



	#collection of a different contract/event
	#dataCollection[count] = dataTrend(dataDict, lowest, highest)


	#print(dataCollection[count].lowest)
	#print(dataCollection[count].highest)

	count += 1

lowestFile.close()

#data of lowest point within 90 days and 

#testing
#testDict = {}
#testData = data[:(len(data)-10)]

#print(dataCollection[oldest])


#print(len(data))
#print(lowest)
#print(data[len(data)-1]['PricePerShare'], data[len(data)-1]['Date'])
#print(len(testData))
#print(dataDict['07/15/2015'])


