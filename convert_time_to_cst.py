# convert times to CSV
import pytz
from datetime import datetime, timedelta
import pandas as pd
if(__name__ == '__main__'):
    tweets = pd.read_csv('strict_filtered_travis_tweets.csv')
    tz = pytz.timezone('US/Central')
    tweets['timestamp'] = tweets.apply(lambda row: datetime.fromisoformat(row['datetime']).timestamp(), axis=1)
    tweets['cst_time'] = tweets.apply(lambda row: datetime.fromisoformat(row['datetime']).astimezone(tz), axis=1)
    tweets.to_csv('strict_filtered_travis_tweets.csv')