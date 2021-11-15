
from flask import g, json, request
from flask_jwt_extended import get_jwt_identity

from .aes import AES
from .rsa import RSA


class CipherHook:

    def encryptResponse(self, response):
        if request.method == "OPTIONS":
            return response

        __aesKey = getattr(g, "aesKey", None)
        __aesIV = getattr(g, "aesIV", None)

        if not __aesKey or not __aesIV or not response.json:
            return response
        responseData = response.json
        for key in responseData:
            if key == "message":
                continue
            text = responseData[key]
            text = json.dumps(text)
            encryption = AES(__aesKey, __aesIV)
            responseData[key] = encryption.encrypt(text)
        response.data = json.dumps(responseData)

        return response

    def decryptRequest(self, userInfo=None, privateKey=None):
        if request.method == "OPTIONS":
            return None

        if not privateKey and not userInfo:
            userInfo = get_jwt_identity()
        if request.is_json:
            self.handleRequestData(request.json, userInfo, privateKey)
        if request.args:
            request.args = self.handleRequestData(request.args.to_dict(), userInfo, privateKey)
        if not request.json and not request.args:
            self.handleRequestData({}, userInfo, privateKey)

        return None

    def handleRequestData(self, args={}, userInfo=None, privateKey=None):
        aesKeyWithRSA = request.headers.get('aesKey', None)
        aesIVWithRSA = request.headers.get("aesIV", None)
        if not aesKeyWithRSA or not aesIVWithRSA:
            return None
        args, g.aesKey, g.aesIV = RSA().decryptWithRSA(args, aesKeyWithRSA, aesIVWithRSA, userInfo, privateKey)

        return args
