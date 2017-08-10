#!/usr/bin/env python

import ConfigParser
import json
from pymongo import MongoClient
import tweepy

class ApplicationConnections():

    def __init__(self):
        self.config = self.get_config()
        self.mongo_client = None
        self.twitter_auth = None
    
    def get_config(self):
        '''
        Gets the config information from app_config.cfg
        '''
        config = ConfigParser.ConfigParser()
        config.readfp(open('app_config.cfg'))
        return config

    def get_mongo_client(self):
        '''
        Gets the mongo location and then connects.
        Returns a client object.
        '''
        if self.mongo_client is not None:
            return self.mongo_client
        mongo_server = self.config.get('Mongo', 'server')
        mongo_port = int(self.config.get('Mongo', 'port'))
        client = MongoClient(mongo_server, mongo_port)
        self.mongo_client = client
        return client

    def get_twitter_auth(self):
        '''
        Gets the twitter auth keys.
        Returns an auth object.
        '''
        if self.twitter_auth is not None:
            return self.twitter_auth
        consumer_token = self.config.get('Twitter', 'consumer_token')
        consumer_secret = self.config.get('Twitter', 'consumer_secret')
        access_key = self.config.get('Twitter', 'access_key')
        access_secret = self.config.get('Twitter', 'access_secret')
        auth = tweepy.OAuthHandler(consumer_token, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        self.twitter_auth = auth
        return auth


class MyStreamListener(tweepy.StreamListener):

    def __init__(self):
        self.conns = ApplicationConnections()
        self.mongo_client = self.conns.get_mongo_client()
        self.db = self.mongo_client['tweets']

    def on_data(self, data):
        '''
        Store data in mongo.
        Only storing relevant data for the task to save memory.
        '''
        json_data = json.loads(data)
        print json_data['geo']
        #self.db.insert()

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

