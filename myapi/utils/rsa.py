from Crypto.PublicKey import RSA as RSAMod
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
# import Crypto.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5 # 用于签名/验签
import base64

from myapi.extensions import db, ma
from myapi.models import User

from flask import request, json, jsonify
from flask_restful import Resource


from myapi.utils import AES


class RSA:

    def createRSA(self):
        RSAKey = RSAMod.generate(2048, Random.new().read)
        publicKey = RSAKey.publickey().export_key().decode()
        privateKey = RSAKey.export_key().decode()
        return publicKey, privateKey

    def encrypt(self, text, publicKey):
        publicCipher = PKCS1_v1_5.new(RSAMod.importKey(publicKey))
        encryptText = publicCipher.encrypt(text.encode())
        encryptText2Base64 = base64.b64encode(encryptText).decode()
        return encryptText2Base64

    def decrypt(self, text, privateKey):
        encryptText = base64.b64decode(text)
        privateCipher = PKCS1_v1_5.new(RSAMod.importKey(privateKey))
        decryptText = privateCipher.decrypt(encryptText, Random.new().read).decode()
        return decryptText

    def setRSAKey(self, username):
        user = User.query.filter_by(username=username).first()
        if not user:
            return None
        user_id = user.id
        rsa = user.utils_rsa
        publicKey, privateKey = self.createRSA()
        if rsa:
            rsaSchema = RSASchema(partial=True)
            rsa = rsaSchema.load(
                {"userId": user_id, "publicKey": publicKey, "privateKey": privateKey},
                instance=rsa
            )
        else:
            rsa = RSAModel(user_id=user_id, public_key=publicKey, private_key=privateKey)
            db.session.add(rsa)
        db.session.commit()
        return publicKey

    def getRSAKey(self, userInfo):
        RSAKey = RSAModel.query.filter_by(user_id=userInfo).first() \
            or User.query.filter_by(username=userInfo).first().utils_rsa
        if not RSAKey:
            return jsonify({"message": "获取公钥失败"}), 401
        rsaSchema = RSASchema(only=("public_key", "private_key",))
        return rsaSchema.dump(RSAKey)

    def getDefaultRSA(self):
        defaultRSASchema = DefaultRSASchema()
        defaultRSA = DefaultRSAModel.query.first()
        return {**defaultRSASchema.dump(defaultRSA)}

    # 用RSA解密aesKey，用解密后的aesKey，解密AES加密的密文
    def decryptWithRSA(self, cipherVar, aesKeyWithRSA, aesIVWithRSA, userInfo, privateKey=None):
        if privateKey:
            rsaPrivatekey = privateKey
        else:
            rsaPrivatekey = self.getRSAKey(userInfo).get("privateKey")
        __aesKey = self.decrypt(aesKeyWithRSA, rsaPrivatekey)
        __aesIV = self.decrypt(aesIVWithRSA, rsaPrivatekey)
        if isinstance(cipherVar, (dict)):
            for key in cipherVar:
                encryptText = cipherVar[key]
                text = AES(__aesKey, __aesIV).decrypt(encryptText)
                cipherVar[key] = json.loads(text)
        else:
            text = AES(__aesKey, __aesIV).decrypt(cipherVar)
            cipherVar = json.loads(text)
        return cipherVar, __aesKey, __aesIV


class RSAModel(db.Model):
    __tablename__ = "utils_rsa"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    public_key = db.Column(db.Text, nullable=False)
    private_key = db.Column(db.Text, nullable=False)

    user = db.relationship('User', backref=db.backref("utils_rsa", uselist=False),  uselist=False, lazy='joined')


class RSASchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = RSAModel
        sqla_session = db.session
        load_instance = True
        include_fk = True
        exclude = (["id"])


class RSAResource(Resource):

    def post(self):
        username = request.json.get("username")
        publicKey = RSA().setRSAKey(username)
        if not publicKey:
            return {"message": "用户名错误"}, 400
        return {"publicKey": publicKey}


class DefaultRSAModel(db.Model):
    __tablename__ = "utils_default_rsa"
    id = db.Column(db.Integer, primary_key=True)
    public_key = db.Column(db.Text, nullable=False)
    private_key = db.Column(db.Text, nullable=False)


class DefaultRSASchema(ma.SQLAlchemyAutoSchema):

    class Meta:
        model = DefaultRSAModel
        sqla_session = db.session
        load_instance = True
        exclude = (["id", ])


class DefaultRSAResource(Resource):

    def get(self):
        defaultRSASchema = DefaultRSASchema(only=("public_key", ))
        defaultRSA = DefaultRSAModel.query.first_or_404()
        return {**defaultRSASchema.dump(defaultRSA)}
