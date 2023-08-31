from Models.VideoProfile import VideoProfile
from typing import List
import pandas as pd
from logger  import LoggingError, LoggingInfo
class ViewOutlier:
    
    # Interquartile Range (IQR)
    def FindOutlier(self,dataset: List[VideoProfile]) -> pd.DataFrame:
        try:
            LoggingInfo("FindOutlier: Finding Outlier process started")    
            dataset = [[row.video_id, row.views] for row in dataset]
            df = pd.DataFrame(dataset, columns=["video_id", "views"])
            
            # Calculate the IQR for views
            Q1 = df['views'].quantile(0.25)
            Q3 = df['views'].quantile(0.75)
            IQR = Q3 - Q1
            
            # Define the threshold for outliers
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Find outliers and return video_ids
            outliers = df[(df['views'] < lower_bound) | (df['views'] > upper_bound)]
            LoggingInfo("FindOutlier: Finding Outlier process ended")
            return outliers

        except Exception as e:
            LoggingError("FindOutlier: Finding Outlier process failed with error: " + str(e))
            