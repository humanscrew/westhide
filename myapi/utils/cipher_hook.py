
from flask import request, json
from myapi.utils import AES, RSA
from flask_jwt_extended import get_jwt_identity


class CipherHook:

    def encryptResponse(self, response):
        if not response.data:
            return response
        try:
            requestData = request.json or request.args
            __aesKey = requestData.get("aesKey")
            __aesIV = requestData.get("aesIV")
            if not __aesKey or not __aesIV:
                return response
            responseData = response.json
            for key in responseData:
                text = responseData[key]
                text = json.dumps(text)
                encryption = AES(__aesKey, __aesIV)
                responseData[key] = encryption.encrypt(text)
            response.data = json.dumps(responseData)
        finally:
            return response

    def decryptRequest(self, userInfo=None, privateKey=None):
        if not request.method in ('GET', 'POST', 'PUT', 'DELETE'):
            return None
        if request.is_json:
            self.handleRequestData(request.json, userInfo, privateKey)
        if request.args:
            request.args = self.handleRequestData(request.args.to_dict(), userInfo, privateKey)
        return None

    def handleRequestData(self, requestData={}, userInfo=None, privateKey=None):
        aesKeyWithRSA = requestData.pop("aesKey", None)
        aesKeyWithIV = requestData.pop("aesIV", None)
        if not aesKeyWithRSA or not aesKeyWithIV:
            return None
        if not privateKey and not userInfo:
            userInfo = get_jwt_identity()
        requestData, __aesKey, __aesIV = RSA().decryptWithRSA(requestData, aesKeyWithRSA, aesKeyWithIV, userInfo, privateKey)
        requestData.update(aesKey=__aesKey, aesIV=__aesIV)
        return requestData
