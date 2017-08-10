#!/usr/bin/env python

import ConfigParser
from pymongo import MongoClient

def get_mongo_client():
    config = ConfigParser.ConfigParser()
    config.readfp(open('app_config.cfg'))
    mongo_server = config.get('Mongo', 'server')
    mongo_port = int(config.get('Mongo', 'port'))
    client = MongoClient(mongo_server, mongo_port)
    return client