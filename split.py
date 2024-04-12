import pandas as pd


if(__name__ == '__main__'):

    df = pd.read_csv('manual_filtered_travis_tweets_with_blockgroups_with_scores_and_sentiment.csv')

    df["VADAR_sentiment"] = pd.to_numeric(df["VADAR_sentiment"])
    positive = df[df['VADAR_sentiment'] >= 0.05]
    negative = df[df['VADAR_sentiment'] <= -0.05]
    nuetral = df[(df['VADAR_sentiment'] > -0.05) & (df['VADAR_sentiment'] < 0.05)]

    positive.to_csv('positive_tweets.csv')
    negative.to_csv('negative_tweets.csv')
    nuetral.to_csv('nuetral_tweets.csv')