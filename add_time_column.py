# code to add datetime column to tweets (allows for sorting, filtering, etc)

import pandas as pd
from datetime import datetime


if(__name__ == '__main__'):
    # sort filtered tweets by time
    
    austin_tweets = pd.read_csv("../travis_tweets_2023.csv")

    # read timestamp, make columns for all, make combined timestamp
    austin_tweets['timestamp'] = austin_tweets.apply(lambda row: datetime.timestamp(datetime.strptime(row.datetime, '%Y-%m-%dT%H:%M:%S.%fZ')), axis=1)
    austin_tweets['year'] = austin_tweets.apply(lambda row: datetime.fromtimestamp(row['timestamp']).year, axis=1)
    austin_tweets['month'] = austin_tweets.apply(lambda row: datetime.fromtimestamp(row['timestamp']).month, axis=1)
    austin_tweets['day'] = austin_tweets.apply(lambda row: datetime.fromtimestamp(row['timestamp']).day, axis=1)
    austin_tweets['hour'] = austin_tweets.apply(lambda row: datetime.fromtimestamp(row['timestamp']).hour, axis=1)
    austin_tweets['minute'] = austin_tweets.apply(lambda row: datetime.fromtimestamp(row['timestamp']).minute, axis=1)
    austin_tweets['second'] = austin_tweets.apply(lambda row: datetime.fromtimestamp(row['timestamp']).second, axis=1)

    austin_tweets = austin_tweets.drop_duplicates(subset=['timestamp', 'username'])
    austin_tweets = austin_tweets.sort_values(by=['timestamp'])
    
    austin_tweets.to_csv("../travis_tweets_2023_time.csv")

    