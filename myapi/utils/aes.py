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
