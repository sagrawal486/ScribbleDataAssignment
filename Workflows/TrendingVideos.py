from Models.VideoProfile import VideoProfile
from typing import List
import pandas as pd
from logger import LoggingError,LoggingInfo
from fastapi import HTTPException

class TrendingVideos:
    
    def GetTrendingWiseData(self,dataset: List[VideoProfile]) -> List:
        try:
            LoggingInfo("GetTrendingWiseData: Getting Most Trending Video process started")
            dataset = [[row.video_id, row.title, row.trending_date, row.views, row.likes, row.dislikes, row.comment_count] for row in dataset]
            df = pd.DataFrame(dataset, columns=["video_id", "title","trending_date", "views", "likes", "dislikes", "comment_count"])
            
            # Group the data by video_id and count the number of unique days a video trended
            trending_videos = df.groupby('video_id')['trending_date'].nunique()

            # Sort the videos by the number of unique trending days in descending order
            sorted_trending_videos = trending_videos.sort_values(ascending=False)

            # Display the top 10 trending videos
            top_trending_videos = sorted_trending_videos.head(10).index.to_list()
            
            # Filter the original DataFrame to get the top titles based on video_id
            top_titles_df = df[df['video_id'].isin(top_trending_videos)][['title']]
            top_titles = top_titles_df.drop_duplicates()['title'].to_list()
            
            LoggingInfo("GetTrendingWiseData: Getting Most Trending Video process ended")
            return top_titles
        
        except Exception as e:
            LoggingError("GetTrendingWiseData: Getting Most Trending Video process failed with error: " + str(e))
            raise HTTPException("Internal Server Error")
        