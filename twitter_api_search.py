import requests
import urllib
import time
import pandas as pd
import json
import datetime as dt
import os
### local libraries
from utils.get_logger import get_logger
from utils.config import headers, params
from utils.preprocessing import get_tweets
logger = get_logger('twitter_api_search')
if 'results' not in os.listdir():
    os.mkdir('results')


class Twitter_Api():
    MAX_ATTEMPTS = 10
    counter = 1
    delay = 5
    url_search = "https://api.twitter.com/2/tweets/search/recent"

    def __init__(self, params ):
        self.params = params
        self.list_response = []

    def get_tweets(self, next_token = None):
        """
        Returns a list of tweets between start_date and end_date
        """
        if next_token is None:
            first_url = self.url_search+ "?" + urllib.parse.urlencode(params)            
            #logger.info(f'################## {first_url} ####################')
            logger.info(f'{"#"*25} {args.query} {"#"*25}')
            response = requests.request("GET", first_url, headers=headers).json()
            time.sleep(self.delay)

            metadata = response.get('meta') 
            if 'newest_id' not in metadata:
                return None
            with open(f'utils/since_id_{args.query}.txt', mode='w') as f:
                f.write(metadata['newest_id'])
        else:
            self.params['next_token'] = next_token
            url_with_next_token = self.url_search + '?' + urllib.parse.urlencode(self.params)
            # logger.info(f'################## {url_with_next_token} ####################')
            response = requests.request("GET", url_with_next_token, headers=headers).json()
            time.sleep(self.delay)
            self.counter += 1
            if self.counter == self.MAX_ATTEMPTS:
                return None
            metadata = response.get('meta') 

        if response.get('errors'):
            if response['errors'][0].get('code') == 88:
                mesg = f"Rate limit exceeded" 
                logger.error(mesg)      
                return None
            else:
                mesg = str(response.get('errors'))
                logger.error(mesg)

        mesg = f"Uploading info...{metadata.get('result_count')} tweets found, run coun : {self.counter}"
        logger.info(mesg)  
        self.list_response.append(response)

        if 'next_token' in metadata:
            next_token = metadata.get('next_token')
            self.get_tweets(next_token)       
        else:
            return None

def convert_date(fecha):
    fecha = dt.datetime.strptime(fecha,'%Y-%m-%d %H:%M:%S') 
    fecha = fecha + dt.timedelta(hours = 5)
    fecha = fecha.strftime("%Y-%m-%dT%H:%M:%SZ")
    return fecha

def main():
    if args.since:
        since = convert_date(args.since)
        params['start_time'] = since

    if args.until:
        until = convert_date(args.until)
        params['end_time'] = until

    if args.since_id:
        if f'since_id_{args.query}.txt' in os.listdir('utils'):
            with open(f'utils/since_id_{args.query}.txt', mode='r') as f:
                since_id = f.read().strip()
            params['since_id'] = since_id
            del params['start_time']

    params['query'] = args.query
    twitter_api = Twitter_Api(params=params)
    twitter_api.get_tweets(next_token=None)
    list_response = twitter_api.list_response

    list_df = []
    for response in list_response:
        df = get_tweets(response)
        list_df.append(df)
    if not list_df:
        return None
    df_final = pd.concat(list_df)

    if args.output == 'csv':
        df_final.to_csv(f'results/tweets_{args.query}.csv',index = False, encoding='utf-8')
    if args.output == 'pkl':
        df_final.to_pickle(f'results/tweets_{args.query}.pkl')
    if args.output == 'json':
        dict_json = df_final.astype(str).to_dict('records')
        with open(f'results/tweets_{args.query}.json', mode='w') as f:
            json.dump(dict_json,f)

if __name__=='__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--query','-q',
                        dest = 'query',
                        help = 'indicar el query a recolectar')

    parser.add_argument('--output','-o',
                        dest = 'output',
                        help = 'indicar el tipo de archivo a guardar',
                        choices = ['csv','pkl','json'],
                        default = 'csv')

    parser.add_argument('--since','-s',
                        dest = 'since',
                        help = 'indicar la fecha de inicio')

    parser.add_argument('--until','-u',
                        dest = 'until',
                        help = 'indicar la fecha final')

    parser.add_argument('--since_id',
                        dest = 'since_id',
                        help = 'indicar la fecha de inicio',
                        action = 'store_true')

    args = parser.parse_args()

    main()
