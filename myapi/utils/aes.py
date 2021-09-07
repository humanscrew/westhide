from Crypto.Cipher import AES as AESMod
from Crypto.Util.Padding import pad, unpad
# from binascii import b2a_hex, a2b_hex

import base64

from myapi.utils.rsa import RSA


class AES:

    def encrypt(self, text, aesKey="abcdsxyzhkj12580"):
        cryptos = AESMod.new(aesKey.encode(), AESMod.MODE_ECB)
        textPad = pad(text.encode(), 16, style='pkcs7')
        encryptText = cryptos.encrypt(textPad)
        encryptText2Base64 = base64.b64encode(encryptText).decode()
        # return b2a_hex(encryptText).decode()
        return encryptText2Base64

    def decrypt(self, text, aesKey="abcdsxyzhkj12580"):
        encryptText = base64.b64decode(text)
        cryptos = AESMod.new(aesKey.encode(), AESMod.MODE_ECB)
        textPad = cryptos.decrypt(encryptText)
        decryptText = unpad(textPad, 16, style='pkcs7').decode()
        return decryptText

    # 用RSA解密aesKey，用解密后的aesKey，解密AES加密的密文
    def decryptWithRSA(self, text, aesKeyWithRSA, user_id):
        rsaPrivatekey = RSA().getRSAKey(user_id).get("privateKey")
        _aeskey = RSA().decrypt(aesKeyWithRSA, rsaPrivatekey)
        decryptText = self.decrypt(text, _aeskey)
        return decryptText, _aeskey
