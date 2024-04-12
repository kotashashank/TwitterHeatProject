import pandas as pd
import time
import math
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def get_absolute(row):
    try:
        return (row.postive_score - row.negative_score) / (row.postive_score + row.negative_score + row.neutral_score)
    except:
        return pd.NA

def get_proportional(row):
    try:
        return (row.postive_score - row.negative_score) / (row.postive_score + row.negative_score)
    except:
        return pd.NA
def get_logit(row):
    try:
        return math.log(row.postive_score + 0.5) - math.log(row.negative_score + 0.5)
    except:  
        
        return pd.NA
if __name__ == '__main__':
    df = pd.read_csv('manual_filtered_travis_tweets_with_blockgroups_with_scores_and_detailed_sentiment.csv')
    absolute = []
    relative_proportional = []
    logic_scale = []
    df['absolute_score'] = df.apply(lambda row: get_absolute(row), axis=1)
    df['relative_proportional_score'] = df.apply(lambda row: get_proportional(row), axis=1)
    df['logit_score'] = df.apply(lambda row: get_logit(row), axis=1)
    
    df.to_csv('manual_filtered_travis_tweets_with_blockgroups_with_scores_and_detailed_extra_sentiment.csv', index=False)  # Save the DataFrame with scores to a new CSV file
