import geopandas as gpd
import pandas as pd

def csv_to_geojson(csv_file, geojson_file):
    # Read the CSV file into a GeoDataFrame
    df = pd.read_csv(csv_file)
    gdf = gpd.GeoDataFrame(
    df, geometry=gpd.points_from_xy(df.latitude, df.longitude), crs="EPSG:4326"
)



    # Convert GeoDataFrame to GeoJSON format
    gdf.to_file(geojson_file, driver='GeoJSON')

if __name__ == "__main__":
    csv_file = 'manual_filtered_travis_tweets_with_blockgroups_with_scores_and_sentiment.csv'
    geojson_file = 'geo_2.geojson'

    hex_file = 'travis_hex.geojson'
    gdf_hex = gpd.read_file(hex_file)

    counts = []
    sentiments = []
    df = pd.read_csv(csv_file)
    tweets = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.latitude, df.longitude), crs="EPSG:4326")
    for index, row in gdf_hex.iterrows():
        filtered_tweets = tweets[(round(row.geometry.x, 6) == tweets.latitude.round(6)) & (round(row.geometry.y, 6) == tweets.longitude.round(6))]
        # print(tweets.latitude)
        # print(round(row.geometry.x, 6))
        counts.append(len(filtered_tweets))
        print(len(filtered_tweets))
        sentiments.append(filtered_tweets.VADAR_sentiment.mean())

    gdf_hex['count'] = counts
    gdf_hex['sentiment'] = sentiments

    gdf_hex.to_file('geo_.geojson')