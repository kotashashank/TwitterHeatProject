# combine csvs to individual files
import pandas as pd
import geopandas as gpd

if(__name__ == '__main__'):
    # create dataframe
    combined_tweets_df = pd.DataFrame(columns = ['link','username','datetime','tweet_text','impressions','likes', 'longitude', 'latitude'])

    # add each location tweets to dataframe
    points = gpd.read_file("../data_retrieval/travis_hex.geojson")

    all_frames = []

    index = 0
    l = len(points)
    for point in points.geometry:
        long_lat_string = str(point.y) + "," + str(point.x)
        tweet_file = "../tweets_by_location/tweets_tc_2023/" + long_lat_string + '.csv'
        tweet_df = pd.read_csv(tweet_file)
        tweet_df['longitude'] = point.y
        tweet_df['latitude'] = point.x

        all_frames.append(tweet_df)
        index += 1
        print(str((index / l) * 100) + '%')
        
    
    combined_tweets_df = pd.concat(all_frames, ignore_index=True)

    combined_tweets_df.to_csv("../travis_tweets_2023.csv")
    # export data frame