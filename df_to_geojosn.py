import geopandas as gpd
import pandas as pd
from textblob import TextBlob

def csv_to_geojson(csv_file, geojson_file):
    # Read the CSV file into a GeoDataFrame
    df = pd.read_csv(csv_file)
    gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.latitude, df.longitude), crs="EPSG:4326"
)



    # Convert GeoDataFrame to GeoJSON format
    gdf.to_file(geojson_file, driver='GeoJSON')


def get_polarity(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

def get_subj(text):
    blob = TextBlob(text)
    return blob.sentiment.subjectivity

if __name__ == "__main__":
    csv_file = 'combined_travis_tweets.csv'
    geojson_file = 'geo_3.geojson'

    hex_file = 'travis_hex.geojson'
    gdf_hex = gpd.read_file(hex_file)

    counts = []
    sentiments = []
    polarity = []
    subjectivity = []
    df = pd.read_csv(csv_file)
    tweets = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.latitude, df.longitude), crs="EPSG:4326")
    # tweets["polarity"] = tweets.apply(lambda row: get_polarity(row.tweet_text), axis=1)
    # tweets["subjectivity"] = tweets.apply(lambda row: get_subj(row.tweet_text), axis=1)
    for index, row in gdf_hex.iterrows():
        filtered_tweets = tweets[((round(row.geometry.x, 6) - tweets.latitude.round(6))** 2 <= 0.00001) & ((round(row.geometry.y, 6) - tweets.longitude.round(6))** 2 <= 0.00001)]
        counts.append(len(filtered_tweets))
        print(len(filtered_tweets))
        # sentiments.append(filtered_tweets.VADAR_sentiment.mean())
        # polarity.append(filtered_tweets.polarity.mean())
        # subjectivity.append(filtered_tweets.subjectivity.mean())

    gdf_hex['count'] = counts

    gdf_hex.to_file('geo.geojson')