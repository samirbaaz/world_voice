#!/usr/bin/env python

import tweepy
import utils

def execute(msg_dict):
    GEOBOX_WORLD = [-180,-90,180,90]
    conns = utils.ApplicationConnections()

    stream = tweepy.streaming.Stream(conns.get_twitter_auth(), utils.MyStreamListener())
    stream.filter(locations=GEOBOX_WORLD)


if __name__ == '__main__':
    msg_dict = {}
    execute(msg_dict)