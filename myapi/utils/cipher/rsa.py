from Crypto.PublicKey import RSA as RSAMod
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random

# import Crypto.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5 # 用于签名/验签
import base64

from flask import json, jsonify

from myapi.struct.models import User, RSAModel, DefaultRSAModel
from myapi.struct.schemas import RSASchema, DefaultRSASchema
from myapi.extensions import db

from .aes import AES


class RSA:
    @staticmethod
    def create_rsa():
        rsa_key = RSAMod.generate(2048, Random.new().read)
        public_key = rsa_key.publickey().export_key().decode()
        private_key = rsa_key.export_key().decode()

        return public_key, private_key

    @staticmethod
    def encrypt(text, public_key):
        public_cipher = PKCS1_v1_5.new(RSAMod.importKey(public_key))
        encrypt_text = public_cipher.encrypt(text.encode())
        encrypt_text2base64 = base64.b64encode(encrypt_text).decode()

        return encrypt_text2base64

    @staticmethod
    def decrypt(text, private_key):
        encrypt_text = base64.b64decode(text)
        private_cipher = PKCS1_v1_5.new(RSAMod.importKey(private_key))
        decrypt_text = private_cipher.decrypt(encrypt_text, Random.new().read).decode()
        return decrypt_text

    def set_rsa_key(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return None
        user_id = user.id
        rsa = user.utils_rsa
        public_key, private_key = self.create_rsa()
        if rsa:
            rsa_schema = RSASchema(partial=True)
            rsa_schema.load(
                {"userId": user_id, "publicKey": public_key, "privateKey": private_key},
                instance=rsa,
            )
        else:
            rsa = RSAModel(
                user_id=user_id, public_key=public_key, private_key=private_key
            )
            db.session.add(rsa)
        db.session.commit()

        return public_key

    @staticmethod
    def get_rsa_key(user_info):
        rsa_key = (
            RSAModel.query.filter_by(user_id=user_info).first()
            or User.query.filter_by(username=user_info).first().utils_rsa
        )
        if not rsa_key:
            return jsonify({"message": "获取公钥失败"}), 401
        rsa_schema = RSASchema(
            only=(
                "public_key",
                "private_key",
            )
        )

        return rsa_schema.dump(rsa_key)

    @staticmethod
    def get_default_rsa():
        default_rsa_schema = DefaultRSASchema()
        default_rsa = DefaultRSAModel.query.first()

        return {**default_rsa_schema.dump(default_rsa)}

    # 用RSA解密aesKey，用解密后的aesKey，解密AES加密的密文
    def decrypt_with_rsa(
        self, cipher_var, aes_key_with_rsa, aes_iv_with_rsa, user_info, private_key=None
    ):
        if private_key:
            rsa_private_key = private_key
        else:
            rsa_private_key = self.get_rsa_key(user_info).get("privateKey")
        __aesKey = self.decrypt(aes_key_with_rsa, rsa_private_key)
        __aesIV = self.decrypt(aes_iv_with_rsa, rsa_private_key)
        if isinstance(cipher_var, (dict,)):
            for key in cipher_var:
                encrypt_text = cipher_var[key]
                text = AES(__aesKey, __aesIV).decrypt(encrypt_text)
                if text:
                    cipher_var[key] = json.loads(text)
                else:
                    cipher_var[key] = None
        elif isinstance(cipher_var, (str,)):
            text = AES(__aesKey, __aesIV).decrypt(cipher_var)
            cipher_var = json.loads(text)

        return cipher_var, __aesKey, __aesIV
