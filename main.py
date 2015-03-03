# coding=utf8


from __future__ import print_function
import tweepy
import config
import sqlite3
import time
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import re


def login():
    auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
    auth.set_access_token(config.access_token, config.access_token_secret)
    api = tweepy.API(auth)
    return(api)

def tweetComparison(api, dbpath):
    connection = sqlite3.connect(dbpath)
    c = connection.cursor()
    tweeted = False
    while not tweeted:
        firstNounQuery = 'select WortID, Wort from Morph natural join Wort where Features like "%_Nom_Pl" order by random() limit 1'
        firstNounID, firstNoun = c.execute(firstNounQuery).fetchone()
        secondNounQuery = 'select Wort from Morph natural join Wort where Features like "%s_Nom_Pl" and not WortID = %d order by random() limit 1' % ("%", int(firstNounID))
        secondNoun = c.execute(secondNounQuery).fetchone()[0]
        adjectiveQuery = 'select Wort from Morph natural join Wort where Features = "Comp_Pred" order by random() limit 1'
        adjective = c.execute(adjectiveQuery).fetchone()[0]
        output = "%s sind %s als %s." % (firstNoun, adjective, secondNoun)


        if output != "":
            print(output)
            api.update_status(output)

        tweeted = True


tweetComparison(login(), "D:/git-repos/VergleichBot/vergleich.sqlite")