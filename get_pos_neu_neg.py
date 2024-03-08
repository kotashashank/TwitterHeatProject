import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# pip (or pip3) install pandas
# pip (or pip3) install vaderSentiment

def sentiment_scores(sentence):
 
    # Create a SentimentIntensityAnalyzer object.
    sid_obj = SentimentIntensityAnalyzer()
 
    sentiment_dict = sid_obj.polarity_scores(sentence)

    return sentiment_dict
     

if __name__ == '__main__':
    df = pd.read_csv('manual_filtered_travis_tweets_with_blockgroups_with_scores.csv')
    sentiments = []
    
    positive = 0
    neutral = 0
    negs = 0
    for tweet in df['tweet_text']:

            # print(tweet)
            score = sentiment_scores(tweet)
            comp = score['compound']
            if(comp >= 0.25):
                positive += 1
            elif(comp <= -0.25):
                negs += 1
            else:
                neutral += 1


    print(positive, neutral, negs)
    # df['VADAR_sentiment'] = sentiments  # Add the bot scores to the DataFrame as a new column
    # df.to_csv('manual_filtered_travis_tweets_with_blockgroups_with_scores_and_sentiment.csv', index=False)  # Save the DataFrame with scores to a new CSV file
