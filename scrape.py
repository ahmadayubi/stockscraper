from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os
import csv
import sys
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

# uses selenium to scrape stocktwits.com
# fileDirectory is the directory path to chromedriver.exe


def scrape(fileDirectory):
    options = Options()
    options.headless = True
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    watch = []
    fileCount = next(os.walk('data/'))[2]
    count = len(fileCount)
    curIter = 0
    with os.scandir("data/") as it:
        for entry in it:
            if entry.name.endswith(".csv") and entry.is_file():
                # Print progress bar
                printProgressBar(curIter, count)

                # Setup driver
                driver = webdriver.Chrome(
                    fileDirectory, options=options)
                ticker = entry.name[:-4]
                baseURL = 'https://stocktwits.com/symbol/'+ticker
                driver.get(baseURL)

                # Message volume
                messageFavorParent = driver.find_elements_by_xpath(
                    '//*[@id="app"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div/div/div[3]/div/div[1]')[0]
                #attributeValue = messagefavor[0].get_attribute("class")
                messageFavor = messageFavorParent.find_elements_by_tag_name("svg")[
                    0]
                isRed = "st_37VuZWc" in messageFavor.get_attribute("class")

                messageVol = float(messageFavorParent.text[:-1])
                if isRed:
                    messageVol = messageVol * -1

                # Sentiment Change
                sentimentFavorParent = driver.find_elements_by_xpath(
                    '//*[@id="app"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div/div/div[2]/div/div[1]')[0]
                #attributeValue = messagefavor[0].get_attribute("class")
                sentimentFavor = messageFavorParent.find_elements_by_tag_name("svg")[
                    0]
                sentimentIsRed = "st_37VuZWc" in sentimentFavor.get_attribute(
                    "class")

                sentimentChange = float(sentimentFavorParent.text[:-1])
                if sentimentIsRed:
                    sentimentChange = sentimentChange * -1

                # Price Change
                priceFavorParent = driver.find_elements_by_xpath(
                    '//*[@id="app"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div/div/div[1]/div/div[1]')[0]
                #attributeValue = messagefavor[0].get_attribute("class")
                priceFavor = messageFavorParent.find_elements_by_tag_name("svg")[
                    0]
                priceIsRed = "st_37VuZWc" in priceFavor.get_attribute(
                    "class")

                priceChange = float(priceFavorParent.text[:-1])
                if priceIsRed:
                    priceChange = priceChange * -1

                # Volume
                myElem = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '.st_2TXS0JE:nth-child(7) > .st_17sIB4J')))
                try:
                    vol = driver.find_element_by_css_selector(
                        '.st_2TXS0JE:nth-child(7) > .st_17sIB4J').get_attribute("innerHTML")
                except TimeoutException:
                    print("Volume Load Error")
                    vol = 'err'
                vol = vol.rstrip("\n")

                # Number of Watchers
                watchers = driver.find_element_by_css_selector(
                    'strong').get_attribute('innerHTML')
                watchers = str(watchers)

                watchers = int(watchers.replace(',', ''))
                # Price of Ticker

                price = driver.find_element_by_css_selector('#app > div > div > div.st_1ccHZxv.st_jGV698i.st_1Z-amNw.st_cUBEAH8.st_3QTv-Ni > div.st_3rHBbGs.st_3QTv-Ni > div > div.st_2DHOr4A.st_3QTv-Ni.st_DmhifDD.st_CjvTpBY.st_2-AYUR9 > div.st_1vtoWp9.st_29vRgrA.st_1GuPg4J.st_2ve8DZ3 > div > div.st_2JjBhU0.st_jGV698i.st_cUBEAH8.st_3QTv-Ni > div > div > div.st_2U5mVnh.st_jGV698i.st_1GuPg4J.st_1jlXvfv > div.st_2Fof5or > span.st_3lrv4Jo.st_8u0ePN3.st_2oUi2Vb.st_31YdEUQ.st_8u0ePN3.st_2mehCkH.st_3kXJm4P').get_attribute('innerHTML')

                price = ''.join(reversed(price))

                exPrice = ''
                for ch in price:
                    if ch == ">":
                        exPrice = ''.join(reversed(exPrice))
                        break
                    else:
                        exPrice = exPrice + ch

                # Write to CSV File
                fileName = 'data/'+ticker+'.csv'
                date = datetime.now()
                fields = [date, ticker, watchers, exPrice,
                          priceChange, messageVol, sentimentChange, vol]
                with open(fileName, 'a', newline='') as f:
                    writeTo = csv.writer(f)
                    writeTo.writerow(fields)
                driver.close()

                # conditions for needing to view ticker after scrape
                if (messageVol > (3 * priceChange) and messageVol >= 10 and priceChange >= -50):
                    watch.append(ticker)
                curIter += 1

    printProgressBar(curIter, curIter)
    print("Stocks to manually view today: ", watch)


def printProgressBar(iteration, total):
    percent = ("{0:." + str(1) + "f}").format(100 *
                                              (iteration / float(total)))
    filledLength = int(50 * iteration // total)
    bar = '█' * filledLength + '-' * (50 - filledLength)
    print('\r%s |%s| %s%% %s' % ('Progress:', bar, percent, 'Harvested'), "\r")
    if iteration == total:
        print()


def addTicker():
    print("Ticker:")
    ticker = input()
    page = requests.get('https://stocktwits.com/symbol/'+ticker)
    soup = BeautifulSoup(page.content, 'html.parser')
    validTicker = soup.find('h3')
    if validTicker is not None:
        print("Invalid Ticker")
    else:
        ticker = "data/" + ticker + ".csv"
        with open(ticker, 'w', newline='') as f:
            writerC = csv.writer(f)
            writerC.writerow(
                ['date', 'ticker', 'watchers', 'price', 'pricechange', 'msgvol', 'sentiment', 'vol'])


with open(os.path.join(sys.path[0], ".local"), "r") as var:
    directory = var.readline()

print('1.Scrape')
print('2.Add new ticker')
# TODO :Add ability to add multiple tickers in one input, from csv file
userIn = input()
if userIn == '1':
    scrape(directory)
else:
    addTicker()
