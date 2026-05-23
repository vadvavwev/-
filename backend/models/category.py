from . import db
from datetime import datetime


class Category(db.Model):
    __tablename__ = "categories"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    devices = db.relationship("Device", back_populates="category", lazy="dynamic")
