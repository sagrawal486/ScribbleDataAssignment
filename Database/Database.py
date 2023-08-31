from Models.VideoProfile import VideoProfileDB,VideoProfile
from typing import List
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from logger import LoggingError,LoggingInfo

class Database:

    def __init__(self, db_url) -> None:
        self.DBURL = db_url
        self.engine = create_engine(self.DBURL)
        #self.Base = declarative_base()

    def InitializeDatabase(self):
        # Drop the table if it exists
        drop_table_query = text("DROP TABLE IF EXISTS video_profiles")
        with self.engine.connect() as connection:
            connection.execute(drop_table_query)

        VideoProfileDB.__table__.create(bind=self.engine)

    def SaveProfileIntoSqlite(self,video_profiles: List[VideoProfile]):
        LoggingInfo("Database: Saving into database started")
        Session = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        session = Session()

        try:
            for profile in video_profiles:
                db_profile = VideoProfileDB(**profile.dict())
                session.add(db_profile)
            session.commit()
            LoggingInfo("Database: Saving into database ended")
        except Exception as e:
            session.rollback()
            LoggingError("Database: Saving into database failed with error: " + str(e))
        finally:
            session.close()


    def GetProfiles(self,region: str) -> List[VideoProfile]:
        try:
            LoggingInfo("Database: Getting data from database started")
            Session = sessionmaker(bind=self.engine)
            session = Session()
            query = session.query(VideoProfileDB).filter_by(region=region)
            results = query.all()
            session.close()
            LoggingInfo("Database: Getting data from database ended")
            return results
        except Exception as e:
            session.close()
            LoggingError("Database: Getting data from database failed with error: " + str(e))
                
