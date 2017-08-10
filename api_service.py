#!/usr/bin/env python

import pymongo
import argparse
import utils

def execute(msg_dict):
    '''
    This is the function that is executed for the api query parameters.
    '''
    conns = utils.ApplicationConnections()
    db = conns.get_db()
    #db.all_tweets.find()
    pass

if __name__ == '__main__':
    msg_dict = {}
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--lat', dest='lat', action='store',
                        default=0, help='input for the latitude (defaults to 0)')
    parser.add_argument('--long', dest='long', action='store',
                        default=0, help='input for the longitude (defaults to 0)')
    parser.add_argument('--radius', dest='radius', action='store',
                        default=10, help='input for the search radius (defaults to 10)')
    parser.add_argument('--amount', dest='amount', action='store',
                        default=250, help='input for the number of tweets (defaults to 250)')
    parser.add_argument('--search', dest='search', action='store',
                        default=None, help='input for the keyword to search for. (defaults to None)')
    args = parser.parse_args()
    
    msg_dict['amount'] = args.amount
    msg_dict['lat'] = args.lat
    msg_dict['long'] = args.long
    msg_dict['radius'] = args.radius
    msg_dict['search'] = args.search

    execute(msg_dict)