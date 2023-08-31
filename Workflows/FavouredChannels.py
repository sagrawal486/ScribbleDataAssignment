from Models.VideoProfile import VideoProfile
from typing import List
import pandas as pd
from logger import LoggingError,LoggingInfo
from fastapi import HTTPException

class FavouredChannels:

    def GetFavouredChannels(self,dataset: List[VideoProfile]) -> List:
        try:
            LoggingInfo("GetFavouredChannels: Getting Favoured Channels process started")        
            dataset = [[row.channel_title, row.views, row.likes, row.dislikes, row.comment_count] for row in dataset]
            video_data = pd.DataFrame(dataset, columns=["channel_title", "views", "likes", "dislikes", "comment_count"])
            
            # Calculate Appearance Frequency
            appearance_frequency = video_data['channel_title'].value_counts()
            video_data['likes'].replace(0, 1, inplace=True)
            video_data['dislikes'].replace(0, 1, inplace=True)
            # Calculate Like to Dislike Ratio
            video_data['like_dislike_ratio'] = video_data['likes']/video_data['dislikes']
            # Calculate the mean like to dislike ratio for each channel
            like_dislike_ratio = video_data.groupby('channel_title')['like_dislike_ratio'].mean()

            # Combine Judgment Criteria
            combined_score = (appearance_frequency + like_dislike_ratio) / 2

            # Create a DataFrame to store the results
            channel_scores = pd.DataFrame({
                'appearance_frequency': appearance_frequency,
                'like_dislike_ratio': like_dislike_ratio,
                'combined_score': combined_score
            })
            # Sort the channels by combined score in descending order
            top_channels = channel_scores.sort_values(by='combined_score', ascending=False)

            # Select the top N channels
            top_n = 10  # Change this value to select a different number of channels
            top_channels = top_channels.head(top_n).index.tolist()

            LoggingInfo("GetFavouredChannels: Getting Favoured Channels process ended")
            return top_channels
        
        except Exception as e:
            LoggingError("GetFavouredChannels: Getting Favoured Channels process failed with error: " + str(e))
            raise HTTPException("Internal Server Error")
    