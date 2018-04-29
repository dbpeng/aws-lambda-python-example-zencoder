from utils.base import Session, engine, Base
from utils.videoJob import VideoTranscodeJob, VideoJobState
from utils.protocols.definitions import TranscoderDoneResponse, TranscoderError400, TranscoderError404
import json
import requests
import traceback
import os

VIDEOS_OUTPUT_PATH = os.environ["VIDEOS_OUTPUT_PATH"]
VIDEOS_S3_PATH = os.environ["VIDEOS_S3_PATH"]

session = Session()

class VideoJobDoesNotExistException(Exception):
    pass

def _updateVideoJobStatus(jobId, status):
    print "updating status..."
    webhooks = []
    if status == "finished":
        statusCode = VideoJobState.DONE.value
    else:
        statusCode = VideoJobState.CANCEL.value
    
    jobs = session.query(VideoTranscodeJob).filter(VideoTranscodeJob.id == jobId).all()
    if len(jobs) == 0:
        raise VideoJobDoesNotExistException("job "+jobId+" doesn't exist")

    for job in jobs:
        if statusCode == VideoJobState.DONE.value:
            dst = job.getDst()
            playbackUrl = dst.replace(VIDEOS_S3_PATH, VIDEOS_OUTPUT_PATH)
            job.setPlaybackUrl(playbackUrl)
            if job.getWebhook() is not None and job.getWebhook() != "":
                webhooks.append(job.getWebhook())
        job.setProgress(statusCode)
    session.commit()
    # issue the notifications from getWebhook
    for webhook in webhooks:
        requests.get(webhook)

def awsEndpointHandler(event, context):
    # (https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format)
    print str(event)
    try:
        jobid = event['pathParameters']['jobid']
        if event['isBase64Encoded'] is True:
            reqBody = event['body'].decode('base64')
        else:
            reqBody = event['body']
        responseBody = json.loads(reqBody)
        status = responseBody['job']['state']
    except:
        traceback.print_exc()
        error = TranscoderError400("50000", "request meta parse error")
        return error.getAWSLambdaProxyResponse()

    try:
        _updateVideoJobStatus(jobid, status)
    except VideoJobDoesNotExistException:
        traceback.print_exc()
        error = TranscoderError404("50001", "job doesn't exist")
        return error.getAWSLambdaProxyResponse()
    except:
        traceback.print_exc()
        error = TranscoderError400("50100", "general error")
        return error.getAWSLambdaProxyResponse()
    
    success = TranscoderDoneResponse()
    return success.getAWSLambdaProxyResponse()


# if __name__ == "__main__":
#     _updateVideoJobStatus("9","finished")
