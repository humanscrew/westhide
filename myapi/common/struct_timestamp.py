from sqlalchemy import func
from datetime import datetime


def model_timestamp(db):
    db.Model.created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    db.Model.updated_at = db.Column(
        db.TIMESTAMP, server_default=func.now(), server_onupdate=func.now()
    )
    db.Table.created_at = db.Column(db.TIMESTAMP, server_default=func.now())
    db.Table.updated_at = db.Column(
        db.TIMESTAMP, server_default=func.now(), server_onupdate=func.now()
    )


def document_timestamp(mdb):
    mdb.Document.createdAt = mdb.DateTimeField(default=datetime.utcnow)
    mdb.Document.updatedAt = mdb.DateTimeField(default=datetime.utcnow)
