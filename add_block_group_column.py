import pandas as pd
import geopandas as gpd
import shapely as shp
import numpy as np

def find_blockgroups(row, blockgroups, longitude, latitude):
    meter_per_degree = 1 / 111_111
    
    print(longitude, latitude)
    print(row.tweet_text)
    point = shp.Point(latitude, longitude)
    buffer = point.buffer(200 * meter_per_degree)  # Creating buffer around the point

    # Calculate intersection areas between buffer and block groups
    intersection_areas = {}
    for _, row in blockgroups.iterrows():
        bg = row['geometry']
        area = buffer.intersection(bg).area / buffer.area
        intersection_areas[row['GEOID']] = area

    # Sort block groups by intersection area in descending order
    sorted_blockgroups = sorted(intersection_areas.items(), key=lambda x: x[1], reverse=True)

    # Create lists for block groups and weights
    blockgroups_list = []
    weights_list = []
    for bg, weight in sorted_blockgroups:
        if(weight > 0.0):
            blockgroups_list.append(bg)
            weights_list.append(weight)

    # Pad the lists with None values if less than 5 block groups are found
    while len(blockgroups_list) < 6:
        blockgroups_list.append(None)
        weights_list.append(None)

    return blockgroups_list[:6], weights_list[:6]  # Returning top 5 block groups and their weights

if __name__ == '__main__':
    # Load tweets
    tweets = gpd.read_file('manual_filtered_travis_tweets.csv')
    
    tweets['is_heat_related'] = tweets['is_heat_related'].replace('', np.nan)
    tweets['longitude'] = tweets['longitude'].replace('', np.nan)
    # print(tweets.head())
    filtered_tweets = tweets[pd.isnull(tweets['is_heat_related'])]
    # filtered_tweets = filtered_tweets[~pd.isnull(filtered_tweets['longitude'])]
    # Load block groups
    block_groups = gpd.read_file("travis_block_groups.geojson")

    # Apply find_blockgroups function to each tweet
    blockgroups_data = filtered_tweets.apply(lambda row: find_blockgroups(row, block_groups, row['longitude'], row['latitude']), axis=1)
    
    # Create separate DataFrames for block groups and weights
    blockgroups_df = pd.DataFrame(blockgroups_data.apply(lambda x: x[0]).to_list(), columns=['BG1', 'BG2', 'BG3', 'BG4', 'BG5', 'BG6'])
    weights_df = pd.DataFrame(blockgroups_data.apply(lambda x: x[1]).to_list(), columns=['weight1', 'weight2', 'weight3', 'weight4', 'weight5', 'weight6'])

    # Replace block group IDs with NaN where weight is 0
    blockgroups_df[weights_df == 0] = np.nan

    # Concatenate block group columns and weight columns
    result_df = pd.concat([blockgroups_df, weights_df], axis=1)

    # Concatenate original tweets data with block group information
    tweets_with_blockgroups = pd.concat([filtered_tweets, result_df], axis=1)

    print(tweets_with_blockgroups.head())
    
    # Save result to CSV
    tweets_with_blockgroups.to_csv('filtered_travis_tweets_with_blockgroups.csv', index=False)
