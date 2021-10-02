
from flask import json, request
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import get_jwt_identity

from myapi.utils import AES, RSA


class CipherHook:

    def encryptResponse(self, response):
        if request.method == "OPTIONS":
            return response
        parser = RequestParser()
        parser.add_argument('aesKey', type=str, help='aesKey cannot be converted')
        parser.add_argument('aesIV', type=str, help='aesKey cannot be converted')
        args = parser.parse_args()
        try:
            __aesKey = args.get("aesKey")
            __aesIV = args.get("aesIV")
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
        if request.method == "OPTIONS":
            return None
        if request.is_json:
            self.handleRequestData(request.json, userInfo, privateKey)
        if request.args:
            request.args = self.handleRequestData(request.args.to_dict(), userInfo, privateKey)
        return None

    def handleRequestData(self, args={}, userInfo=None, privateKey=None):
        aesKeyWithRSA = args.pop("aesKey", None)
        aesKeyWithIV = args.pop("aesIV", None)
        if not aesKeyWithRSA or not aesKeyWithIV:
            return None
        if not privateKey and not userInfo:
            userInfo = get_jwt_identity()
        args, __aesKey, __aesIV = RSA().decryptWithRSA(args, aesKeyWithRSA, aesKeyWithIV, userInfo, privateKey)
        args.update(aesKey=__aesKey, aesIV=__aesIV)
        return args
