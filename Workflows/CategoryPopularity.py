from Models.VideoProfile import VideoProfile
from typing import List
import pandas as pd
from logger import LoggingInfo,LoggingError
from fastapi import HTTPException

class CategoryPopularity:
    
    def GetCategoryWiseData(self,dataset: List[VideoProfile]) -> List:
        try:
            LoggingInfo("GetCategoryWiseData: Getting Category Wise Data process started")        
            dataset = [[row.category_title, row.views, row.likes, row.dislikes, row.comment_count] for row in dataset]
            df = pd.DataFrame(dataset, columns=["category_title", "views", "likes", "dislikes", "comment_count"])
            
            # Group the data by category_title and calculate sum of views, likes, and comments
            category_popularity = df.groupby('category_title')[['views', 'likes', 'comment_count']].sum()

            # Sort the categories by total views in descending order
            sorted_categories = category_popularity.sort_values(by='views', ascending=False)

            # Display the top 10 popular categories
            top_popular_categories = sorted_categories.head(10).index.to_list()
            
            LoggingInfo("GetCategoryWiseData: Getting Category Wise Data process ended")
            
            return top_popular_categories
        
        except Exception as e:
            LoggingError("GetCategoryWiseData: Getting Category Wise Data process failed with error: " + str(e))
            raise HTTPException("Internal Server Error")
 
        