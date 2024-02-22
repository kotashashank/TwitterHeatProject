# code to add block groups for each tweet

import geopandas as gpd
import shapely as shp

def find_blockgroups(blockgroups, longitude, latitude):

    meter_per_degree = 1 / 111_111
    point = shp.Point(latitude, longitude)
    buffer = shp.buffer(point, 200 * meter_per_degree)
    # print(shp.area(buffer))
    # polygon = shp.Polygon(buffer)

    groups = "{'"


    

    for i, row in block_groups.iterrows():
        bg = row['geometry'] # get block group


        # print(bg.intersection(buffer).area, bg.intersection(buffer).area / buffer.area)
        area = ((buffer.intersection(bg).area/buffer.area))
        # if bg.intersects(buffer):
            
            # print(area)

        if(area >= .1):
            string_area = "{:.2f}".format(area)
            groups += (row['GEOID'] + "':" + string_area + ",'")
            # print("intersection for point " + str(point.x) + "with area " + str(area))
        
        # get buffer range of point
        # point


    
    return groups[:-2] + '}'
        

        

if(__name__ == '__main__'):
    
    # load tweets
    tweets = gpd.read_file('filtered_travis_tweets.csv')
    
    # load block groups
    block_groups = gpd.read_file("travis_block_groups.geojson")


    tweets['blockgroups'] = tweets.apply(lambda row: find_blockgroups(block_groups, row['longitude'], row['latitude']), axis=1)

    print(tweets.head())
    tweets.to_csv('filtered_travis_tweets_with_blockgroups.csv')
    