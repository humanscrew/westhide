
from flask import json, request
from flask_restful.reqparse import RequestParser
from flask_jwt_extended import get_jwt_identity

from myapi.utils import AES, RSA


class CipherHook:

    def encryptResponse(self, response):
        if request.method == "OPTIONS":
            return response
        try:
            parser = RequestParser()
            parser.add_argument('__aesKey', type=str, help='aesKey cannot be converted')
            parser.add_argument('__aesIV', type=str, help='aesKey cannot be converted')
            args = parser.parse_args()

            __aesKey = args.get("__aesKey")
            __aesIV = args.get("__aesIV")
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
        if not privateKey and not userInfo:
            userInfo = get_jwt_identity()
        if request.is_json:
            self.handleRequestData(request.json, userInfo, privateKey)
        if request.args:
            request.args = self.handleRequestData(request.args.to_dict(), userInfo, privateKey)
        return None

    def handleRequestData(self, args={}, userInfo=None, privateKey=None):
        aesKeyWithRSA = request.headers.get('aesKey', None)
        aesIVWithRSA = request.headers.get("aesIV", None)
        if not aesKeyWithRSA or not aesIVWithRSA:
            return None
        args, __aesKey, __aesIV = RSA().decryptWithRSA(args, aesKeyWithRSA, aesIVWithRSA, userInfo, privateKey)
        args.update(__aesKey=__aesKey, __aesIV=__aesIV)
        return args
