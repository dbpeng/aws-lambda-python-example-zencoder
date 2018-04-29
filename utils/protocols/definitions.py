import json

class ResponseBase(object):
    def __init__(self, statusCode, isBase64=False):
        self.statusCode = statusCode
        self.base64 = isBase64
        self.headers = {}

    def getStatusCode(self):
        return self.statusCode
    
    def isBase64(self):
        return self.base64

    def addHeader(self, key, value):
        self.headers[key] = value

    def getHeader(self, key):
        if key in self.headers: 
            return self.headers[key]
        else:
            return None 

    def getHeaders(self):
        return self.headers

    def getBody(self):
        pass
    
    def getAWSLambdaProxyResponse(self):
        res = {
            "isBase64Encoded": self.isBase64(),
            "statusCode": self.getStatusCode(),
            "headers": self.getHeaders(),
            "body": self.getBody()
        }

        return res


class TranscoderSuccessResponse(ResponseBase):
    def __init__(self):
        super(TranscoderSuccessResponse, self).__init__(200, False)
        self.addHeader("Content-Type", "application/json")
    def getBody(self):
        body = {
            "code": 200
        }

        return json.dumps(body)

class TranscoderDoneResponse(ResponseBase):
    def __init__(self):
        super(TranscoderDoneResponse, self).__init__(200, False)
        self.addHeader("Content-Type", "application/json")

    def getBody(self):
        body = {
            "code": 200
        }

        return json.dumps(body)

class TranscoderError(ResponseBase):
    def __init__(self, statusCode, errorCode, errorMessage):
        super(TranscoderError, self).__init__(statusCode, False)
        self.addHeader("Content-Type", "application/json")
        self.errorCode = errorCode
        self.errorMessage = errorMessage

    def getBody(self):
        body = {
            "code": self.errorCode,
            "message": self.errorMessage
        }
        return json.dumps(body)

class TranscoderError400(TranscoderError):
    def __init__(self, code, message):
        super(TranscoderError400, self).__init__(400, code, message)

class TranscoderError404(TranscoderError):
    def __init__(self, code, message):
        super(TranscoderError404, self).__init__(404, code, message)


