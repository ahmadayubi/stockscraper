import praw
import requests
from collections import Counter
import sys
from flask import jsonify
import os


class RedditScraper():
    def __init__(self, scrapeSize):
        self.scrapeSize = scrapeSize

    def __isStock(self, x):
        upper = True
        for letter in x:
            if letter.islower():
                upper = False
                break
        if upper or "$" in x:
            return True
        else:
            return False

    def scrape(self):
        reddit = praw.Reddit(client_id=os.environ.get("CLIENT_ID"),
                             client_secret=os.environ.get("CLIENT_SECRET"), user_agent='Reddit Stock Scraping')
        hotTickers = []
        newTickers = []
        totalTickers = []
        for k in range(2):
            if k == 0:
                postList = reddit.subreddit(
                    'pennystocks').hot(limit=self.scrapeSize)
            else:
                postList = reddit.subreddit(
                    'pennystocks').new(limit=self.scrapeSize)
            for post in postList:
                getTitle = True
                for j in range(2):
                    if getTitle:
                        sStr = post.title
                        getTitle = False
                    else:
                        sStr = post.selftext

                    for word in (sStr).split():
                        if len(word) < 5 and len(word) > 2 and word.isalpha() and self.__isStock(word):
                            page = requests.get(
                                'https://api.stocktwits.com/api/2/streams/symbol/'+word+".json")
                            page = page.json()
                            if page['response']['status'] != 404:
                                if k == 0:
                                    hotTickers.append(word)
                                else:
                                    newTickers.append(word)
                                # print(post.selftext)
                                break

        hotTickers = Counter(hotTickers)
        newTickers = Counter(newTickers)
        totalTickers.append(list(hotTickers.items()))
        totalTickers.append(list(newTickers.items()))
        return totalTickers
