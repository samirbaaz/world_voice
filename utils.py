#!/usr/bin/env python

import ConfigParser
import json
from pymongo import MongoClient, GEO2D
import tweepy

class ApplicationConnections():

    def __init__(self):
        self.config = self.get_config()
        self.mongo_client = None
        self.twitter_auth = None
        self.db = None
    
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

    def get_db(self, db_name='tweets'):
        if self.db is not None:
            return self.db
        client = self.get_mongo_client()
        db = None
        '''
        database_names is dangerous if there are a lot of dbs.
        '''
        if 'tweets' not in client.database_names():
            db = self.mongo_client['tweets']
            db.all_tweets.create_index([("geo", GEO2D), ("timestamp_ms", -1)])
        if db is None:
            db = self.mongo_client['tweets']
        self.db = db
        return db

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
        self.db = self.conns.get_db()

    def on_data(self, data):
        '''
        Store data in mongo.
        Only storing relevant data for the task to save memory.
        TODO: Clean up text so we don't have junk/emojis in mongo.
        '''
        json_data = json.loads(data)
        if 'geo' not in json_data or json_data['geo'] is None:
            '''
            Choosing to ignore these tweets for now.
            TODO: add location from palces for them.
            '''
            return
        insert_data = {'geo': json_data['geo']['coordinates'],
                       'text': json_data['text'],
                       'timestamp_ms': int(json_data["timestamp_ms"])}
        self.db.all_tweets.insert(insert_data)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

