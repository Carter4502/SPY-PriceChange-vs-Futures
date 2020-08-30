import csv
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.rcParams["toolbar"] = 'None'

class SpyData:
  def __init__(self, date, spydata):
    self.date = date
    self.spydata = spydata


class FullSpyData:
	def __init__(self, date, PriceChange, FutureChange):
		self.date = date
		self.PriceChange = PriceChange
		self.FutureChange = FutureChange

changeInPrice = []
changeInFuture = []
finalList = []

with open("SPY Historical Data.csv") as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=",")
	rowCount = 0
	for row in csv_reader:
		if rowCount == 0:
			rowCount+= 1
		else:
			changeInPrice.append(SpyData(row[0], row[6]))
			rowCount+= 1
with open("US 500 Futures Historical Data.csv") as myFile:
	myFileReader = csv.reader(myFile, delimiter=",")
	rowCount = 0
	for row in myFileReader:
		if rowCount == 0:
			rowCount+= 1
		else:
			changeInFuture.append(SpyData(row[0], row[6]))
			rowCount += 1


dictionary = {}

for Futureitem in changeInFuture:
	dictionary[Futureitem.date] = {'CIF': Futureitem.spydata}

for priceChangeItem in changeInPrice:
	if (priceChangeItem.date in dictionary):
		dictionary[priceChangeItem.date].update({'CIP': priceChangeItem.spydata})


finalList = [FullSpyData(k, v.get('CIP', 0), v.get('CIF', 0)) for k, v in dictionary.items()]

listOfFutureChangesClean = []
listOfPriceChangesClean = []

for x in range(len(finalList)):
	try:
		listOfPriceChangesClean.append(float(finalList[x].PriceChange[:-1]))
		listOfFutureChangesClean.append(float(finalList[x + 1].FutureChange[:-1]))
	except Exception as e:
		break

listOfPriceChangesClean.pop()

print("Raw Data Pairs:")
for i in range(len(listOfFutureChangesClean)):
	print("(" + str(listOfFutureChangesClean[i]), str(listOfPriceChangesClean[i]) + ")")
# the list will be 1 longer then the future list because the exception isn't
# triggered until we try to append to future list

fig = plt.gcf()
fig.canvas.set_window_title("Futures vs Prices")
plt.scatter(listOfFutureChangesClean, listOfPriceChangesClean)
plt.title('Change in Future vs Change in Price S&P 500')
plt.xlabel("Previous Day Future Change %")
plt.ylabel("Price Change %")
plt.show()









