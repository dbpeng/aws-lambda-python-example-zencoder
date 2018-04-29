import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import json
from base import Session, engine, Base
from enum import Enum

VIDEOS_S3_PATH = os.environ["VIDEOS_S3_PATH"]

class VideoJobState(Enum):
    INIT = 0
    DONE = 3
    CANCEL = 4

class VideoTranscodeJob(Base):
    __tablename__ = "TranscodingJob"
    id = Column("ID", Integer, primary_key=True)
    src = Column("Src", String(100))
    dst = Column("Dst", String(100))
    playUrl = Column("VideoUrl", String(256))
    config = Column("Config", String(100))
    vendor = Column("Vendor", String(100))
    jobId = Column("JobId", String(100))
    progress = Column("Progress", Integer)
    webhook = Column("Webhook", String(300))
    created_At = Column("Created_At", DateTime, default=datetime.now)
    updated_At = Column("Updated_At", DateTime, onupdate=datetime.now)
    
    def __init__(self):
        self.progress = 0

    def setConfig(self, config):
        self.config = config
        filename = "profiles/"+self.config+".json"
        with open(filename, 'r') as f:
            datastore = json.load(f)
        self.configContext = datastore

    def getConfig(self):
        return self.config
    
    def getConfigContext(self):
        return self.configContext

    def setSrc(self, src):
        self.src = src

    def getSrc(self):
        return self.src

    def setPlaybackUrl(self, url):
        # TODO: should validate url scheme here
        self.playUrl = url

    def getPlaybackUrl(self):
        return self.playUrl

    def setDst(self, dst):
        # this part needs a revamp, we should not by default assume it's HLS
        self.dst = VIDEOS_S3_PATH + dst + "/playlist.m3u8"

    def getDst(self):
        return self.dst
    
    def setVendor(self, vendorId):
        self.vendor = vendorId

    def getVendor(self):
        return self.vendor

    def setJobId(self, jobid):
        self.jobId = jobid
    
    def getJobId(self):
        return self.jobId
    
    def setWebhook(self, url):
        self.webhook = url
    
    def getWebhook(self):
        return self.webhook

    def setProgress(self, status):
        self.progress = status
    
    def getProgress(self):
        return self.progress
    
    def getCreatedTime(self):
        return self.createTime
    
    def getUpdatedTime(self):
        return self.updatedTime
    
    def setId(self, id):
        self.id = id

    def getId(self):
        return self.id

    def getJobDescription(self):
        # self.configContext['input'] = self.getSrc()
        for output in self.configContext['output']:
            output['base_url'] = self.getDst()
        return self.configContext

    def submit(self):
        pass

# if __name__ == "__main__":
#     session = Session()
#     vjob = VideoTranscodeJob()
#     vjob.setSrc("s3://wowza-video/hk33456678.mp4")
#     vjob.setDst("13ffjsdhr")
#     vjob.setConfig("zen-hls")
#     vjob.setJobId("13556245")
#     vjob.setVendor("zencoder")
    
#     session.add(vjob)
#     session.commit()

#     # jobs = session.query(VideoTranscodeJob).all()

#     # for job in jobs:
#     #     job.setProgress(4)

#     # session.commit()
#     session.close()
