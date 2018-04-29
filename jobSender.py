from utils.videoJob import VideoTranscodeJob
from utils.base import Base
from utils.transcoder import ProviderZencoder
from utils.base import Session, engine, Base
from utils.protocols.definitions import TranscoderSuccessResponse, TranscoderError400
import shortuuid
import json
import traceback

session = Session()

def _processVideo(src, provider, profile, webhook=""):
    # 1. create the transcoding job
    job = VideoTranscodeJob()
    job.setSrc(src)
    job.setDst(shortuuid.uuid())
    job.setVendor(provider)
    job.setConfig(profile)
    if webhook != "":
        job.setWebhook(webhook)
    session.add(job)
    session.commit()
    # 2. operate the zencoder sdk to submit
    coder = ProviderZencoder(job)
    response = coder.execute()
    # 3. update the job id
    job.setJobId(response)
    # 4. write to database
    session.commit()
    

def awsSnsHandler(event, context):
    if type(event) is not dict:
        raise Exception("event is not a dictionary type")
    # parse the source / provider / profile through SNS
    transcodeContext = event['Records'][0]['Sns']['Message']['default']
    _processVideo(transcodeContext['src'],
                    "zencoder",
                    transcodeContext['profile'], 
                    webhook=transcodeContext["webhook"])
    # return success or error
    session.close()

def awsEndpointHandler(event, context):
    # (https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format)
    if event['isBase64Encoded'] is True:
        requestBodyStr = event['body'].decode('base64')
    else:
        requestBodyStr = event['body']

    reqBody = json.loads(requestBodyStr)
    
    try:
        if "webhook" in reqBody:
            _processVideo(reqBody['src'], "zencoder", reqBody['profile'], webhook=reqBody['webhook'])
        else:
            _processVideo(reqBody['src'], "zencoder", reqBody['profile'])
    except:
        traceback.print_exc()
        error = TranscoderError400("50000", "general error")
        return error.getAWSLambdaProxyResponse()

    success = TranscoderSuccessResponse()
    return success.getAWSLambdaProxyResponse()
    # return sucess or error

# if __name__ == "__main__":
#     testData = {
#         "Records": [
#             {
#                 "Sns": {
#                     "Message": {
#                         "default": {
#                             "src": "https://wowza-video.escapex.com/hk3345678-2.mp4",
#                             "profile": "zen-hls",
#                             "webhook": "http://www.kimo.com.tw"
#                         }
#                     }
#                 }
#             }
#         ]
#     }

#     awsSnsHandler(testData, "")

