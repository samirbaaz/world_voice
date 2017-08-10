#!/usr/bin/env python

import pymongo
import argparse
import utils

def execute(msg_dict):
    '''
    This is the function that is executed for the api query parameters.
    TODO: Clean up variable names and code quality.
    '''
    conns = utils.ApplicationConnections()
    db = conns.get_db()

    tmp_lat = float(msg_dict['lat'])
    tmp_long = float(msg_dict['long']) 
    tmp_rad = float(msg_dict['radius'])
    tmp_amt = int(msg_dict['amount'])
    tmp_search = msg_dict['search']
    if not tmp_search:
        cur = db.all_tweets.find({'geo': {'$within': {'$center': [[tmp_lat, tmp_long], tmp_rad]}}},
                                 {'_id': 0}).sort([('timestamp_ms', -1)]).limit(tmp_amt)
    else:
        '''
        TODO: Look into using the $text $search functionality once a text index is added.
        '''
        cur = db.all_tweets.find({'text': {'$regex': tmp_search},
                                  'geo': {'$within': {'$center': [[tmp_lat, tmp_long], tmp_rad]}}},
                                 {'_id': 0}).sort([('timestamp_ms', -1)]).limit(tmp_amt)
    out = [x for x in cur]
    return out

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

    print execute(msg_dict)