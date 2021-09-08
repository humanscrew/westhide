from Crypto.PublicKey import RSA as RSAMod
from Crypto.Cipher import PKCS1_v1_5
from Crypto import Random
# import Crypto.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5 # 用于签名/验签
import base64

from myapi.extensions import db, ma
from myapi.models.user import User

from sqlalchemy.ext.hybrid import hybrid_property

from flask import request
from flask_restful import Resource


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
            schema = RSASchema(partial=True)
            rsa = schema.load(
                {"user_id": user_id, "public_key": publicKey, "private_key": privateKey},
                instance=rsa
            )
        else:
            rsa = RSAModel(user_id=user_id, public_key=publicKey, private_key=privateKey)
            db.session.add(rsa)
        db.session.commit()
        return publicKey

    def getRSAKey(self, user):
        RSAKey = RSAModel.query.filter_by(user_id=user).first() or User.query.filter_by(username=user).first().utils_rsa
        return {
            "publicKey": RSAKey.public_key,
            "privateKey": RSAKey.private_key
        }


class RSAModel(db.Model):
    __tablename__ = "utils_rsa"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    public_key = db.Column(db.Text, nullable=False)
    _private_key = db.Column("private_key", db.Text, nullable=False)

    user = db.relationship('User', backref=db.backref("utils_rsa", uselist=False),  uselist=False, lazy='joined')

    @hybrid_property
    def private_key(self):
        return self._private_key

    @private_key.setter
    def private_key(self, value):
        self._private_key = value


class RSASchema(ma.SQLAlchemyAutoSchema):

    id = ma.Int(dump_only=True)
    user_id = ma.Int(required=True)
    public_key = ma.String(required=True)
    private_key = ma.String(load_only=True, required=True)

    class Meta:
        model = RSAModel
        sqla_session = db.session
        load_instance = True
        exclude = (["_private_key", "id"])


class RSAResource(Resource):

    def post(self):
        username = request.json.get("username")
        publicKey = RSA().setRSAKey(username)
        if not publicKey:
            return {"msg": "用户名错误"}, 400
        return {"publicKey": publicKey}
