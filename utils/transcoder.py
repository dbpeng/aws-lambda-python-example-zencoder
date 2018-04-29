from zencoder import Zencoder
from videoJob import VideoTranscodeJob
import os
from enum import Enum

API_URL = os.environ["ZENCODER_URL"]
API_KEY = os.environ["ZENCODER_KEY"]
CREDENTIAL_NAME = os.environ["ZENCODER_CRED"]
WEBHOOK_ORIGIN = os.environ["VIDEOS_URL"]
WEBHOOK_PATH = os.environ["VIDEOS_PATH"]

class ZENCODER(Enum):
    RESPONSE_SUCCESS = 201
    
class ProviderBase(object):
    def __init__(self, videoJob):
        self.job = videoJob

class ProviderZencoder(ProviderBase):
    def __init__(self, videoJob):
        if not self._evalProfile(videoJob.getConfig()):
            raise Exception("video profile is not supported")
        super(ProviderZencoder, self).__init__(videoJob)
    
    def _evalProfile(self, profile):
        return True

    def execute(self):
        client = Zencoder(API_KEY)
        jobContext = self.job.getJobDescription()['output']
        uniquePath = WEBHOOK_PATH.replace("{jobid}", str(self.job.getId()))
        responseWebhook = WEBHOOK_ORIGIN + uniquePath
        response = client.job.create(self.job.getSrc(), 
                                        outputs=(jobContext), 
                                        options={
                                            "credentials": CREDENTIAL_NAME,
                                            "notifications": [responseWebhook]
                                        })
        if response.code == ZENCODER.RESPONSE_SUCCESS.value:
            return response.body['id']
        else:
            return -1

# if __name__ == "__main__":
#     job = VideoTranscodeJob()
#     job.setSrc("https://wowza-video.escapex.com/hk3345678-2.mp4")
#     job.setDst("133khfbjshr1")
#     job.setConfig("zen-hls")
#     job.setVendor("zencoder")
#     job.setId(8)
#     zen = ProviderZencoder(job)
#     job.setJobId(zen.execute())
#     print job.getJobId()
