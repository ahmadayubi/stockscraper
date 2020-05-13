import numpy as np
import csv
from matplotlib import pyplot as plt
from matplotlib.widgets import CheckButtons
from datetime import datetime

# convert to number from numerized string


def convertToNum(sNum):
    if sNum[-1] == 'k':
        return float(sNum[:-1]) * 1000
    elif sNum[-1] == 'm':
        return float(sNum[:-1]) * 1000000
    else:
        return float(sNum)

# views data


def viewTicker(ticker):
    time_format = '%Y-%m-%d %H:%M:%S.%f'
    headers = ['date', 'ticker', 'watchers', 'price',
               'pricechange', 'msgvol', 'sentiment', 'vol']
    data = np.genfromtxt('data/'+ticker+'.csv', delimiter=',',
                         skip_header=1, dtype=None, names=headers, encoding=None)
    time = [datetime.strptime(i, time_format)for i in data['date']]
    vol = [convertToNum(i) for i in data['vol']]

    print("Choices:")
    print("1 Watchers")
    print("2 Price")
    print("3 Price Change")
    print("4 Message Volume Change")
    print("5 Sentiment Change")
    print("6 Volume")
    print("9 Show Graphs")
    print("0 End")
    while True:
        choice = int(input("Enter Choice:"))
        if choice == 1:
            plt.figure("Watchers")
            plt.plot(time, data['watchers'], label="Watchers")
            plt.legend()
        elif choice == 2:
            plt.figure("Price")
            plt.plot(time, data['price'], label="Price")
            plt.legend()
        elif choice == 3:
            plt.figure("Price Change")
            plt.plot(time, data['pricechange'], label="Price Change")
            plt.legend()
        elif choice == 4:
            plt.figure("Message Volume Change")
            plt.plot(time, data['msgvol'], label="Message Volume Change")
            plt.legend()
        elif choice == 5:
            plt.figure("Sentiment Change")
            plt.plot(time, data['sentiment'], label="Sentiment Change")
            plt.legend()
        elif choice == 6:
            plt.figure("Volume")
            plt.plot(time, vol, label="Volume")
            plt.legend()
        elif choice == 9:
            fig, (ax1, ax2, ax3, ax4, ax5, ax6) = plt.subplots(6)
            ax1.plot(time, data['watchers'], label="Watchers")
            ax2.plot(time, data['price'], label='Price')
            ax3.plot(time, data['pricechange'], label='Price Change')
            ax4.plot(time, data['msgvol'], label="Message Volume Change")
            ax5.plot(time, data['sentiment'], label="Sentiment Change")
            ax6.plot(time, vol, label="Volume")
            plt.legend()
            plt.show()
        else:
            break
        choice = 0


tickerC = input("Ticker:")
viewTicker(tickerC)
