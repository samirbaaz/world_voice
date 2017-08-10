# world_voice
A tool to see what people are talking about in the world right now.


To install required libraries and systems in osx:

    python:
    pip install tweepy
    pip install pymongo

    MongoDb:
    https://docs.mongodb.com/getting-started/shell/tutorial/install-mongodb-on-os-x/


Once the above have been installed, run gather_service with the following command:

python gather_service.py

You can run this in detached mode using the following command:

python gather_service.py &

app_config.cfg should look like this:
    [Mongo]
    server=localhost
    port=27017

    [Twitter]
    consumer_token=xxxxxxxx
    consumer_secret=xxxxxxxx
    access_key=xxxxxxxx
    access_secret=xxxxxxxx