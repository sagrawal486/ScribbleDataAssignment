from BackgroundTasks.CreateProfile import CreateProfile
import sys
import configparser
from Database.Database import Database
from Outliers.ViewsOutlier import ViewOutlier
from Workflows.CategoryPopularity import CategoryPopularity
from Workflows.TrendingVideos import TrendingVideos
import pandas as pd
from logger import LoggingInfo,LoggingError
def main(args):
    
    try:
        LoggingInfo("Create profile process started")
        
        # Read configuration from config.ini
        config = configparser.ConfigParser()
        config.read("config.ini")

        regions = config["Regions"]
        dataset_path = config.get('Path','DataSetPath')
        attributes = config["Attributes"]

        db_url = config.get('Database','DBURL')

        # Create Profile
        create_profile = CreateProfile(regions,attributes,dataset_path)
        video_profiles = create_profile.createProfile()

        LoggingInfo("Create profile process ended")
        LoggingInfo("Saving profile process started")
        # Store profiles in sqlite
        database = Database(db_url)
        database.InitializeDatabase()
        status = database.SaveProfileIntoSqlite(video_profiles)    
        LoggingInfo("Saving profile process ended")
        LoggingInfo("Finding outliers process started")
        # Find Outliers based on views
        region = 'US'
        video_profiles = database.GetProfiles(region)
        views_outlier_obj = ViewOutlier()
        outliers = views_outlier_obj.FindOutlier(video_profiles)
        outliers.to_excel('ViewsOutliers.xlsx', index=False)
        LoggingInfo("Outliers saved into ViewsOutliers excel file")
    except Exception as E:
        LoggingError("Exiting main function with Error: " + str(E))
if __name__ == "__main__":
    main(sys.argv[1:])
