from flask import Flask
from flask import Flask, request, render_template
from kaggle.api.kaggle_api_extended import KaggleApi

app = Flask(__name__)

def check_file_type(files):
    image = 0
    csv = 0
    if files.files[0].fileType.lower() in ['.jpg', '.png', '.webp','.tif']:
        image += 1
    elif files.files[0].fileType.lower() in ['.csv' ]:
        csv += 1
    print(image, csv)


'''api = KaggleApi()
api.authenticate()
text = 'google'
datasets = api.dataset_list(search=text)
for dat in datasets:
    check_file_type(api.dataset_list_files(dat.ref))


api = KaggleApi()
api.authenticate()
text = 'Google'
print(text)
datasets = api.dataset_list(search=text)
for dat in datasets:
    check_file_type(api.dataset_list_files(dat.ref))api_secret = '924eeda9ef2b4b5d9d41013ffdb7cd30'


import requests
import urllib
import json
import pprint

# Make the HTTP request.
response = requests.get('http://catalog.data.gov/api/3/action/package_search?q='+'camp&rows=50')
assert response.status_code == 200

# Use the json module to load CKAN's response into a dictionary.
response_dict = json.loads(response.content)

# Check the contents of the response.
assert response_dict['success'] is True
result = response_dict['result']
dataset=[]
for res in response_dict['result']['results']:
    tags = []
    for tag in res['tags']:
        tags.append(tag['name'])
    try:
        contentUrl = res['resources'][0]['url']
    except:
        contentUrl = 'empty'
    dataset.append({'name': res['title'],
                    'source': "Data.Gov",
                    'size': None,
                    'alternateName': res['notes'],
                    'url': 'https://catalog.data.gov/dataset/' + res['name'],
                    'tags': tags,
                    'contentUrl': contentUrl})


apiSecret = '924eeda9ef2b4b5d9d41013ffdb7cd30'
from newsapi import NewsApiClient

# Init
newsapi = NewsApiClient(api_key=apiSecret)

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      language='en',
                                      sort_by='relevancy',
                                      page=1)
text = 'camp'
response = requests.get('http://catalog.data.gov/api/3/action/package_search?q=' +text+ '&rows=50')
response_dict = json.loads(response.content)'''

'''from sodapy import Socrata

client = Socrata("data.kcmo.org", None)

client.datasets()

import twitter
api = twitter.Api(consumer_key='yXiLI7TBdAHIrH7xXH5GowVXV',
                  consumer_secret='aIeSh7bSSDqDKnL2DfahxAhLjz7ylKSHKvWIPDJaJa6UQKJgsg',
                  access_token_key='886704367-hXZFLJVBatKjuwllKB3v99jx5oGQ08VDQbaS0Ild',
                  access_token_secret='Pb2kN0Lb0Az0qgdwP6fLSYoyxR7hksvfOeWuzSQdlf3vl')

results = api.GetSearch(    raw_query="q=Cinnpie exposing was honestly%20&count=100", return_json=True)



from TwitterSearch import *
try:
    tso = TwitterSearchOrder() # create a TwitterSearchOrder object
    tso.set_keywords(['trump', 'china']) # let's define all words we would like to have a look for
    tso.set_language('en') # we want to see German tweets only
    tso.set_include_entities(False) # and don't give us all those entity information

    # it's about time to create a TwitterSearch object with our secret tokens
    ts = TwitterSearch(
        consumer_key = 'yXiLI7TBdAHIrH7xXH5GowVXV',
        consumer_secret = 'aIeSh7bSSDqDKnL2DfahxAhLjz7ylKSHKvWIPDJaJa6UQKJgsg',
        access_token = '886704367-hXZFLJVBatKjuwllKB3v99jx5oGQ08VDQbaS0Ild',
        access_token_secret = 'Pb2kN0Lb0Az0qgdwP6fLSYoyxR7hksvfOeWuzSQdlf3vl'
     )

     # this is where the fun actually starts :)
    for tweet in ts.search_tweets_iterable(tso):
        x= tweet
        print( '@%s tweeted: %s' % ( tweet['user']['screen_name'], tweet['text'] ) )
        break

except TwitterSearchException as e: # take care of all those ugly errors if there are some
    print(e)
'''
import tweepy
import time
consumer_key = "yXiLI7TBdAHIrH7xXH5GowVXV"
consumer_secret = "aIeSh7bSSDqDKnL2DfahxAhLjz7ylKSHKvWIPDJaJa6UQKJgsg"
access_token = "886704367-hXZFLJVBatKjuwllKB3v99jx5oGQ08VDQbaS0Ild"
access_token_secret = "Pb2kN0Lb0Az0qgdwP6fLSYoyxR7hksvfOeWuzSQdlf3vl"
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, parser=tweepy.parsers.JSONParser())

tweets_list = []
term = 'trump'
count = 100
num=500


# Pulling individual tweets from query
while len(tweets_list)<num:
    for status in api.search(q='trump', max_id=max_id, count=100)['statuses']:
        tweets_list.append(status)
    max_id=tweets_list[-1]['id']

'''for status in tweepy.Cursor(api.search, q='world', count=100, result_type='mixed', tweet_mode='extended').items(500):
    x.append(status._json)'''
