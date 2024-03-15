import pandas as pd
import time
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


def sentiment_scores(sentence):
 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    sentiment_dict = sid_obj.polarity_scores(sentence)

    return sentiment_dict
     

if __name__ == '__main__':
    df = pd.read_csv('manual_filtered_travis_tweets_with_blockgroups_with_scores.csv')
    sentiments = []
    for tweet in df['tweet_text']:
        try:
            score = sentiment_scores(tweet)
            comp = score['compound']
            sentiments.append(comp)
        except:
            sentiments.append('N/A')  # Append 'N/A' if score extraction fails


    df['VADAR_sentiment'] = sentiments  # Add the bot scores to the DataFrame as a new column
    df.to_csv('manual_filtered_travis_tweets_with_blockgroups_with_scores_and_sentiment.csv', index=False)  # Save the DataFrame with scores to a new CSV file
