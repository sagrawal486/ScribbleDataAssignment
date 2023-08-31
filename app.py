from fastapi import FastAPI
import configparser
from Database.Database import Database
from Workflows.CategoryPopularity import CategoryPopularity
from Workflows.TrendingVideos import TrendingVideos
from Workflows.FavouredChannels import FavouredChannels
import uvicorn
from Models.VideoProfile import Regions

app = FastAPI()

# Read configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

regions = config["Regions"]
dataset_path = config.get('Path', 'DataSetPath')
attributes = config["Attributes"]

db_url = config.get('Database', 'DBURL')

# Initialize Database object
database = Database(db_url)

@app.get("/")
def read_root():
    return {"Hello": "World"}


''' Define a task workflow for customers
find the category that have relatively higher business potential on basis of views and region
http://localhost:8000/category-popularity?region=US
'''
@app.get("/category-popularity")
def get_category_popularity(region: Regions):
    video_profiles = database.GetProfiles(region)
    category_popularity_obj = CategoryPopularity()
    category_popularity = category_popularity_obj.GetCategoryWiseData(video_profiles)
    return category_popularity

'''
Define a task workflow for customers
title of videos with maximum trending days
http://localhost:8000/trending-videos?region=US
'''
@app.get("/trending-videos")
def get_trending_videos(region: Regions):
    video_profiles = database.GetProfiles(region)
    trending_videos_obj = TrendingVideos()
    most_trending_videos = trending_videos_obj.GetTrendingWiseData(video_profiles)
    return most_trending_videos

'''
Define a task workflow for customers
most favoured channel
http://localhost:8000/favoured-channels?region=US
'''
@app.get("/favoured-channels")
def get_favoured_channels(region: Regions):
    video_profiles = database.GetProfiles(region)
    favoured_channels_obj = FavouredChannels()
    favoured_channels = favoured_channels_obj.GetFavouredChannels(video_profiles)
    return favoured_channels

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
 