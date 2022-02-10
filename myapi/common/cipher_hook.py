from flask import g, json, request
from flask_jwt_extended import get_jwt_identity

from myapi.utils import AES
from myapi.utils import RSA


class CipherHook:
    @staticmethod
    def encrypt_response(response):
        if request.method == "OPTIONS":
            return response

        __aesKey = getattr(g, "aesKey", None)
        __aesIV = getattr(g, "aesIV", None)

        if not __aesKey or not __aesIV or not response.json:
            return response
        response_data = response.json
        for key in response_data:
            if key == "message":
                continue
            text = response_data[key]
            text = json.dumps(text)
            encryption = AES(__aesKey, __aesIV)
            response_data[key] = encryption.encrypt(text)
        response.data = json.dumps(response_data)

        return response

    @staticmethod
    def decrypt_request(user_info=None, private_key=None):
        if request.method == "OPTIONS":
            return None

        if not private_key and not user_info:
            user_info = get_jwt_identity()

        request_data = request.json or request.args.to_dict()

        aes_key_with_rsa = request.headers.get("aesKey", None)
        aes_iv_with_rsa = request.headers.get("aesIV", None)
        if not aes_key_with_rsa or not aes_iv_with_rsa:
            return None
        request_data, g.aesKey, g.aesIV = RSA().decrypt_with_rsa(
            request_data, aes_key_with_rsa, aes_iv_with_rsa, user_info, private_key
        )

        if request.json:
            request.json.update(**request_data)
        if request.args:
            setattr(request, "args", request_data)

        setattr(request, "data", json.dumps(request_data).encode())
        return None
