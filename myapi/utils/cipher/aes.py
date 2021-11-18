from Crypto.Cipher import AES as AESMod
from Crypto.Util.Padding import pad, unpad

# from binascii import b2a_hex, a2b_hex

import base64


class AES:
    def __init__(self, aes_key, aes_iv):
        self.__aes_key = aes_key.encode()
        self.__aes_iv = aes_iv.encode()
        self.__cryptos = AESMod.new(self.__aes_key, AESMod.MODE_OFB, self.__aes_iv)

    def encrypt(self, text):
        text_pad = pad(text.encode(), 16, style="pkcs7")
        encrypt_text = self.__cryptos.encrypt(text_pad)
        encrypt_text2base64 = base64.b64encode(encrypt_text).decode()
        # return b2a_hex(encrypt_text).decode()
        return encrypt_text2base64

    def decrypt(self, text):
        encrypt_text = base64.b64decode(text)
        text_pad = self.__cryptos.decrypt(encrypt_text)
        decrypt_text = unpad(text_pad, 16, style="pkcs7").decode()
        return decrypt_text
