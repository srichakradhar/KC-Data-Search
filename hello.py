from os.path import sep
from sodapy import Socrata
from flask import Flask, render_template, request, make_response
import json
import tweepy
from kaggle.api.kaggle_api_extended import KaggleApi
from newsapi import NewsApiClient
import requests
import random
import json

count = 0
datasetCount = 1
oldTerm = ''
newsPage = 1
client = Socrata("data.kcmo.org", None)

app = Flask(__name__, template_folder='templates')

def check_file_type(files):
    image = 0
    csv = 0
    if files.files[0].fileType.lower() in ['.jpg', '.png', '.webp','.tif']:
        return 'Image'
    elif files.files[0].fileType.lower() in ['.csv' ]:
        return 'CSV'
    elif files.files[0].fileType.lower() in ['.json' ]:
        return 'JSON'
    elif files.files[0].fileType.lower() in ['.xml' ]:
        return 'XML'
    elif files.files[0].fileType.lower() in ['.ndjson' ]:
        return 'NdJSON'

@app.route('/')
def my_form():
    #return "Hello World"
    return render_template('data.html')

@app.route('/', methods=['POST'])
def my_form_post():
    api = KaggleApi()
    print('Hello')
    api.authenticate()
    text = request.form['text']
    datasets = api.dataset_list(search=text)
    response = requests.get('http://catalog.data.gov/api/3/action/package_search?q=' +text+ '&rows=50')
    response_dict = json.loads(response.content)
    dataset = list()
    for dat in datasets:
        dataset.append({'name':dat.title,
            'source':'Kaggle',
            'size':dat.size,
            'alternateName':dat.subtitle,
            'url':dat.url,
            'tags':dat.tags,
            'contentUrl':'https://www.kaggle.com/'+dat.ref+'/download'})

    for res in response_dict['result']['results']:
        tags = []
        for tag in res['tags']:
            tags.append(tag['name'])
        try:
            contentUrl=res['resources'][0]['url']
        except:
            contentUrl='empty'
        dataset.append({'name':res['title'],
        'source':"Data.Gov",
        'size':None,
        'alternateName':res['notes'],
        'url':'https://catalog.data.gov/dataset/' + res['name'],
        'tags':tags,
        'contentUrl':contentUrl})


    random.shuffle(dataset)
    return  render_template('data.html', datasetInfo=dataset, value=text)

@app.route('/loaddata')
def loaddata():
    source = request.args.get('source')
    term = request.args.get('term')
    global oldTerm, count, datasetCount, newsPage
    if(term != oldTerm):
        oldTerm = term
        count = 0
        datasetCount = 1
        newsPage = 1
    if(source=='Kaggle'):
        api = KaggleApi()
        api.authenticate()
        text = term
        datasets = api.dataset_list(search=text, page = datasetCount)
        if not datasets:
        dataset = []
        i=0
        for dat in datasets[count:count+4]:
            i = i+1
            dataset.append({'name': dat.title,
                            'source': 'Kaggle',
                            'size': dat.size,
                            'alternateName': dat.subtitle,
                            'url': dat.url,
                            'date': str(dat.lastUpdated),
                            'tags': str(dat.tags),
                            'contentUrl': 'https://www.kaggle.com/' + dat.ref + '/download',
                            'fileType': check_file_type(api.dataset_list_files(dat.ref))})
        count = count + len(dataset)
        if not dataset:
            datasetCount += 1
            count = 0
        resu = make_response(json.dumps(dataset), 200)
        return resu
    elif(source=='News'):
        apiSecret = '74fa401c60a045438f71dd307d1399e9'
        newsapi = NewsApiClient(api_key=apiSecret)
        all_articles = newsapi.get_everything(q=term,
                                              language='en',
                                              sort_by='relevancy',
                                              page=newsPage)
        newsPage += 1
        resu = make_response(json.dumps(all_articles['articles']), 200)
        return resu
    elif(source=='Data.gov'):
        response = requests.get('http://catalog.data.gov/api/3/action/package_search?q=' +term+ '&rows=50')
        response_dict = json.loads(response.content)
        resu = make_response(json.dumps(response_dict['result']['results']), 200)
        return resu
    elif(source=='KCMO.org'):
        global client
        result = client.datasets(q=term)
        resu = make_response(json.dumps(result), 200)
        return resu
    elif(source=='Twitter'):
        num = int(request.args.get('count'))
        consumer_key = "kY9uF1FuC7GzMyVxMRHku61Kx"
        consumer_secret = "Zk4bTnmMzNF8UTmMhviocFZa1a5Ny6sSZuSjI00xhsPvhzcAvS"
        access_token = "1291188055068610561-I9fHoOhalXPjYXkYa7VWlbS7xFM1N1"
        access_token_secret = "y1Pnxq4weOc80btZtAT5XiI9hIO370WjdQzgMs8waPYI8"
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth, wait_on_rate_limit=True, parser=tweepy.parsers.JSONParser())

        x = (api.search(q=term, count=100))
        max_id = x['search_metadata']['max_id']

        tweets_list=[]

        # Pulling individual tweets from query

        while len(tweets_list) < num:
            for status in api.search(q=term, max_id=max_id, count=100, result_type='mixed', tweet_mode='extended')['statuses']:
                tweets_list.append(status)
            max_id = tweets_list[-1]['id']

        resu = make_response(json.dumps(tweets_list), 200)
        return resu



if __name__ == '__main__':
    app.run()
