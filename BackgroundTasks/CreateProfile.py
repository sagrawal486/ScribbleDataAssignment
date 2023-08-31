import pandas as pd
import os
import json
from Models.VideoProfile import VideoProfile
from typing import List
from datetime import date
from logger import LoggingInfo,LoggingError
class CreateProfile:
    
    def __init__(self,regions,attributes,dataset_path) -> None:
        self.Regions = regions
        self.Attributes = attributes
        self.Dataset_Path = dataset_path
        self.Categories = {}

    def createProfile(self) -> List[VideoProfile]:
        
        video_profiles = []
        try:
            for _,regions in self.Regions.items():
                
                LoggingInfo(f"Create Profile: Profile creation of region - {regions} is started")
                
                video_id_set = set()
                # Read CSV File
                csv_file = regions + "videos.csv"
                csv_file_path = os.path.join(self.Dataset_Path, csv_file)
                if regions in ('JP','KR','RU','MX'):
                    df = pd.read_csv(csv_file_path, encoding='ISO-8859-1')
                else:
                    df = pd.read_csv(csv_file_path)
                df = df.drop_duplicates()
                
                agg_functions = {
                'title': 'first',  # Keep the first value
                'channel_title': 'first',
                'category_id': 'first',
                'publish_time': 'first',
                'tags': 'first',
                'views': 'max',  # Max of views
                'likes': 'max',  
                'dislikes': 'max',
                'comment_count': 'max',
                'thumbnail_link': 'first',
                'comments_disabled': 'first',
                'ratings_disabled': 'first',
                'video_error_or_removed': 'first',
                'description': 'first'
                }
                df = df.groupby(['video_id', 'trending_date']).agg(agg_functions).reset_index()
                df['description'] = df['description'].astype(str)
                #Read Category JSON File
                json_file = regions + "_category_id.json"
                json_file_path = os.path.join(self.Dataset_Path, json_file)

                with open(json_file_path, "r") as category_data:
                    categories_data = json.load(category_data)

                self.Categories = {}
                self.processCategories(categories_data)
                
                for _, row in df.iterrows():
                    
                    if row['video_id'] == '#NAME?':
                        continue
                    
                    video_id_set.add(row['video_id'])
                    year, day, month = map(int, row["trending_date"].split('.'))
                    converted_date = date(year + 2000, month, day)
                    profile = {
                        "video_id": row["video_id"],
                        "trending_date": converted_date,
                        "title": row["title"],
                        "region": regions,
                        "channel_title": row["channel_title"],
                        "category_id": row["category_id"],
                        "tags": row["tags"],
                        "description": row["description"]              
                    }

                    # Map category ID to category title
                    category_id = str(row["category_id"])
                    if category_id in self.Categories:
                        profile["category_title"] = self.Categories[category_id]
                    else:
                        profile["category_title"] = "Unknown Category"

                    for _,attr in self.Attributes.items():
                        profile[attr] = row[attr]

                    obj = VideoProfile(**profile)

                    video_profiles.append(obj)
                LoggingInfo(f"Create Profile: Profile creation of region - {regions} is ended")
        except Exception as E:
            LoggingError("Create Profile: " + str(E)) 
        
        return video_profiles
        
    def processCategories(self,categories_data):

        for category in categories_data['items']:
            self.Categories[category['id']] = category['snippet']['title']


