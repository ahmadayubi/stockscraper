from selenium import webdriver
import pandas as pd
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import os
import csv
import sys


def scrape(fileDirectory):
    options = Options()
    options.headless = True

    with os.scandir("data/") as it:
        for entry in it:
            if entry.name.endswith(".csv") and entry.is_file():
                driver = webdriver.Chrome(
                    fileDirectory, options=options)
                ticker = entry.name[:-4]
                baseURL = 'https://stocktwits.com/symbol/'+ticker
                driver.get(baseURL)

                messageVolElem = driver.find_elements_by_xpath(
                    '//*[@id="app"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div/div/div[3]/div/div[1]')[0]
                messageFavorParent = driver.find_elements_by_xpath(
                    '//*[@id="app"]/div/div/div[3]/div[2]/div/div[1]/div[1]/div/div[2]/div/div/div[1]/div/div/div[3]/div/div[1]')[0]
                #attributeValue = messagefavor[0].get_attribute("class")
                messageFavor = messageFavorParent.find_elements_by_tag_name("svg")[
                    0]
                isRed = "st_37VuZWc" in messageFavor.get_attribute("class")

                messageVol = float(messageVolElem.text[:-1])
                if isRed:
                    messageVol = messageVol * -1
                vol = driver.find_element_by_css_selector(
                    '.st_2TXS0JE:nth-child(7) > .st_17sIB4J').get_attribute("innerHTML")

                watchers = driver.find_element_by_css_selector(
                    'strong').get_attribute('innerHTML')

                price = driver.find_element_by_css_selector('#app > div > div > div.st_1ccHZxv.st_jGV698i.st_1Z-amNw.st_cUBEAH8.st_3QTv-Ni > div.st_3rHBbGs.st_3QTv-Ni > div > div.st_2DHOr4A.st_3QTv-Ni.st_DmhifDD.st_CjvTpBY.st_2-AYUR9 > div.st_1vtoWp9.st_29vRgrA.st_1GuPg4J.st_2ve8DZ3 > div > div.st_2JjBhU0.st_jGV698i.st_cUBEAH8.st_3QTv-Ni > div > div > div.st_2U5mVnh.st_jGV698i.st_1GuPg4J.st_1jlXvfv > div.st_2Fof5or > span.st_3lrv4Jo.st_8u0ePN3.st_2oUi2Vb.st_31YdEUQ.st_8u0ePN3.st_2mehCkH.st_3kXJm4P').get_attribute('innerHTML')
                price = ''.join(reversed(price))

                exPrice = ''
                for ch in price:
                    if ch == ">":
                        exPrice = ''.join(reversed(exPrice))
                        break
                    else:
                        exPrice = exPrice + ch

                fileName = 'data/'+ticker+'.csv'
                date = datetime.now()
                fields = [date, ticker, watchers, exPrice, messageVol, vol]
                with open(fileName, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow(fields)
                driver.close()


def addTicker():
    print("Ticker:")
    ticker = input()
    ticker = "data/" + ticker + ".csv"
    with open(ticker, 'w', newline='') as f:
        writerC = csv.writer(f)
        writerC.writerow(
            ['date', 'ticker', 'watchers', 'price', 'msgvol', 'vol'])


with open(os.path.join(sys.path[0], ".local"), "r") as var:
    directory = var.readline()

print('1.Scrape')
print('2.Add new ticker')
userIn = input()
if userIn == '1':
    scrape(directory)
else:
    addTicker()
