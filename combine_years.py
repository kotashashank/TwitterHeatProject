# combine two individual csv files together 

import pandas as pd

if(__name__ == '__main__'):
    files = ['travis_tweets_time.csv','travis_tweets_2023_time.csv']
    
    combined_df = pd.read_csv(files[0])
    for file in files[1:]:
        df = pd.read_csv(file)
        combined_df = pd.concat([combined_df, df])
    
    print(len(combined_df))
    combined_df.to_csv('combined_travis_tweets.csv')