from flask import request, json
from Crypto.Cipher import AES as AESMod
from Crypto.Util.Padding import pad, unpad
# from binascii import b2a_hex, a2b_hex

import base64


class AES:

    def __init__(self, aesKey, aesIV):
        self.__aesKey = aesKey.encode()
        self.__aesIV = aesIV.encode()
        self.__cryptos = AESMod.new(self.__aesKey, AESMod.MODE_OFB, self.__aesIV)

    def encrypt(self, text):
        textPad = pad(text.encode(), 16, style='pkcs7')
        encryptText = self.__cryptos.encrypt(textPad)
        encryptText2Base64 = base64.b64encode(encryptText).decode()
        # return b2a_hex(encryptText).decode()
        return encryptText2Base64

    def decrypt(self, text):
        encryptText = base64.b64decode(text)
        textPad = self.__cryptos.decrypt(encryptText)
        decryptText = unpad(textPad, 16, style='pkcs7').decode()
        return decryptText


def encryptResponse(response):
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
